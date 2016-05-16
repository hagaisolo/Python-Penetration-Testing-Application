# This "virtual" class in a bunch of common method intended to used by all tools
from os import path, listdir
from sys import path as sys_path
import pickle
import xml.etree.ElementTree as Et


class ToolBasic(object):
    def __init__(self):
        self.path_project = self.path_abs()

    @staticmethod
    def open_file(filename):
        f = open(filename, 'r')
        return f

    @staticmethod
    def list_all_groups():
        my_path = sys_path[0]+"\Groups"
        groups = []
        for name in listdir(my_path):
            if name == "parameters" or name == "__init__.py":
                continue
            groups.append(name)
        return groups

    @staticmethod
    def list_group():
        my_path = sys_path[0]+"\Groups"
        m = 0
        for name in listdir(my_path):
            if name == "parameters" or name == "__init__.py":
                continue
            m += 1
            print "Group %s - \"" % m + name + "\" - Include the following Tests:"
            str_temp = my_path + "\\" + name + "\Tests.txt"
            f = open(str_temp, 'r')
            file_temp = f.read()
            file_temp = file_temp.split()
            j = file_temp.index("List:")
            for i in range(j+1, len(file_temp)):
                print file_temp[i]

    @staticmethod
    def path_abs():
        path_access = path.abspath("main.py")
        index = path_access.index("main")
        path_project = path_access[0:index:1]
        return path_project

    @staticmethod
    def print_list(_list):
        for item in _list:
            for _sub_item in item:
                print _sub_item + ' , ',
            print '\n'

    @staticmethod
    def check_is_group_exists(group):
        my_path = sys_path[0]+"\Groups"
        for name in listdir(my_path):
            if name == group:
                return True
        return False

    @staticmethod  # consider moving up to utilities
    def get_test_plan():
        test_plan_file = open("accessories/TestPlan", 'rb')
        temp_test_plan = pickle.load(test_plan_file)
        if temp_test_plan.group_list == '':
                print ("no groups were selected...\n")
        test_plan_file.close()
        return temp_test_plan

    @staticmethod
    def delete_duplication(dup_list):
        return list(set(dup_list))

    def get_tool_demand(self, _test_plan):
        my_path = self.path_abs() + "Groups\\"
        tool_list = []
        for item in _test_plan.get_list():
            root_path = my_path + item + "\data.xml"
            tree = Et.parse(root_path)
            root = tree.getroot()
            for element in root:
                if element.tag == "tools":
                    for tool in element:
                        tool_list.append(tool.tag)
        return tool_list

# For debug purposes
if __name__ == "__main__":
    dd = ToolBasic()
    print dd.path_project
    _temp_list = [["hagai", "302", "hello"], ["yaron", "201", "bye"]]
    ToolBasic.print_list(_temp_list)
