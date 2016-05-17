# This is the UI (User Interference), It is responsible to communicate the core and groups to the user,
# it can be forward developed into a GUI.
"""
UI:
    method:
    __init__ : we instantiate a UI object with a test plan
    gather_param: instantiate a PG object, collects parameter according to test plan
    run_test: run tests according to test plan after gathered parameters
"""
import pickle
from subprocess import Popen, CREATE_NEW_CONSOLE
from sys import executable

from Core.Base import switch_case
from Core.DA import DA
from Core.PG import PGMain
from Core.TPB import TPBMain
from Core.Base import ToolBasic

TPB = TPBMain.TPB


class UI(ToolBasic.ToolBasic):
    def __init__(self):
        ToolBasic.ToolBasic.__init__(self)

    def menu(self):
        print ("This is the Test Manager utility")
        flag = True
        while flag:
            switch = raw_input("1. Gather Parameters\n2. Run test\n3. View Data"
                               "\n4. Build test plan.\n5. Print test plan\n6. exit the test manager\n")
            for case in switch_case.switch(switch):
                if case('1'):
                    self.gather_parameters()
                elif case('2'):
                    self.run_tests()
                elif case('3'):
                    self.data_collect()
                elif case('4'):
                    self.build_test_plan()
                elif case('5'):
                    print self.get_test_plan().get_list()
                    break
                elif case('6'):
                    flag = False
                    break
                else:
                    print ("not a valid choice")

    def gather_parameters(self):
        gatherer = PGMain.PG()
        gatherer.group_list = self.get_test_plan().group_list
        gatherer.gather_param_demand()
        gatherer.insert_default_values()
        gatherer.gather_question_parameter()
        print gatherer.parameters
        param_file = open('Groups//parameters', 'wb')
        pickle.dump(gatherer.parameters, param_file)
        param_file.close()

    def run_tests(self):
        print "You've selected run_tests method"
        test_plan = self.get_test_plan()
        for item in test_plan.group_list:
            Popen([executable, 'Groups//'+item+'//' + item + '.py'], creationflags=CREATE_NEW_CONSOLE)
        pass

    @staticmethod
    def build_test_plan():
        builder = BuildTestPlan()
        builder.menu()

    @staticmethod
    def data_collect():
        data_analyzer = DA.DA()
        data_analyzer.menu()


class BuildTestPlan(object):
    def __init__(self):
        self.test_planner = TPB()
        self.loop_flag = True

    def menu(self):
        print "The TPB will Help You Build The Most Suitable Test Design"
        print "write \"Help\" for further instructions\n"
        while self.loop_flag:
            x = raw_input("Choose Build Type Full/Single/Custom:")
            for case in switch_case.switch(x):
                # Print the TPBHelp.txt document
                if case('Help'):
                    self.test_planner.help_text()
                    self.loop_flag = False

                # Print A list of all available groups
                elif case('List'):
                    self.test_planner.list_group()
                    self.loop_flag = False

                # Full test plan, run all available groups
                elif case('Full'):
                    self.test_planner.full_test_plan()
                    self.loop_flag = False

                # Single test plan, run specific group
                elif case('Single'):
                    self.test_planner.single_test_plan()
                    self.loop_flag = False

                # Create Custom test plan
                elif case('Custom'):
                    self.test_planner.custom_test_plan()
                    self.loop_flag = False

                # Quits the Test Plan Builder
                elif case('Quit'):
                    print "Exiting TPB...\n"
                    self.loop_flag = False

                else:
                    pass
