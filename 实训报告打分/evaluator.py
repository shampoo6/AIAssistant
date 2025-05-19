from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from state import State
from zhipu_llm import llm
# from spark_llm import llm
from template_reader import rules


def evaluator(state: State):
    prompt_template = ChatPromptTemplate.from_template("""# 背景介绍
用户是一位人工智能专业的实训课老师，课程结束后需要对学生上交的《实训报告》进行评分
用户已经给学生的实训报告给出了分数和评语，你需要给出一些修改建议
# 任务
你需要根据用户提供的 `评分规则` `实训报告` `分数` 和 `评语`，**对用户给的 `分数` 和 `评语` 提出批判性意见，并给出修改建议**
**请不要对 `实训报告` 提出修改建议**
# 评分规则
评分规则如下:

```markdown
{rules}
```
# 实训报告
## 学生姓名
{student_name}
## 报告内容
学生的实训报告内容如下:

```
{report}
```
# 分数
{score}
# 评语
{remark}
# 输出
请对用户给的 `分数` 和 `评语` 提出批判性意见，并给出修改建议，输出为字符串格式
你的输出:
""")
    suggestion = (prompt_template | llm | StrOutputParser()).invoke({
        'rules': rules,
        'student_name': state['current_name'],
        'report': state['current_doc_content'],
        'score': state['current_score'],
        'remark': state['current_remark']
    })
    current_eval_count = state.get('current_eval_count', 0)
    current_eval_count += 1
    return {'current_suggestion': suggestion, 'current_eval_count': current_eval_count}
