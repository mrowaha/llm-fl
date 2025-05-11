localize_fault_prompt = """
You have a failing test and executed files in this test. You should go through the code, localize the fault
and explain your reasoning for the fault candidate. You should:
- Starting from the failing file, trace the execution by using function/class method explanations as needed
- Load those function/class method execution (tools available)
<restrictions>
- your file content searches are only restricted to the executed files provided to you.
- you must not make any assumptions of file paths. You must first study the import statements of the current file and then derive a file path of the definition you want.
- you will not immediately deduce the fault from the failing test. you must first go through files before reaching conclusion
- when loading file content from file path, you must specify the definitions (e.g. variables' names, functions' names, class' names) that you want to keep in the file content
</restrictions>
<output_format>
- you will give the name of the code hunk (variable, function, class) that you consider to be faulty
- your output will be of the following format
name: <faulty code hunk's name>
file: <faulty code hunk's file path>
explanation: <small explanation about why you consider this code hunk faulty>
</output_format>
""".strip()
