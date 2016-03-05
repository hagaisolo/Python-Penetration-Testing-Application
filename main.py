# !usr/bin/python
from accessories import switch_case
from time import sleep
from accessories import GroupAndTestsLister
from sys import path
from TPB import TPBMain
from TPB import TestPlan
from TM import TMMain
import pickle


class Main(object):
    def __init__(self):
        self.test_plan = TestPlan.TestPlan('')


if __name__ == '__main__':
    main = Main()
    while 1:
        menu_path = path[0]+"/accessories/MainMenu.txt"
        f = open(menu_path,'r')
        print f.read()

        try:
            x = raw_input()
        except KeyboardInterrupt:
            print "Exit Program"
            exit(1)

        for case in switch_case.switch(x):
            if case('1'):
                Builder = TPBMain.TPB()
                Builder.intro_menu()
            elif case('2'):
                # Enters the TM - TestManager, if main.test_plan.group_list is empty returns
                test_plan_file = open("accessories/TestPlan", 'rb')
                main.test_plan = pickle.load(test_plan_file)
                if main.test_plan.group_list == '':
                    print ("no groups were selected...\n")
                    break
                test_plan_file.close()
                test_manager = TMMain.TM(main.test_plan)
                test_manager.gather_parameters()
                test_manager.run_tests()
            elif case('3'):
                GroupAndTestsLister.Lister()
            elif case('4'):
                print ("Final Project @ Yuppi\n")
            elif case('5'):
                print ("Exists Program...")
                exit(1)
            else:
                print ("Please Enter a Valid Entry!!!\n")
                break
            try:
                raw_input("\nPress any key to return to menu\n")
            except KeyboardInterrupt:
                print ("Exit Program...")
                exit(1)
        sleep(2)