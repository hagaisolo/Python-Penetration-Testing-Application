# This is the Data Analyzer / Collector class
# from Core.Base import switch_case
from Core.Base import ToolBasic

switch_case = ToolBasic.switch


class DA(ToolBasic.ToolBasic):
    def __init__(self):
        ToolBasic.ToolBasic.__init__(self)
        self.stats = 0
        self.test_plan = self.get_test_plan()
        self.dis = False
        self.loop_flag = True

    def menu(self):
        print "Welcome To The Data Analyzer / Collector Utility"
        print "The DA will Help Analyze and Parse the output data"
        print "\"Help\" for further instructions\n"
        while self.loop_flag:
            x = raw_input("Choose Action Help/Display/Process/List/Quit ")
            for case in switch_case(x):
                # Print the help.txt document
                if case('Help') or case('help'):
                    self.help_text()
                # Print A list of all available groups
                elif case('List'):
                    print self.test_plan.group_list
                # Display data
                elif case('Display'):
                    self.dis = True
                    self.display()
                # Process data
                elif case('Process'):
                    self.dis = False
                    self.display()
                # Quits the DC
                elif case('Quit'):
                    print "Exiting DA...\n"
                    self.loop_flag = False

    def help_text(self):
        print "Help Text Method"
        f = self.open_file("Core/DA/help.txt")
        help_text = f.read()
        print help_text

    def display_all(self):
        string = "Display tests data_log files:\n"
        my_path = self.path_abs() + "Groups/"
        string += str ( self.test_plan.group_list )
        for test in self.test_plan.group_list:
            string += ("Display data for ___ %s ___ test:\n" % test)
            f = open(my_path+test+"/data_log", 'r')
            string += f.read()
        return string

    def display(self, _group):
        string = "Display tests data_log files:\n"
        my_path = self.path_abs() + "Groups/"
        string += str ( _group )
        string += ("Display data for ___ %s ___ test:\n" % _group)
        f = open(my_path+_group+"/data_log", 'r')
        string += f.read()
        return string
