import json
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from lang.language_support import get_executed_function_body, get_executed_class_method


async def tool__get_function_body(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    executed_function_body = get_executed_function_body(
        run_context.context['project_name'],
        int(run_context.context['bug_id']),
        args['file_path'],
        args['function_name']
    )
    if executed_function_body is None:
        return "the function definition does not exist"
    return f"""
<function_body_with_coverage file_path={args['file_path']}>
{executed_function_body[0]}

<analysis>
- if the line begins with > then it was executed
- if the lines begins with ! then it was not executed
- if all the lines in the function begin with !, this funciton was never executed so ignore it
</analysis>

</function_body_with_coverage>
"""


async def tool__get_class_method_body(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    executed_class_method = get_executed_class_method(
        run_context.context['project_name'],
        int(run_context.context['bug_id']),
        args['file_path'],
        args['class_name'],
        args['method_name']
    )
    if executed_class_method is None:
        return "the class method definition does not exist"
    return executed_class_method[0]

function_explanation_tool = FunctionTool(
    name="get_function_body_tool",
    description="returns a function body for a given function name and file path",
    params_json_schema={
        "type": "object",
        "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path in which the function is housed in"
                },
            "function_name": {
                    "type": "string",
                    "description": "the name of the function that we need the function body for"
                }
        }
    },
    on_invoke_tool=tool__get_function_body,
)

class_method_explanation_tool = FunctionTool(
    name="get_class_method_body_tool",
    description="returns a class method body for a given class name, its method name and the module path",
    params_json_schema={
        "type": "object",
        "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path in which the class is housed in"
                },
            "method_name": {
                    "type": "string",
                    "description": "the name of the class method that we need the body for"
                },
            "class_name": {
                    "type": "string",
                    "description": "the name of the class that has the method"
                }
        }
    },
    on_invoke_tool=tool__get_class_method_body
)
