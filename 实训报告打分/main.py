import datetime
import threading
from copy import deepcopy

import env
import os
import json
import pandas as pd
from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import Send, Command
from tools import extract_text_from_docx
from state import State
from scoring_node import scoring
from evaluator import evaluator

EVALUATE_COUNT = int(os.getenv('EVALUATE_COUNT'))


class WorkerState(TypedDict):
    name: str
    dir_path: str


def scan_dir(state: State):
    sends = []
    for entry in os.scandir(state['scan_dir_path']):
        if entry.is_dir():
            stu_name = entry.name
            sends.append(Send('find_report', {'name': stu_name, 'dir_path': entry.path}))
    return sends


def _find_docx(dir_path):
    for entry in os.scandir(dir_path):
        if entry.is_dir():
            docx_path = _find_docx(entry.path)
            if docx_path is not None:
                return docx_path
        if os.path.splitext(entry.name)[-1] in ['.docx', '.doc']:
            return entry.path


def find_report(state: WorkerState):
    docx_path = _find_docx(state['dir_path'])
    assert docx_path is not None, f'No docx file found in: {state["dir_path"]}'
    return {'meta_data': [(state["name"], docx_path)]}


def ready_to_score(state: State):
    meta_data_copy = deepcopy(state['meta_data'])
    return {'meta_data_copy': meta_data_copy}


def extract_docx_text(state: State):
    meta_data = state['meta_data_copy']
    assert len(meta_data) > 0, '.docx file not found'
    name, docx_path = meta_data.pop(0)
    json_str = extract_text_from_docx.invoke({'docx_path': os.path.normpath(os.path.abspath(docx_path))})
    doc_content = json.loads(json_str)['content']
    return {'meta_data_copy': meta_data, 'current_name': name, 'current_doc_content': doc_content}


def continue_eval_route(state: State):
    if state['current_eval_count'] < EVALUATE_COUNT:
        return Command(goto='scoring', update={'current_eval_count': state['current_eval_count']})
    df_data = deepcopy(state['data_frame_datas'])
    df_data['name'].append(state['current_name'])
    df_data['score'].append(state['current_score'])
    df_data['remark'].append(state['current_remark'])
    timestamp = datetime.datetime.now().timestamp()
    thread = threading.Thread(
        target=lambda data: pd.DataFrame(data).to_csv(f'dist/result_{timestamp}.csv', index=False, encoding='gbk'),
        args=[df_data])
    thread.start()
    thread.join()
    if len(state['meta_data_copy']) > 0:
        return Command(goto='extract_docx_text', update={'current_eval_count': 0, 'data_frame_datas': df_data})
    else:
        return Command(goto=END)


builder = StateGraph(State)
builder.add_node('find_report', find_report)
builder.add_node('ready_to_score', ready_to_score)
builder.add_node('extract_docx_text', extract_docx_text)
builder.add_node('scoring', scoring)
builder.add_node('evaluator', evaluator)
builder.add_node('continue_eval_route', continue_eval_route)

builder.add_conditional_edges(
    START,
    scan_dir,
    ['find_report']
)
builder.add_edge('find_report', 'ready_to_score')
builder.add_edge('ready_to_score', 'extract_docx_text')
builder.add_edge('extract_docx_text', 'scoring')
builder.add_edge('scoring', 'evaluator')
builder.add_edge('evaluator', 'continue_eval_route')

graph = builder.compile()
print(graph.get_graph().draw_ascii())
config = {'recursion_limit': 1000}

chunks = graph.stream({'scan_dir_path': './assets', 'data_frame_datas': {'name': [], 'score': [], 'remark': []}},
                      config=config)
for chunk in chunks:
    print(chunk)
