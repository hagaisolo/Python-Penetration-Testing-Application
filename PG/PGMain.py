#
# The Parameter Gatherer (PG) is a key feature in the application architecture
# It is responsible to collect the necessary parameters for the groups.
# First it scan the groups Param.txt files and arrange a list of all required
# Parameters (some groups ask for the same parameters, often) the it start
# collecting the parameters both by autonomous SW and user input
import PGMenu
import PGTPC
import PGGather


class PG(object):

    def __init__(self):
        self.parameters = []
        self.group_list = []
        self.Menu = True

    def intro_menu(self):
        PGMenu.menu()
        self.Menu = True

    def gather_param_demand(self, groups): # This method get a list of groups and return their parameter demand
        self.group_list.append(groups)
        self.parameters = PGGather.gather_param_demand(self.group_list)

    def check_group_tools_valid(self,group):
        checker = PGTPC.TPC()
