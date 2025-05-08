localize_fault_prompt = """
<your role>
You have a failing test and executed files in this test. You should go through the code, localize the fault
and explain your reasoning for the fault candidate. You should:
- Starting from the failing file, trace the execution across executed files by using function/class method explanations as needed
- Load those function/class method execution (tools available)
You can only trace the files within the executed files.
You may need to look into other executed files to localize the fault
<example_tracing>
if you believe that a function might be responsible for the fault, use the imports of the file you are considering at the moment
to fetch the details of that functions. You can recursively do this until you localize the fault
</example_tracing>
</your role>
""".strip()
