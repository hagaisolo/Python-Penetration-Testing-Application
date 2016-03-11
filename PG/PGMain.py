#
# The Parameter Gatherer (PG) is a key feature in the application architecture
# It is responsible to collect the necessary parameters for the groups.
# First it scan the groups Param.txt files and arrange a list of all required
# Parameters (some groups ask for the same parameters, often) the it start
# collecting the parameters both by autonomous SW and user input
# self.raw_parameter structure : cell#0 parameter name ; cell#1 type ; cell#2 Question ; cell #3 Auto? ; cell#4 external tool
# self.parameter structure: cell#0 parameter name ; cell#1 parameter value
from accessories import Pathes


class PG(object):

    def __init__(self):
        self.raw_parameters = []
        self.parsed_parameters = []
        self.parameters = []
        self.group_list = []
        self.Menu = True

    def intro_menu(self):
        print "Welcome To The PG"
        print "The PG Gather The Required Parameter To Run the Tests"
        print "\"Help\" for further instructions\n"
        self.Menu = True

    def gather_param_demand(self):
        my_path = Pathes.group()
        m = 0
        param_list = []
        for name in self.group_list:
            str_temp = my_path+name+"\Param.txt"
            try:
                f = open(str_temp, 'r')

                temp_line = f.readline()
                while temp_line != "List:\n":
                    temp_line = f.readline()
                index = 0
                while True:
                    param_list.append(f.readline())
                    if param_list[index] == '':
                        break
                    index += 1
            except ValueError:
                pass
        param_list.pop()
        self.delete_duplication(param_list)
        self.raw_parameters = param_list

    @staticmethod
    def delete_duplication(dup_list):
        limit = len(dup_list)-1
        for i in range(0, limit):
            for j in range(i+1, limit):
                if dup_list[j] == dup_list[i]:
                    dup_list.remove(dup_list[j])
                    limit -= 1

    def parameter_parser(self):
        line_list = []
        for line in self.raw_parameters:
            line = line.split('><')
            line_list.append(line)
        self.parsed_parameters = line_list

    def gather_question_parameter(self):
        param_list = []
        for i in range(len(self.parsed_parameters)):
            if self.parsed_parameters[i][3] == "NON":
                param_list.append((self.parsed_parameters[i][0], raw_input(self.parsed_parameters[i][2])))
        self.parameters = param_list

# For Debug purposes
if __name__ == "__main__":
    groups = ["DOS"]
    param_obj = PG()
    param_obj.group_list = groups
    param_obj.gather_param_demand()
    param_obj.gather_question_parameter()
    a=5;