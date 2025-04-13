from lang.language_support import get_executed_function_body

project = 'thefuck'
bug = 1
filename = 'thefuck/types.py'
functionname = '__init__'

print(get_executed_function_body(project, bug, filename, functionname)[0])
