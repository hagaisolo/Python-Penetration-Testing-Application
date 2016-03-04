# This is the Test Manager, it run the tests... it is also responsible for call the
# suitable feature for collecting parameters and output data from the tests.
import imp
from PG import PGMain


class TM(object):
    def __init__(self, test_plan_input):
        self.test_plan = test_plan_input

    def gather_parameters(self):
        gatherer = PGMain.PG()
        gatherer.gather_param_demand(self.test_plan.group_list)
        print gatherer.parameters


