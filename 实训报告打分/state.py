import operator
from typing import TypedDict, Annotated, List


class State(TypedDict):
    scan_dir_path: str
    meta_data: Annotated[list, operator.add]
    meta_data_copy: List[tuple]
    current_name: str
    current_doc_content: str
    current_score: float
    current_remark: str
    current_eval_count: int
    current_suggestion: str
    data_frame_datas: dict
