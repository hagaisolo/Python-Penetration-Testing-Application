# This is the Test Manager, it run the tests... it is also responsible for call the
# suitable feature for collecting parameters and output data from the tests.
"""
TM:
    method:
    __init__ : we instantiate a TM object with a test plan
    gather_param: instantiate a PG object, collects parameter according to test plan
    run_test: run tests according to test plan after gathered parameters
"""
from PG import PGMain
import pickle
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE
from accessories import switch_case


class TM(object):
    def __init__(self):
        self.test_plan = self.get_test_plan()

    def get_test_plan(self):
        test_plan_file = open("accessories/TestPlan", 'rb')
        temp_test_plan = pickle.load(test_plan_file)
        if temp_test_plan.group_list == '':
                print ("no groups were selected...\n")
        test_plan_file.close()
        return temp_test_plan

    def menu(self):
        print ("This is the Test Manager utility")
        flag = True
        while flag:
            switch = raw_input("1. Gather Parameters\n2. Run test\n3. exit the test manager\n")
            for case in switch_case.switch(switch):
                if case('1'):
                    self.gather_parameters()
                elif case('2'):
                    self.run_tests()
                elif case('3'):
                    flag = False
                    break
                else:
                    print ("not a valid choice")

    def gather_parameters(self):
        gatherer = PGMain.PG()
        gatherer.group_list = self.test_plan.group_list
        gatherer.gather_param_demand()
        gatherer.parameter_parser()
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

