# file: simple_rag.py
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from openai import OpenAI
os.environ["DASHSCOPE_API_KEY"] = "sk-69122c7a6960491685c6edc87c028dfa"
API_KEY_Qwen3_MAX = "sk-69122c7a6960491685c6edc87c028dfa"
client = OpenAI(api_key=API_KEY_Qwen3_MAX,base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
# 加载向量库
db = FAISS.load_local("vector_db",
                      DashScopeEmbeddings(model="text-embedding-v4"),
                      allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 5})
def answer(query):
    docs = retriever.invoke(query)
    context = "\n\n".join([d.page_content for d in docs])

# 大模型
    prompt = f"""
你是一个专业问答助手，请始终记住自己的身份和职责。
请根据以下资料回答用户的问题，不要凭空编造。
【资料】
    {context}
【问题】
    {query}
【要求】
1. 基于资料作答
2. 若问题已确认不属于资料里面的内容或者指代不明确，请根据自身已学习知识回答，并不要说明根据"自身已学习知识回答"和显示资料库里面的任何内容
3. 若资料不足请说明“基于自身已学习知识回答”，并给出回答
4. 若问题指代不明确，请不要输出资料库里面的任何内容 -- 特别重要
"""
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        stream_options={"include_usage": True}
    )
    return response

# 一键问答
if __name__ == "__main__":
    while True:
        q = input("\n请输入：")
        if q == "exit":
            break
        print("\nRAG 应答：")
        for chunk in answer(q):
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content,end="")
