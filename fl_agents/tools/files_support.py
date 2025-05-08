import os
import pathlib
import json
from agents.tool import FunctionTool
from agents.run_context import RunContextWrapper
from dirs import get_minified_annotations_folder, get_project_bug_dir


async def tool__load_file(run_context: RunContextWrapper, str_args) -> str:
    args = json.loads(str_args)
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']
    file = args['file_path']
    minified_annotations_dir = get_minified_annotations_folder(
        project_name, bug_id)

    file_content: str = ""
    with open(
        os.path.join(str(minified_annotations_dir), file+',cover')
    ) as f:
        file_content = f.read()

    return f"""
    <file_executed_content file={args['file_path']}>
    {file_content}
    </file_executed_content>
    """


async def tool__load_executed_files(run_context: RunContextWrapper, args) -> str:
    project_name = run_context.context['project_name']
    bug_id = run_context.context['bug_id']

    bug_executed_files_path = get_project_bug_dir(
        project_name, bug_id, 'data') / pathlib.Path('executed-files.json')

    executed_files = []
    with open(bug_executed_files_path, 'r') as f:
        executed_files = json.load(f)

    return f"""
    <executed_files>
    {executed_files}
    </executed_files>
    """

file_content_tool = FunctionTool(
    name="get_file_content",
    description="gets the file content specified by the file path",
    params_json_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "file path to get the file content of"
                    }
                }
    },
    on_invoke_tool=tool__load_file
)
