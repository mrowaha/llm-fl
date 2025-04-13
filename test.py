from lang.language_support import get_executed_function_body, get_class_method, get_executed_class_method

project = 'thefuck'
bug = 1
filename = 'thefuck/types.py'
functionname = '__init__'

print(get_class_method(project, bug, filename, 'Rule', functionname)[0])
print('///////////////////////////////')
print(get_executed_class_method(
    project, bug, filename, 'Rule', functionname)[0])
