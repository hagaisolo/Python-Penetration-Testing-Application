# This is the Data Analyzer / Collector class
from accessories import ToolBasic
from accessories import switch_case


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
            for case in switch_case.switch(x):
                # Print the TPBHelp.txt document
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
        f = self.open_file("DA/help.txt")
        help_text = f.read()
        print help_text

    def display(self):
        print "Display tests data_log files:"
        my_path = self.path_abs() + "Groups\\"
        print self.test_plan.group_list
        for test in self.test_plan.group_list:
            print ("Display data for ___ %s ___ test:" % test)
            f = open(my_path+test+"\\data_log", 'r')
            print(f.read())
