import json
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from lang.language_support import get_executed_function_body, get_executed_class_method
language_support_model_id = 'qwen2.5-coder:7b'
language_support_model = OpenAIChatCompletionsModel(
    model=language_support_model_id,
    openai_client=AsyncOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama")
)


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
    return executed_function_body[0]


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
    on_invoke_tool=tool__get_function_body
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
),

function_explanation_agent = Agent(
    name="Function Explanation Agent",
    model=language_support_model,
    handoff_description="""
    will take a query for a function name and return a detailed explanation
    of the function and its execution in the failing test
    """,
    tools=[function_explanation_tool]
)

class_method_explanation_agent = Agent(
    name="Class Method Explanation Agent",
    model=language_support_model,
    handoff_description="""
    will take a query for a class name and its class method and returns a detailed
    explanation of the class method and its execution in the failing test
    """,
    tools=[class_method_explanation_tool]
)
