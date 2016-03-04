# This is the TPC - Tool Presence Checker file.
# The TPC is responsible to compare between group's tool demands and tool presence at host computer.
# The tool extract to group demand from the Req_Tools.txt files and compare them to the
# Presence_Tool.txt file located in accessories.
from sys import path


class TPC(object):
    def __init__(self):
        self.tool_list = []
        self.tool_presence_list = []
        self.bad_syntax_letters = ["\n"]

    def get_tool_req(self, group):
        """ This method retrieves the group requested tools in a list format """
        my_path = path[0]+"/../Groups/"+group+"/Req_tools.txt"
        f = open(my_path, 'r')
        try:
            temp_line = f.readline()
            while temp_line != "List:\n":
                temp_line = f.readline()
            index = 0
            while True:
                self.tool_list.append(f.readline())
                if self.tool_list[index] == '':
                    break
                index += 1
        except ValueError:
                pass
        self.delete_duplication()

    def delete_duplication(self):
        """ This method delete duplication in a list """
        limit = len(self.tool_list)-1
        for i in range(0, limit):
            for j in range(i+1, limit):
                if self.tool_list[j] == self.tool_list[i]:
                    self.tool_list.remove(self.tool_list[j])
                    limit -= 1
        self.tool_list.remove(self.tool_list[-1])

    def get_presence_list(self):
        """ This method retrieves the present tools list in a list format """
        my_path = path[0]+"/../accessories/Tool_Presence_List.txt"
        f = open(my_path, 'r')
        try:
            temp_line = f.readline()
            while temp_line != "List:\n":
                temp_line = f.readline()
            index = 0
            while True:
                self.tool_presence_list.append(f.readline())
                if self.tool_presence_list[index] == '':
                    break
                index += 1
        except ValueError:
                pass

    def clear_syntax(self,list_curr):
        """ list_curr: This method clears unwanted char from the list for later possible lists comparison """
        for item in list_curr:
            for i in range(0,len(self.bad_syntax_letters)):
                repaired_item = item.replace(self.bad_syntax_letters[i],'')
                list_curr[list_curr.index(item)] = repaired_item

    def check_group_req(self):
        """ Compare between the previously obtained lists to see if the presence list contain all the tool
            demand of the group"""
        for item in self.tool_list:
            try:
                self.tool_presence_list.index(item)
                pass
            except ValueError:
                return False
        return True

"""#     -------for DEBUG purposes--------
if __name__ == '__main__':
    tester = TPC()
    tester.get_tool_req("BruteForce")
    tester.get_presence_list()
    print tester.tool_presence_list
    print tester.tool_list
    tester.clear_syntax(tester.tool_list)
    tester.clear_syntax(tester.tool_presence_list)
    print tester.tool_presence_list
    print tester.tool_list
    a = tester.check_group_req()
    print a
"""