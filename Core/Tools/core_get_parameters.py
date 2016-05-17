import pickle

__name__ = "core_get_parameters"

def parse_param(param_list):
    parsed_param = {}
    for item in param_list:
        parsed_param[item[0]] = item[1]
    return parsed_param

def core_get_parameters():
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return parse_param(param_list)
