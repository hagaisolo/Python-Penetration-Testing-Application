# This is the Data Analyzer / Collector class
from accessories import ToolBasic
import pickle   # later maybe import pickle only at ToolBasic and create functions there
from accessories import switch_case

class DA(ToolBasic.ToolBasic):
    def __init__(self):
        self.stats = 0
        self.menu()

    def menu(self):
        print "Welcome To The Data Analyzer / Collector Utility"
        print "The DA will Help Analyze and Parse the ouput data"
        print "\"Help\" for further instructions\n"
        loop_flag = True
        while loop_flag:
            x = raw_input("Choose Build Type Full/Single/Custom:")
            for case in switch_case.switch(x):
                # Print the TPBHelp.txt document
                if case('Help'):
                    self.help_text()

                # Print A list of all available groups
                elif case('List'):
                    self.list_group()

                # Full test plan, run all available groups
                elif case('Full'):
                    groups = self.list_all_groups()
                    print groups
                    test_plan = TestPlan(groups)
                    test_plan_file = open("accessories/TestPlan", 'wb')
                    pickle.dump(test_plan, test_plan_file)
                    test_plan_file.close()
                    loop_flag = False

                # Single test plan, run specific group
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

                # Create Custom test plan
                elif case('Custom'):
                    while 1:
                        groups_raw = raw_input("Please Enter Group Name To Execute\n")
                        print groups_raw
                        groups_raw = groups_raw.replace(" ", "")
                        print groups_raw
                        groups_pre = groups_raw.split(',')
                        print groups_pre
                        groups = []
                        for group in groups_pre:
                            if self.check_is_group_exists(group):
                                groups.append(group)
                                print "Group: ", group, " exists and added to test plan"
                            else:
                                print "Group: ", group, "Does not exists"
                        answer = raw_input("Are This Plan OK? (y/n)")
                        if answer is "y" or "yes":
                            break
                    test_plan = TestPlan(groups)
                    test_plan_file = open("accessories/TestPlan", 'wb')
                    pickle.dump(test_plan, test_plan_file)
                    test_plan_file.close()
                    loop_flag = False

                # Quits the Test Plan Builder
                elif case('Quit'):
                    print "Exiting TPB...\n"
                    loop_flag = False

                else:
                    pass