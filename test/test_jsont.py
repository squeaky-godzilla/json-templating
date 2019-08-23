import pytest
import subprocess
import os
import json

# def test_stage_1():
#     with open("./stage_1/output.json", 'r') as output_json_file:
#         expected_output = json.load(output_json_file)
#     output = os.popen('python ../jsont.py ./stage_1/input.json ./stage_1/params.json').read()
#     output = json.loads(output)
#     assert output == expected_output

def test_stage_1_subprocess():
    with open("./stage_1/output.json", 'r') as output_json_file:
        expected_output = json.load(output_json_file)
    child = subprocess.Popen(['python', '../jsont.py', './stage_1/input.json', './stage_1/params.json'], stdout=subprocess.PIPE)
    output = json.loads(child.stdout.read())
    assert output == expected_output

# def test_stage_2_recursive_on():
#     with open("./stage_2/output.json", 'r') as output_json_file:
#         expected_output = json.load(output_json_file)
#     output = os.popen('python ../jsont.py ./stage_2/input.json ./stage_2/params.json -r').read()
#     output = json.loads(output)
#     assert output == expected_output

def test_stage_2_recursive_on_subprocess():
    with open("./stage_2/output.json", 'r') as output_json_file:
        expected_output = json.load(output_json_file)
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './stage_2/params.json', '-r'], stdout=subprocess.PIPE)
    output = json.loads(child.stdout.read())
    assert output == expected_output

# def test_stage_2_recursive_off():
#     with open("./stage_2/output_recursive_off.json", 'r') as output_json_file:
#         expected_output = json.load(output_json_file)
#     output = os.popen('python ../jsont.py ./stage_2/input.json ./stage_2/params.json').read()
#     output = json.loads(output)
#     assert output == expected_output

def test_stage_2_recursive_off_subprocess():
    with open("./stage_2/output_recursive_off.json", 'r') as output_json_file:
        expected_output = json.load(output_json_file)
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './stage_2/params.json'], stdout=subprocess.PIPE)
    output = json.loads(child.stdout.read())
    assert output == expected_output

def test_general_syntax_exitcode_1():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './stage_2/params3.json', './stage_2/input.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 1


def test_unable_to_load_nonexistent_file_exitcode_2():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './stage_2/params3.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 2

def test_unable_to_load_params_invalid_json_exitcode_2():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './additional/invalid_json_params.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 2

def test_unable_to_load_input_invalid_json_exitcode_2():
    child = subprocess.Popen(['python', '../jsont.py', './additional/invalid_json_input.json', './stage2/params.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 2

def test_params_lb_escape_exitcode_3():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './additional/lb_variable.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 3

def test_params_params_invalid_key_exitcode_3():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './additional/invalid_key_params.json'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 3

def test_params_cyclical_reference_exitcode_4():
    child = subprocess.Popen(['python', '../jsont.py', './stage_2/input.json', './additional/cref_variable.json', '-r'])
    streamdata = child.communicate()[0]
    exitcode = child.returncode
    assert exitcode == 4

def test_input_unknown_var():
    child = subprocess.Popen(['python', '../jsont.py', './additional/unknown_variable_input.json', './stage_2/params.json'], stdout=subprocess.PIPE)
    output = child.stdout.read()
    assert "{{unknown}}" in str(output)

