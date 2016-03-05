#
# The Parameter Gatherer (PG) is a key feature in the application architecture
# It is responsible to collect the necessary parameters for the groups.
# First it scan the groups Param.txt files and arrange a list of all required
# Parameters (some groups ask for the same parameters, often) the it start
# collecting the parameters both by autonomous SW and user input

# self.raw_parameter structure : cell#0 parameter name ; cell#1 type ; cell#2 Question ; cell #3 Auto? ; cell#4 external tool
# self.parameter structure: cell#0 parameter name ; cell#1 parameter value
import PGMenu
import PGTPC
import PGGather


class PG(object):

    def __init__(self):
        self.raw_parameters = []
        self.parameters = []
        self.group_list = []
        self.Menu = True

    def intro_menu(self):
        PGMenu.menu()
        self.Menu = True

    def gather_param_demand(self):
        """
         This method get a list of groups and return their parameter demand
        :param self:
        :return: list of parameter requests divided into field
        """
        self.raw_parameters = PGGather.parameter_parser(PGGather.gather_param_demand(self.group_list))

    def gather_question_parameter(self):
        self.parameters = PGGather.gather_question_parameter(self.raw_parameters)

    def check_group_tools_valid(self,group):
        checker = PGTPC.TPC()


# For Debug purposes
if __name__ == "__main__":
    groups = ["DOS"]
    param_obj = PG()
    param_obj.group_list = groups
    param_obj.gather_param_demand()
    param_obj.gather_question_parameter()
    a=5;