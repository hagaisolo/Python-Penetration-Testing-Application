# menu method for TPB class
from accessories import switch_case
from accessories import GroupAndTestsLister
from sys import path
from TestPlan import TestPlan
import pickle


def menu():
    print "Welcome To The TPB"
    print "The TPB will Help You Build The Most Suitable Test Design"
    print "\"Help\" for further instructions\n"
    loop_flag = True
    while loop_flag:
        x = raw_input()
        for case in switch_case.switch(x):
            if case('Help'):
                help_text()
            elif case('List'):
                GroupAndTestsLister.Lister()
            elif case('Full'):
                pass # Run full tests - all groups
            elif case('Single'):
                group = raw_input("Please Enter Group Name To Execute\n")
                test_plan = TestPlan(group)
                test_plan_file = open("", 'wb')
                pickle.dump(test_plan,test_plan_file)
            elif case('Quit'):
                print "Exiting TPB...\n"
                loop_flag = False
            elif case('Custom'):
                # creating a custom test plan
                print ("This option is not supported yet...\n")
            else:
                pass


def help_text():
    file_str = path[0] + "\TPB\TPBHelp.txt"
    f = open(file_str,'r')
    print f.read()

