# This is the test plan build (TPB) main file it hold the TPB class and some methods
from accessories import switch_case
from accessories import GroupAndTestsLister
import pickle
from accessories import ToolBasic


class TestPlan(object):
    def __init__(self, some_list):
        self.group_list = []
        self.group_list.append(some_list)


class TPB(ToolBasic.ToolBasic):
    def intro_menu(self):
        print "Welcome To The TPB"
        print "The TPB will Help You Build The Most Suitable Test Design"
        print "\"Help\" for further instructions\n"
        loop_flag = True
        while loop_flag:
            x = raw_input("Choose Build Type Full/Single/Custom:")
            for case in switch_case.switch(x):
                if case('Help'):
                    self.help_text()
                elif case('List'):
                    GroupAndTestsLister.Lister()
                elif case('Full'):
                    pass  # Run full tests - all groups
                elif case('Single'):
                    while 1:
                        group = raw_input("Please Enter Group Name To Execute\n")
                        if self.check_is_group_exists(group):
                            break
                        print "Group Does not exists"
                    test_plan = TestPlan(group)
                    test_plan_file = open("accessories/TestPlan", 'wb')
                    pickle.dump(test_plan, test_plan_file)
                    test_plan_file.close()
                    loop_flag = False
                elif case('Quit'):
                    print "Exiting TPB...\n"
                    loop_flag = False
                elif case('Custom'):
                    #  creating a custom test plan
                    print ("This option is not supported yet...\n")
                else:
                    pass


