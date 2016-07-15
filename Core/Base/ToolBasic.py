# This "virtual" class in a bunch of common method intended to used by all tools
from os import path, listdir
from sys import path as sys_path
import pickle
import xml.etree.ElementTree as Et
import imp


class ToolBasic(object):
    def __init__(self):
        self.path_project = self.path_abs()
        self.Et = Et

    @staticmethod
    def open_file(filename):
        f = open(filename, 'r')
        return f

    @staticmethod
    def list_all_groups():
        my_path = sys_path[0]+"\Groups"
        print my_path
        group_list = listdir(my_path)
        group_list.remove("parameters")
        group_list.remove("__init__.py")
        return group_list

    @staticmethod
    def list_group_tests():
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
        test_plan_file = open("Core/Base/TestPlan", 'rb')
        try:
            temp_test_plan = pickle.load(test_plan_file)
        except EOFError:
            temp_test_plan = TestPlan([])
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

    def dynamic_importer(name, class_name):
        """
        Dynamically imports modules / classes
        """
        try:
            fp, pathname, description = imp.find_module(name)
        except ImportError:
            print "unable to locate module: " + name
            return (None, None)

        try:
            example_package = imp.load_module(name, fp, pathname, description)
        except Exception, e:
            print e

        try:
            myclass = imp.load_module("%s.%s" % (name, class_name), fp, pathname, description)
            print myclass
        except Exception, e:
            print e

        return example_package, myclass

    def get_xml_root(self, _group="Ping"):
        my_path = self.path_abs() + "Groups\\"
        root_path = my_path + _group + "\data.xml"
        tree = Et.parse(root_path)
        root = tree.getroot()
        return root


class TestPlan(object):
    def __init__(self, some_list):
        self.group_list = some_list

    def set_list(self, _list):
        self.group_list = _list

    def get_list(self):
        return self.group_list


class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """ returns Returns the match method once then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


# For debug purposes
if __name__ == "__main__":
    dd = ToolBasic()
    print dd.path_project
    _temp_list = [["hagai", "302", "hello"], ["yaron", "201", "bye"]]
    ToolBasic.print_list(_temp_list)
