# !usr/bin/python
from accessories import switch_case
from time import sleep
from accessories import ToolBasic
from sys import path
from TPB import TPBMain
from TM import TMMain


class Main(object):
    def __init__(self):
        self.test_plan = TPBMain.TestPlan('')


if __name__ == '__main__':
    main = Main()
    print ("Hello and Welcome to TestBundleExpress:\nThe ultimate penetration tests package for IoT developers")
    while 1:
        menu_path = path[0]+"/accessories/MainMenu.txt"
        f = open(menu_path,'r')
        print f.read()
        x = raw_input()
        for case in switch_case.switch(x):
            if case('1'):
                Builder = TPBMain.TPB()
                Builder.intro_menu()
            elif case('2'):
                test_manager = TMMain.TM()
                test_manager.menu()
            elif case('3'):
                ToolBasic.ToolBasic.list_group()
            elif case('4'):
                print ("Final Project @ Yuppi\n")
            elif case('5'):
                print ("Exists Program...")
                exit(1)
            else:
                print ("Please Enter a Valid Entry!!!\n")
                break