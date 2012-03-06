'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Requirement class itself
   
 (c) 2010-2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

import operator

from rmtoo.lib.digraph.Digraph import Digraph
from rmtoo.lib.BaseRMObject import BaseRMObject
from rmtoo.lib.logging.EventLogging import tracer
from rmtoo.lib.FuncCall import FuncCall
from rmtoo.lib.InputModuleTypes import InputModuleTypes

import sys
reload(sys)
# pylint: disable=E1101
sys.setdefaultencoding('utf-8')

class Requirement(Digraph.Node, BaseRMObject):

    def execute(self, executor, func_prefix):
        '''Execute the parts which are needed for Requirement.'''
        tracer.debug("Called: name [%s]." % self.name)
        FuncCall.pcall(executor, func_prefix + "requirement", self)
        tracer.debug("Finished: name [%s]." % self.name)

    # Requirement Type
    # Each requirement has exactly one type.
    # The class ReqType sets this from the contents of the file.
    # Note: There can only be one (master requirement)
    rt_master_requirement = 1
    # Initial requirement is deprecated
    rt_initial_requirement = 2
    rt_design_decision = 3
    rt_requirement = 4

    def __init__(self, content, rid, file_path, mls, mods, config):
        Digraph.Node.__init__(self, rid)
        BaseRMObject.__init__(self, InputModuleTypes.reqtag, 
                              content, rid, mls, mods,
                              config, "requirements", file_path)

    def get_prio(self):
        return self.values["Priority"]
    
    def __str__(self):
        '''Return the name/id of the requirement.'''
        return "Requirement [%s]" % self.get_id()
    
    def __repr__(self):
        return self.__str__()

    def get_status(self):
        return self.values["Status"]

    def get_topic(self):
        return self.values["Topic"]

    def get_efe_or_0(self):
        '''Returns the EfE units or 0 if not available.'''
        efe = self.get_value("Effort estimation")
        if efe == None:
            return 0
        return efe

    def is_implementable(self):
        return self.values["Class"].is_implementable()

    def write_analytics_result(self, mstderr):
        '''Write out the analytics results.'''
        for k, v in sorted(self.analytics.items(),
                           key=operator.itemgetter(0)):
            if v[0] < 0:
                mstderr.write("+++ Error:Analytics:%s:%s:result is '%+3d'\n"
                              % (k, self.id, v[0]))
                for l in v[1]:
                    mstderr.write("+++ Error:Analytics:%s:%s:%s\n" %
                                  (k, self.id, l))
