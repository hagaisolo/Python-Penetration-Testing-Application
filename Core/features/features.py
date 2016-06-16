import pickle

__name__ = "core_get_parameters"


def core_get_parameters():
    """
    this function get the parameter from the pickle file.
    :return: Dictionary of parameters
    """
    param_file = open('Groups//parameters', 'rb')
    param_list = pickle.load(param_file)
    param_file.close()
    return param_list
