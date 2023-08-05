import datetime
import collections

import synapse.common as s_common
import synapse.eventbus as s_eventbus
import synapse.telepath as s_telepath

import synapse.lib.config as s_config
import synapse.lib.reflect as s_reflect

import synapse.cores.common as s_cores_common

MODEL_REV_FORMAT = '%Y%m%d%H%M'

def modelrev(name, vers):
    '''
    A decorator used to flag model revision functions.

    Args:
        name (str): Name of the model.
        vers (int): Revision of the model. It is validated using validate_revnumber.
    '''

    def wrap(f):
        f._syn_mrev = (name, vers)
        return f

    return wrap

def validate_revnumber(revision):
    '''
    Validate a model revision number matches the time format '%Y%m%d%H%M'

    Args:
        revision (int): Revision to validate.

    Raises:
        BadRevValu: If the integer does not match the time format.
    '''
    try:
        if revision != 0:
            datetime.datetime.strptime(str(revision), MODEL_REV_FORMAT)
    except ValueError as e:
        raise s_common.BadRevValu(valu=revision, mesg='CoreModule model revision must be a timestamp.')

class CoreModule(s_eventbus.EventBus, s_config.Configable):
    '''
    The CoreModule base class from which cortex modules must extend.

    This module interface implements helper APIs to facilitate cortex
    extensions.

    To load a module within a cortex, add it to the list of modules in
    the cortex config ( mostly likely within your dmon config ) as shown:

    # example cortex config
    {
        "modules":[
            ["foopkg.barmod.modctor", {
                "foo:opt":10,
                "bar:opt":"http://www.vertex.link"
            }]
        ]
    }

    Modules may extend the cortex in various ways such as:

        * Implement and enforce data model additions
        * Enrich properties during node creation / modification
        * Add "by" handlers and side-pocket indexes to extend queries
        * Add custom storm/swarm operators to the query language
        * etc etc etc...

    NOTE: The cortex which loads the module plumbs all events into the
          CoreModule instance using EventBus.link().
    '''

    def __init__(self, core, conf):
        s_eventbus.EventBus.__init__(self)
        s_config.Configable.__init__(self)

        s_telepath.reqNotProxy(core)

        self.core = core  # type: s_cores_common.Cortex
        core.link(self.dist)

        def fini():
            core.unlink(self.dist)

        self.onfini(fini)

        # check for decorated functions for model rev
        self._syn_mrevs = []

        for name, meth in s_reflect.getItemLocals(self):
            mrev = getattr(meth, '_syn_mrev', None)
            if mrev is None:
                continue

            name, vers = mrev
            self._syn_mrevs.append((name, vers, meth))

        self.initCoreModule()
        self.setConfOpts(conf)
        self.postCoreModule()

    def form(self, form, valu, **props):
        '''
        A module shortcut for core.formTufoByProp()

        Args:
            form (str): The node form to retrieve/create
            valu (obj): The node value
            **props:    Additional node properties

        '''
        return self.core.formTufoByProp(form, valu, **props)

    def initCoreModule(self):
        '''
        Module implementers may over-ride this method to initialize the
        module during initial construction.  Any exception raised within
        this method will be raised from the constructor and mark the module
        as failed.

        Args:

        Returns:
            (None)
        '''
        pass

    def postCoreModule(self):
        '''
        Module implementers may over-ride this method to initialize the module
        *after* the configuration data has been loaded.

        Returns:
            (None)

        '''
        pass

    @staticmethod
    def getBaseModels():
        '''
        Get a tuple containing name, model values associated with the CoreModule.

        Any models which are returned by this function are considered revision 0 models for the name, and will be
        automatically loaded into a Cortex if the model does not currently exist.

        Note:
            While this may return multiple tuples, internal Synapse convention is to define a single model in a
            single CoreModule subclass in a single file, for consistency.

        Returns:
            ((str, dict)): A tuple containing name, model pairs.
        '''
        return ()

    def getModlRevs(self):
        '''
        Generate a list of ( name, vers, func ) tuples for model revisions in this module.

        Returns:
            ([ (str, int, func), ... ])

        Example:

            for name, vers, func in modu.getModlRevs():
                core.revModlVers(name,revs)
        '''
        return list(self._syn_mrevs)

    def onFormNode(self, form, func):
        '''
        Register a callback to run during node formation.  This callback
        will be able to set properties on the node prior to construction.

        Args:
            form (str): The name of the node creation
            func (function): A callback

        Returns:
            (None)

        Example:

            def myFormFunc(form, valu, props, mesg):
                props['foo:bar:baz'] = 10

            self.onFormNode('foo:bar', myFormFunc)

        NOTE: This may not be used for a module loaded with a remote cortex.
        '''

        def distfunc(mesg):
            form = mesg[1].get('form')
            valu = mesg[1].get('valu')
            props = mesg[1].get('props')

            return func(form, valu, props, mesg)

        def fini():
            self.core.off('node:form', distfunc)

        self.core.on('node:form', distfunc, form=form)
        self.onfini(fini)

    def onNodeAdd(self, func, form=None):
        '''
        Register a callback to run when a node is added.

        Args:
            func (function): The callback
            form (str): The form of node to watch for (or all!)

        Returns:
            (None)

        Example:

            def callback(node):
                dostuff(node)

            self.onNodeAdd(callback, form='inet:fqdn')

        '''
        def dist(mesg):
            node = mesg[1].get('node')
            func(node)

        def fini():
            self.core.off('node:add', dist)

        self.core.on('node:add', dist, form=form)
        self.onfini(fini)

    def onNodeDel(self, func, form=None):

        '''
        Register a callback to run when a node is deleted.

        Args:
            func (function): The callback
            form (str): The form of node to watch for (or all!)

        Returns:
            (None)

        Example:

            def callback(node):
                dostuff(node)

            self.onNodeDel(callback, form='inet:fqdn')
        '''
        def dist(mesg):
            node = mesg[1].get('node')
            func(node)

        def fini():
            self.core.off('node:del', dist)

        self.core.on('node:del', dist, form=form)
        self.onfini(fini)

    # TODO: many more helper functions which wrap event conventions with APIs go here...
