#
# The Parameter Gatherer (PG) is a key feature in the application architecture
# It is responsible to collect the necessary parameters for the groups.
# First it scan the groups Param.txt files and arrange a list of all required
# Parameters (some groups ask for the same parameters, often) the it start
# collecting the parameters both by autonomous SW and user input
# self.raw_parameter structure :
#       cell#0 parameter name ; cell#1 type ; cell#2 Question ; cell #3 Auto? ; cell#4 external tool
# self.parameter structure: cell#0 parameter name ; cell#1 parameter value
import xml.etree.ElementTree as Et
from Core.Base import ToolBasic


class PG(ToolBasic.ToolBasic):

    def __init__(self):
        ToolBasic.ToolBasic.__init__(self)
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
        my_path = self.path_abs() + "Groups\\"
        parameter_demand_list = []
        for name in self.group_list:
            data_file = my_path+name+"\data.xml"
            tree = Et.parse(data_file)
            root = tree.getroot()
            for element in root:
                if element.tag == "parameters":
                    for parameter in element:
                        parameter_line = [parameter.tag, parameter.attrib]
                        if self.parameter_demand_list_exists(parameter_demand_list,parameter_line): # already exists
                            pass
                        else:
                            parameter_demand_list.append(parameter_line)
        print parameter_demand_list
        self.parsed_parameters = parameter_demand_list

    @staticmethod
    def parameter_demand_list_exists(_demand_list, _line):
        for item in _demand_list:
            if item[0] == _line[0]:
                return True
        return False


    def insert_default_values(self):
        # insert default values
        for item in self.parsed_parameters:
             if 'tool' not in item[1]:
                item[1]['tool'] = 'non'

    @staticmethod
    def parse_param(param_list):
        parsed_param = {}
        for item in param_list:
            parsed_param[item[0]] = item[1]
        return parsed_param

    def gather_question_parameter(self):
        parameters_values = []
        for item in self.parsed_parameters:
            if item[1]['tool'] == 'non':
                parameters_values.append([item[0], raw_input(item[1]['question'])])
            else:
                self.gather_tool_parameter(item)
        self.parameters = self.parse_param(parameters_values)

    def gather_tool_parameter(self, _module_name='sys', _class_name='path'):
        module_name, class_name = self.dynamic_importer(_module_name, _class_name)




