import env
import os

from langchain_community.chat_models import ChatZhipuAI

os.environ["ZHIPUAI_API_KEY"] = os.getenv('ZHIPU_API_KEY')
llm = ChatZhipuAI(
    model="GLM-4-Flash",
    temperature=0.9,
)

if __name__ == '__main__':
    print(llm.invoke('你好'))
