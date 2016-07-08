# This is the test plan build (TPB) main file it hold the TPB class and some methods
import imp
import pickle
from Core.Base import ToolBasic

TestPlan = ToolBasic.TestPlan


class IoTCharacterization (object):
    def __init__(self):
        self.layers = [dict(), dict(), dict(), dict(), dict()]

    def add_characterization(self, _layer=1, _char=('type', 'value')):
        if _char[0] in self.layers[_layer-1]:
            self.layers[_layer-1][_char[0]].append(_char[1])
        else:
            self.layers[_layer-1][_char[0]] = [_char[1]]

    def remove_characterization(self, _layer=1, _char=('type', 'value')):
        # add remove characterization method here
        if _char[0] in self.layers[_layer-1]:
            self.layers[_layer-1][_char[0]].remove(_char[1])
            if not self.layers[_layer-1][_char[0]]:
                self.layers[_layer-1].pop(_char[0], None)
        else:
            pass

    def print_all(self):
        string = ""
        for i in range(0, 5):
            string += "Layer %s : " % i
            string += str(self.layers[i])
            #  for item in self.layers[i].itervalues():
            #     string += ','.join(item)
            string += "\n"
        return string

    def find_tuple(self,  _char=('type', 'value'), _layers=(0, 1, 2, 3, 4)):
        for layer in _layers:
            if not self.layers[layer]:
                return True
            for item in self.layers[layer]:
                if _char[0] in self.layers[layer]:
                    if self.layers[layer][_char[0]] == [_char[1]]:
                        return True
                    elif self.layers[layer][_char[0]] == ['all']:
                        return True
                else:
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
        self.iot_all = self.build_characterization_list_full()
        self.iot_user = IoTCharacterization()

    def help_text(self):
        f = self.open_file("Core/TPB/help.txt")
        help_text = f.read()
        return help_text

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
                return True
            else:
                raise Exception("Tool missing")
        else:
            raise Exception("Group does not exists")

    def custom_test_plan(self, groups_raw):
        groups = []
        groups_pre = groups_raw.split(' ')
        for group in groups_pre:
            if self.check_is_group_exists(group):
                if self.verify_tool_presence(TestPlan([group])):
                    groups.append(group)
                else:
                    raise Exception("Tool missing for group: " + group)
            else:
                raise Exception("Group: "+ group+ " Does not exists")
        self.test_plan.set_list(groups)
        self.dump_to_file(self.test_plan)
        return True

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
        # self.iot_all = self.build_characterization_list_full()
        # self.iot_all.print_all()
        # self.user_characterization()
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
        for i in range(1, 5):
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
        for layer_num in range(1, 6):
            for item in iot_group.layers[layer_num-1]:
                value = iot_group.layers[layer_num-1][item]
                print item, value
                # check all list value, just one need to be found
                value_flag = False
                for v in value:
                    if self.iot_user.find_tuple(_char=(item,v), _layers=[layer_num-1]):
                        value_flag = True
                if not value_flag:
                    return False
        return True
