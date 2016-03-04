# !/usr/bin/python
# The gather on demand function's input is a list of strings, each string is a name
# of a group to gather parameters for. The method scans the group's Param.txt files
# and collect a list of requested parameters with detail on each parameter according
# To Architecture Specification (4.2) on the format
import os
from sys import path
from accessories import Pathes


def gather_param_demand(group):
    my_path = Pathes.group()
    m = 0
    param_list = []
    for name in group:
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
    delete_duplication(param_list)
    return param_list


def delete_duplication(dup_list):
    limit = len(dup_list)-1
    for i in range(0, limit):
        for j in range(i+1, limit):
            if dup_list[j] == dup_list[i]:
                dup_list.remove(dup_list[j])
                limit -= 1


def parameter_parser(raw_param):
    line_list = []
    for line in raw_param:
        line = line.split('><')
        line_list.append(line)
    return line_list


def gather_question_parameter(parsed_param):
    param_list = []
    for i in range(len(parsed_param)):
        if parsed_param[i][3] == "NON":
            param_list.append((parsed_param[i][0], raw_input(parsed_param[i][2])))
    return param_list



#    -------for DEBUG purposes--------
if __name__ == '__main__':
    list_group = "Ping"
    param = gather_param_demand([list_group])
    param = parameter_parser(param)
    param_temp = gather_question_parameter(param)
    a=5;