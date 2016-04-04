# This "virtual" class in a bunch of common method intended to used by all tools
from os import path, listdir, getcwd
from sys import path as sys_path


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
        _list_len = len(_list)
        _list_tuple_len = len(_list[0])
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


# For debug purposes
if __name__ == "__main__":
    dd = ToolBasic()
    print dd.path_project
    _temp_list = [["hagai","302","hello"],["yaron","201","bye"]]
    ToolBasic.print_list(_temp_list)