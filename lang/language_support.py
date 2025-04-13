import os
import dirs
import ast
import parso


def get_function_body(
    project_name: str, bug_id: int,
    file_path: str, function_name: str
):
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'source', file_path)
    with open(true_file_path, "r") as f:
        source = f.read()

    # Parse the file using AST
    tree = ast.parse(source, filename=true_file_path)

    # Find the function definition
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Use inspect to get source code from AST node
            return ast.get_source_segment(source, node)

    return None


def get_executed_function_body(
    project_name: str, bug_id: int,
    file_path: str, function_name: str
):
    project_dir = dirs.get_project_bug_dir(project_name, bug_id, 'data')
    true_file_path = os.path.join(
        str(project_dir.absolute()), 'annotation', file_path + ',cover'
    )

    with open(true_file_path, "r") as f:
        source = f.read()

    module = parso.parse(source)
    print(module.iter_funcdefs())
    for node in module.iter_funcdefs():
        if node.name.value == function_name:
            return node.get_code()

    return None


def get_class_source(
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
