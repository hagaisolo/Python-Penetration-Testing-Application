# !usr/bin/python
# This feature is responsible for printing a list of all existing groups and tests
# currently at the TestBundle
# It list Group by swiping over directory name and list test according to group's
# Test.txt files which declare the group's tests. it does not validated existence
from os import listdir
from sys import path


class Lister(object):
    def __init__(self):
        mypath = path[0]+"\Groups"
        m = 0
        for name in listdir(mypath):
            m +=1
            print "Group %s - \"" % m + name + "\" - Include the following Tests:"
            str_temp = mypath + "\\" + name +"\Tests.txt"
            f = open(str_temp, 'r')
            file_temp = f.read()
            file_temp = file_temp.split()
            j = file_temp.index("List:")
            for i in range (j+1,len(file_temp)):
                print file_temp[i]