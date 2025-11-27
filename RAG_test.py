from random import choices

API_KEY_Qwen3_MAX = "sk-69122c7a6960491685c6edc87c028dfa"

from openai import OpenAI
import faiss
import numpy as np
import json
# ===============================
# 1. 初始化 OpenAI 客户端
# ===============================
client = OpenAI(api_key=API_KEY_Qwen3_MAX,base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")


# ===============================
# 2. 创建本地文档库
# ===============================
documents = [
    "LiamWu,中文名为巫家浩，四川工业科技学院软件工程学生，男生，喜欢编程和探索，主要使用编程语言python，c++",
    "刘鑫忠，英文名为Jack，四川工业科技学院软件工程专业学生,男生，喜欢玩游戏，会一点点C语言，但始终详细自己能找到实习"
]


# ===============================
# 3. 文本 → 向量（Embedding）
# ===============================
def embed(texts):
    response = client.embeddings.create(
        model="text-embedding-v4",
        input=texts
    )
    return [np.array(item.embedding, dtype="float32") for item in response.data]


doc_vectors = embed(documents)

# ===============================
# 4. 创建 FAISS 向量数据库
# ===============================
dim = len(doc_vectors[0])      # Embedding 维度
index = faiss.IndexFlatL2(dim)  # L2 距离索引
index.add(np.array(doc_vectors))  # 写入向量


# ===============================
# 5. 检索函数
# ===============================
def search(query, top_k=2):
    query_vec = np.array(embed([query])[0]).reshape(1, -1)
    distances, indices = index.search(query_vec, top_k)
    return [documents[i] for i in indices[0]]


# ===============================
# 6. RAG 生成答案
# ===============================
def answer(query):
    # 检索相关文档
    retrieved_docs = search(query)
    context = "\n".join(f"- {d}" for d in retrieved_docs)

    # 构建 Prompt
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

    # 调用大模型生成最终回答
    response = client.chat.completions.create(
        model="qwen3-max",
        messages=[{"role": "user", "content": prompt}],
        stream = True,
        stream_options={"include_usage": True}
    )

    return response


# ===============================
# 7. 测试
# ===============================
if __name__ == "__main__":
    while True:
        q = input("\n请输入：")
        if q == "exit":
            break
        print("\nRAG 应答：")
        for chunk in answer(q):
            if chunk.choices and chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content,end="")
