# This is the test plan build (TPB) main file it hold the TPB class and some methods
import imp
import pickle
from Core.Base import ToolBasic

TestPlan = ToolBasic.TestPlan


class TPB(ToolBasic.ToolBasic):
    def __init__(self, _list=None):
        ToolBasic.ToolBasic.__init__(self)
        self.loop_flag = True
        if _list is None:
            self.test_plan = TestPlan([])
        else:
            self.test_plan = TestPlan(_list)
        self.test_plan_path = "Core/Base/TestPlan"

    def help_text(self):
        print "Help Text Method"
        f = self.open_file("Core/TPB/TPBHelp.txt")
        help_text = f.read()
        print help_text

    def full_test_plan(self):
        groups = self.list_all_groups()
        print groups
        self.test_plan.set_list(groups)
        self.dump_to_file(self.test_plan)
        self.loop_flag = False

    def single_test_plan(self):
        while True:
            group = [raw_input("Please Enter Group Name To Execute\n")]
            if self.check_is_group_exists(group[0]):
                self.test_plan.set_list([group[0]])
                if self.verify_tool_presence():
                    self.dump_to_file(self.test_plan)
                    break
                else:
                    print ("tool missing")
            else:
                print "Group Does not exists"
        self.loop_flag = False

    def custom_test_plan(self):
        groups = []
        while True:
            groups_raw = raw_input("Please Enter Groups Name To Execute, name "
                                   "separated in one space[Ping BruteForce TCP]\n")
            print groups_raw
            groups_pre = groups_raw.split(' ')
            print groups_pre
            for group in groups_pre:
                if self.check_is_group_exists(group):
                    if self.verify_tool_presence(TestPlan([group])):
                        groups.append(group)
                        print "Group: ", group, " exists and added to test plan"
                    else:
                        print "Group %s exists but tool missing" % group
                else:
                    print "Group: ", group, "Does not exists"
            print groups
            answer = raw_input("Are This Plan OK? (y/n)")
            if answer == "y" or answer == "yes":
                break
            else:
                groups = []
        self.test_plan.set_list(groups)
        self.dump_to_file(self.test_plan)
        self.loop_flag = False

    def dump_to_file(self, _input):
        input_file = open(self.test_plan_path, 'wb')
        pickle.dump(_input, input_file)
        input_file.close()

    def verify_tool_presence(self, _test_plan=TestPlan([])):
        if not _test_plan.get_list():
            tool_list = self.get_tool_demand(self.test_plan)
        else:
            tool_list = self.get_tool_demand(_test_plan)
        verify = True
        for tool in tool_list:
            try:
                imp.find_module(tool)
            except ImportError:
                verify = False
        return verify
