from pathlib import Path
from typing import Literal
data_dir = Path(".") / Path("data")
preprocessed_dir = Path(".") / Path("preprocessed")


def get_project_bug_dir(project_name: str, bug_id: int, type: Literal["data", "preprocessed"]) -> Path:
    dir: Path = None
    if type == 'data':
        dir = data_dir / Path(project_name) / Path(str(bug_id))
    elif type == 'preprocessed':
        dir = preprocessed_dir / Path(project_name) / Path(str(bug_id))
    else:
        raise ValueError("unrecognized project dir type")

    if not dir.exists():
        raise NotADirectoryError

    return dir


def get_minified_annotations_folder(project_name: str, bug_id: int) -> Path:
    return data_dir / Path(project_name) / Path(str(bug_id)) / "minified_annotations"
