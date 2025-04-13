import os
import dirs
import ast
from typing import Tuple, Optional

Lines = Tuple[int, int]


def get_function_body(
    project_name: str, bug_id: int,
    file_path: str, function_name: str
) -> Optional[Tuple[str, Lines]]:
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'source', file_path)
    with open(true_file_path, "r") as f:
        source = f.read()

    # Parse the file using AST
    tree = ast.parse(source, filename=true_file_path)

    # Find the function definition with decorators
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Find the starting line: if there are decorators, use the first one
            if node.decorator_list:
                start_line = min(
                    decorator.lineno for decorator in node.decorator_list)
            else:
                start_line = node.lineno

            # Extract lines from start_line to end_lineno (inclusive)
            source_lines = source.splitlines()
            function_lines = source_lines[start_line - 1: node.end_lineno]
            return ('\n'.join(function_lines), (start_line, node.end_lineno))

    return None


def get_executed_function_body(
    project_name: str, bug_id: int,
    file_path: str, function_name: str
) -> Optional[Tuple[str, Lines]]:
    function_body = get_function_body(
        project_name, bug_id, file_path, function_name)

    if function_body is None:
        return None

    start_line, end_line = function_body[1]

    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'annotation', file_path+',cover')

    executed_body: Optional[list[str]] = None
    with open(true_file_path, "r") as f:
        lines = f.readlines()
        executed_body = lines[start_line - 1:end_line]
    if executed_body is not None:
        return (''.join(executed_body), (start_line, end_line))
    return None


def get_class_body(
    project_name: str, bug_id: int,
    file_path: str, class_name: str
):
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'source', file_path)
    with open(true_file_path, "r") as f:
        source = f.read()
    tree = ast.parse(source, filename=true_file_path)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return ast.get_source_segment(source, node)
    return None


def get_class_method(
    project_name: str, bug_id: int,
    file_path: str, class_name: str,
    method_name: str
) -> Tuple[str, Lines] | None:
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'source', file_path)
    with open(true_file_path, "r") as f:
        source = f.read()

    tree = ast.parse(source, filename=true_file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == method_name:
                    # Determine the start line, including decorators
                    if child.decorator_list:
                        start_line = min(
                            decorator.lineno for decorator in child.decorator_list)
                    else:
                        start_line = child.lineno

                    source_lines = source.splitlines()
                    method_lines = source_lines[start_line -
                                                1: child.end_lineno]
                    return ('\n'.join(method_lines), (start_line, child.end_lineno))

    return None


def get_executed_class_method(
    project_name: str, bug_id: int,
    file_path: str, class_name: str,
    method_name: str
) -> Optional[Tuple[str, Lines]]:
    method = get_class_method(
        project_name, bug_id, file_path, class_name, method_name)

    if method is None:
        return None

    start_line, end_line = method[1]

    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'annotation', file_path+',cover')

    executed_body: Optional[list[str]] = None
    with open(true_file_path, "r") as f:
        lines = f.readlines()
        executed_body = lines[start_line - 1:end_line]
    if executed_body is not None:
        return (''.join(executed_body), (start_line, end_line))
    return None


def extract_imports(
    project_name: str, bug_id: int,
    file_path: str
):
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'source', file_path)
    with open(true_file_path, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    import_nodes = [node for node in tree.body if isinstance(
        node, (ast.Import, ast.ImportFrom))]
    return '\n'.join(ast.unparse(node) for node in import_nodes)
