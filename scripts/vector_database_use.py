# author:LiamWu
# 功能：简单的 RAG 问答测试（基于已有向量数据库）
# 用法：在项目根目录运行 python scripts/vector_database_use.py
import os
import sys
from dotenv import load_dotenv

# 确保工作目录为项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from openai import OpenAI

load_dotenv()

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')
if not DASHSCOPE_API_KEY:
    print("错误：未配置 DASHSCOPE_API_KEY，请在 .env 文件中设置")
    exit(1)

os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 加载向量库
db = FAISS.load_local(
    "vector_db",
    DashScopeEmbeddings(model="text-embedding-v4"),
    allow_dangerous_deserialization=True
)
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
3. 若资料不足请说明"基于自身已学习知识回答"，并给出回答
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
                print(chunk.choices[0].delta.content, end="")
