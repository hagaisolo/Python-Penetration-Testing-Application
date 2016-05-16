import xml.etree.ElementTree as Et
import os

group_list = ["Ping"]
if __name__ == "__main__":
    my_path = os.path.abspath("") + "\\Groups\\"
    param_list = []
    for name in group_list:
            data_file = my_path+name+"\data.xml"
            tree = Et.parse(data_file)
            root = tree.getroot()
            for element in root:
                if element.tag == "parameters":
                    for parameter in element:
                        parameter_line = [parameter.tag]
                        parameter_line.append(parameter.attrib)
                        param_list.append(parameter_line)

    parsed_parameters = param_list
    # insert default values
    for item in parsed_parameters:
        # if not item[1].has_key('tool'):
        if 'tool' not in item[1]:
            item[1]['tool'] = 'non'

    parameters_values = []
    for item in parsed_parameters:
        if item[1]['tool'] == 'non':
            parameters_values.append([item[0], raw_input(item[1]['question'])])
    parameters = parameters_values
