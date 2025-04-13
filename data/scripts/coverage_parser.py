"""
includes functions to get the executed files and the executed lines
must be executed from the data root folder
"""
import argparse
from pathlib import Path
import json
coverage_report_suffix = "coverage-report.json"
executed_lines_suffix = "executed-lines.json"
executed_files_suffix = "executed-files.json"


def get_executed_lines(project_name: str, bug_id: int) -> None:
    project_bug_dir = Path('.') / Path(project_name) / Path(str(bug_id))
    report_filepath = project_bug_dir / Path(coverage_report_suffix)
    result_filepath = project_bug_dir / Path(executed_lines_suffix)
    with open(report_filepath) as f:
        data = json.load(f)

    with open(result_filepath, "w") as f:
        files = {}
        for file, info in data.get("files", {}).items():
            executed = set(
                range(1, info["summary"]["num_statements"] + 1)) - set(info["missing_lines"])
            files[file] = sorted(executed)
        json.dump(files, f)


def get_executed_files(project_name: str, bug_id: int) -> None:
    project_bug_dir = Path('.') / Path(project_name) / Path(str(bug_id))
    report_filepath = project_bug_dir / Path(coverage_report_suffix)
    result_filepath = project_bug_dir / Path(executed_files_suffix)
    with open(report_filepath) as f:
        data = json.load(f)

    with open(result_filepath, "w") as f:
        files = []
        for file, info in data.get("files", {}).items():
            files.append(file)
        json.dump(files, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generate executed lines and executed files for a given project name and its bug id")

    parser.add_argument(
        "--project",
        type=str,
        required=True,
        help="project name"
    )

    parser.add_argument(
        "--bug",
        type=int,
        required=True,
        help="bug id"
    )

    args = parser.parse_args()
    get_executed_lines(args.project, args.bug)
    get_executed_files(args.project, args.bug)
