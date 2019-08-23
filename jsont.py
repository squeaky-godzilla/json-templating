#!/usr/bin/env python3

"""
Simplistic JSON Templating
"""

__author__ = "Vitek Urbanec"
__version__ = "0.1.0"
__license__ = "MIT"

import json
import sys
import re
import argparse

MSG = '''
jsont <input.json> <params.json>
The json string template syntax is: {{variableName}}. The replace only happens in JSON string values.\n 
The left braces can be escaped by {{lb}}. The right braces do not need to be escaped. "lb" cannot be used as a variable name.\n 
The application writes the result to stdout.\n

'''

# argparser is configured to allow for positional arguments
# and also flags

PARSER = argparse.ArgumentParser(usage=MSG)
PARSER.add_argument('input_json_file')
PARSER.add_argument('params_json_file')
PARSER.add_argument('-r', action='store_true', help='recursive variables')
try:
    ARGS = PARSER.parse_args()
except:
    exit(1)

if ARGS.r:
    RECURSIVE_VARS_MODE = True
else:
    RECURSIVE_VARS_MODE = False

INPUT_JSON = ARGS.input_json_file
PARAMS_JSON = ARGS.params_json_file

# list of reserved variables

RESERVED_VARS = {
    "lb":"{",
}

# loading the JSON into Python dict

try:
    with open(INPUT_JSON, 'r') as input_json_file:
        INPUT_DICT = json.load(input_json_file)

    with open(PARAMS_JSON, 'r') as params_json_file:
        PARAMS_DICT = json.load(params_json_file)
except Exception as exc:
    print(exc, file=sys.stderr)
    exit(2)

def validate_key(key_arg):
    """ function to validate that the params key is a valid word """
    valid_key_pattern = re.compile(r"\w+$")
    try:
        valid_key_pattern.match(key_arg).group(0)
        return True
    except AttributeError:
        return False

for k, v in PARAMS_DICT.items():
    if k in RESERVED_VARS.keys() or not validate_key(k):
        exit(3)



# add reserved variables to the params_dictionary

PARAMS_DICT.update(RESERVED_VARS)



def replace_variable(target, variable_arg, params_dict_arg):
    """function to enable resolving the pointer variables"""
    if '{{%s}}' % variable_arg == params_dict_arg[variable_arg]:
        exit(4)
    else:
        output = target.replace('{{%s}}' % variable_arg, params_dict_arg[variable_arg])
    return output

def params_re_str(string_arg, params_dict_arg):
    """regexp to enable the single-pass templating (to avoid sequential replacement)
       using the lambda function"""
    replace_dict = dict((re.escape('{{%s}}' % k), v) for k, v in params_dict_arg.items())
    pattern = re.compile("|".join(replace_dict.keys()))
    string_output = pattern.sub(lambda m: replace_dict[re.escape(m.group(0))], string_arg)
    return string_output

def template_list(list_arg, params_dict_arg):
    """# function to enable templating a list"""
    output_list = list_arg
    for index, item in enumerate(output_list):
        if isinstance(item, str):
            output_list[index] = params_re_str(item, params_dict_arg)
        elif isinstance(item, dict):
            output_list[index] = template_dict(item, params_dict_arg)
        elif isinstance(item, list):
            output_list[index] = template_list(item, params_dict_arg)
    return output_list

def template_dict(input_dict_arg, params_dict_arg):
    """function to enable templating a dictionary"""
    output_dict = input_dict_arg
    for key, value in output_dict.items():
        if isinstance(value, str):
            output_dict[key] = params_re_str(value, params_dict_arg)
        elif isinstance(value, dict):
            output_dict[key] = template_dict(value, params_dict_arg)
        elif isinstance(value, list):
            output_dict[key] = template_list(value, params_dict_arg)

    return output_dict

# with recursive mode enabled, a new params_dict is generated with resolved variable pointers

if RECURSIVE_VARS_MODE:

    RESOLVED_D = PARAMS_DICT

    for variable in list(PARAMS_DICT):
        for key, value in RESOLVED_D.items():
            RESOLVED_D[key] = replace_variable(value, variable, PARAMS_DICT)

    PARAMS_DICT = RESOLVED_D

def main():
    """main function"""
    output = template_dict(INPUT_DICT, PARAMS_DICT)
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
    