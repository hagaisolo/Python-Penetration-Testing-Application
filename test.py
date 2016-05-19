import xml.etree.ElementTree as Et
import os
import imp
import nmap

group_list = ["Ping"]


def dynamic_importer(name, class_name):
    """
    Dynamically imports modules / classes
    """
    try:
        fp, pathname, description = imp.find_module(name)
    except ImportError:
        print "unable to locate module: " + name
        return (None, None)

    try:
        example_package = imp.load_module(name, fp, pathname, description)
    except Exception, e:
        print e

    try:
        myclass = imp.load_module("%s.%s" % (name, class_name), fp, pathname, description)
        print myclass
    except Exception, e:
        print e

    return example_package, myclass


if __name__ == "__main__":
    """
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
    """
    tool_list = []
    my_path = os.path.abspath("") + "\\Groups\\"
    for item in group_list:
            root_path = my_path + item + "\data.xml"
            tree = Et.parse(root_path)
            root = tree.getroot()
            for element in root:
                if element.tag == "tools":
                    for tool in element:
                        tool_list.append(tool)
    name = tool_list[0].tag

    md, cl = dynamic_importer(name, name)
    print md, cl
    scanner = md.PortScanner()
    scanner.scan()

    # scanner = nmap.PortScanner()
    # scanner.scan()
