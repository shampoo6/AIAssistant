import os

from langchain_community.chat_models import ChatSparkLLM

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = os.getenv('SPARKAI_URL')
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = os.getenv('SPARKAI_APP_ID')
SPARKAI_API_SECRET = os.getenv('SPARKAI_API_SECRET')
SPARKAI_API_KEY = os.getenv('SPARKAI_API_KEY')
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = os.getenv('SPARKAI_DOMAIN')

llm = ChatSparkLLM(
    spark_api_url=SPARKAI_URL,
    spark_llm_domain=SPARKAI_DOMAIN,
    temperature=0.9,
    spark_app_id=SPARKAI_APP_ID,
    spark_api_key=SPARKAI_API_KEY,
    spark_api_secret=SPARKAI_API_SECRET
)

if __name__ == '__main__':
    print(llm.invoke('你好'))
