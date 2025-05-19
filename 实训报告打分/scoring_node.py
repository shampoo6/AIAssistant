from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from pydantic import BaseModel, Field

from state import State
from zhipu_llm import llm as zhipu_ai
from spark_llm import llm as spark_ai
from ollama_llm import llm as ollama_ai
from template_reader import rules, scoring_template


class ScoringResult(BaseModel):
    """打分结果"""
    name: str = Field(description='学生姓名')
    score: float = Field(description='分数')
    remark: str = Field(description='评语')


_parser = PydanticOutputParser(pydantic_object=ScoringResult)
_output_format = _parser.get_format_instructions().replace('{', '{{').replace('}', '}}')

_output_fix_parser = OutputFixingParser.from_llm(
    llm=zhipu_ai,
    parser=_parser,
    max_retries=3,
    prompt=PromptTemplate.from_template('''
# 概述
你是一个数据修复工具，负责处理 json 转换的异常
# 应该输出的结构要求
{instructions}
# 原始输出数据
{completion}
# 异常信息
{error}
# 输出
请根据 `应该输出的结构要求`、`原始输出数据` 和 `异常信息` 尝试输出修复后的，符合要求的结果
请输出你修复后的结果:
''')
)


def scoring(state: State):
    prompt_template = ChatPromptTemplate.from_template(scoring_template)
    scoring_result = (prompt_template | spark_ai | _output_fix_parser).invoke({
        'rules': rules,
        'student_name': state['current_name'],
        'report': state['current_doc_content'],
        'suggestion': state.get('current_suggestion', '无'),
        'output_format': _output_format
    })
    return {'current_name': state['current_name'], 'current_score': scoring_result.score,
            'current_remark': scoring_result.remark}
