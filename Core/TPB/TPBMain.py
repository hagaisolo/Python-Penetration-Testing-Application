# This is the test plan build (TPB) main file it hold the TPB class and some methods
import imp
import pickle
from Core.Base import ToolBasic

TestPlan = ToolBasic.TestPlan


class IoTCharacterization (object):
    def __init__(self):
        self.layers = [dict(), dict(), dict(), dict(), dict(), dict()]

    def add_characterization(self, _layer=1, _char=('type', 'value')):
        if _char[0] in self.layers[_layer]:
            self.layers[_layer][_char[0]].append(_char[1])
        else:
            self.layers[_layer][_char[0]] = [_char[1]]

    def print_all(self):
        for i in range (1, 6):
            print "Layer ", i, " : ",
            print self.layers[i]

    def find_tuple(self,  _char=('type', 'value'), _layers=[1,2,3,4,5,6]):
        for layer in _layers:
            for item in self.layers[layer]:
                if _char[0] in self.layers[layer]:
                    if   self.layers[layer][_char[0]] == [_char[1]]:
                        return True
                    elif self.layers[layer][_char[0]] == ['all']:
                        return True
        return False


class TPB(ToolBasic.ToolBasic):
    def __init__(self, _list=None):
        ToolBasic.ToolBasic.__init__(self)
        self.loop_flag = True
        if _list is None:
            self.test_plan = TestPlan([])
        else:
            self.test_plan = TestPlan(_list)
        self.test_plan_path = "Core/Base/TestPlan"
        self.iot = IoTCharacterization()
        self.iot_all = IoTCharacterization()
        self.iot_user = IoTCharacterization()

    def help_text(self):
        print "Help Text Method"
        f = self.open_file("Core/TPB/help.txt")
        help_text = f.read()
        print help_text

    def full_test_plan(self):
        groups = self.list_all_groups()
        print groups
        self.test_plan.set_list(groups)
        self.dump_to_file(self.test_plan)
        self.loop_flag = False

    def single_test_plan(self, group):
            if self.check_is_group_exists(group[0]):
                self.test_plan.set_list([group[0]])
                if self.verify_tool_presence():
                    self.dump_to_file(self.test_plan)
                    print group[0], " chosen"
                    return True
                else:
                    print ("tool missing")
                    return False
            else:
                print "Group Does not exists"
                return False
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

    def smart_test_plan(self):
        self.iot_all = self.build_characterization_list_full()
        self.iot_all.print_all()
        self.user_characterization()
        self.iot_user.print_all()
        temp_test_plan = []
        for group in self.list_all_groups():
            if self.test_if_group_allowed(group):
                temp_test_plan.append(group)
        self.test_plan.set_list(temp_test_plan)
        self.dump_to_file(self.test_plan)
        self.loop_flag = False

    def build_characterization_list_full(self):
        # collect all possible choices to device characterization from all groups
        iot = IoTCharacterization()
        for group in self.list_all_groups():
            self.build_characterization_list_group(iot, group)
        for layer in iot.layers:
            for key in layer:
                layer[key] = list(set(layer[key]))
        return iot

    def build_characterization_list_group(self, _iot, _group="Ping"):
        # collect all choices from one group
        root = self.get_xml_root(_group)
        for case in root:
            if case.tag == "testplan":
                for layer in case:
                    for charac in layer:
                        _iot.add_characterization(int(layer.attrib["layer"]), tuple((charac.attrib["type"], charac.text)))

    def user_characterization(self):
        # user characterize his device according to layer method
        print ("Characterizing device: ")
        print ("Layer 1 : ")
        for i in range(1,6 ):
            if self.iot_all.layers[i]:
                for item in self.iot_all.layers[i]:
                    flag = True
                    while flag:
                        print ("Choose one of the following for your device: "),
                        print item
                        choice = raw_input(self.iot_all.layers[i]).split()
                        for ch in choice:
                            if ch == "all":
                                self.iot_user.add_characterization(i, (item, ch))
                                flag = False
                            else:
                                if ch in self.iot_all.layers[i][item]:
                                    self.iot_user.add_characterization(i, (item, ch))
                                else:
                                    print ("invalid choice")
                                    flag = True
                                    break
                                flag = False


    def test_if_group_allowed(self, group):
        # test if group flag are included in the user flags specification
        root = self.get_xml_root(group)
        iot_group = IoTCharacterization()
        self.build_characterization_list_group(iot_group, group)
        # for each item in iot_group we check if it included in iot_user
        for layer_num in range(1,6):
            for item in iot_group.layers[layer_num]:
                value = iot_group.layers[layer_num][item]
                print item, value
                # check all list value, just one need to be found
                value_flag = False
                for v in value:
                    if self.iot_user.find_tuple(_char=(item,v), _layers=[layer_num]):
                        value_flag = True
                if not value_flag:
                    return False
        return True
