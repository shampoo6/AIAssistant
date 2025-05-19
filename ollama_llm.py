from langchain_ollama import ChatOllama

llm = ChatOllama(model='deepseek-r1:7b')

if __name__ == '__main__':
    print(llm.invoke('你好，请问根号0等于多少？'))
