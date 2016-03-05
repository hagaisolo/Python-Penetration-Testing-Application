# This is the Test Manager, it run the tests... it is also responsible for call the
# suitable feature for collecting parameters and output data from the tests.
"""
TM:
    method:
    __init__ : we instantiate a TM object with a test plan
    gather_param: instantiate a PG object, collects parameter according to test plan
    run_test: run tests according to test plan after gathered parameters
"""
import imp
from PG import PGMain
import pickle
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE


class TM(object):
    def __init__(self, test_plan_input):
        self.test_plan = test_plan_input

    def gather_parameters(self):
        gatherer = PGMain.PG()
        gatherer.group_list = self.test_plan.group_list
        gatherer.gather_param_demand()
        gatherer.gather_question_parameter()
        print gatherer.parameters
        param_file = open('Groups//parameters', 'wb')
        pickle.dump(gatherer.parameters, param_file)
        param_file.close()

    def run_tests(self):
        print "You've selected run_tests method"
        for item in self.test_plan.group_list:
            Popen([executable, 'Groups//'+item+'//' + item + '.py'], creationflags=CREATE_NEW_CONSOLE)
        pass

# For debug purposes
if __name__ == "__main__":
    test = TM()

