# author:LiamWu
# beginDate:2025/11/28
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings


# 把论文pdf版本放在data文件夹下面,运行此文件,此文件会自动加载pdf文本,并创建向量数据库
# 向量数据库会保存在

# 加载所有在data文件夹下面的论文
loader = DirectoryLoader(
    './data',
    glob = "**/*.pdf",
    loader_cls=PyPDFLoader,
    show_progress=True
)
# 将所有pdf文本加载为langchain对象
docs = loader.load()
print(f"已被划分成{len(docs)}个区块")

# 文本切块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    separators=['\n\n','\n','.',' ',""]
)
chunks = text_splitter.split_documents(docs)
print(f"已被划分成{len(chunks)}个可嵌入区块")

embeddings = DashScopeEmbeddings(
    model = "text-embedding-v4",
    dashscope_api_key =  "sk-69122c7a6960491685c6edc87c028dfa",
)

# 分批处理以避免 API 限制和兼容性问题
batch_size = 25  # 每批处理 25 个文档
print(f"开始分批生成向量数据库，每批 {batch_size} 个区块...")

db = None
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    print(f"处理第 {i//batch_size + 1} 批 ({i+1}-{min(i+batch_size, len(chunks))}/{len(chunks)})...")
    
    try:
        if db is None:
            # 第一批：创建数据库
            db = FAISS.from_documents(batch, embeddings)
        else:
            # 后续批次：添加到现有数据库
            batch_db = FAISS.from_documents(batch, embeddings)
            db.merge_from(batch_db)
        print(f"  ✓ 第 {i//batch_size + 1} 批处理成功")
    except Exception as e:
        print(f"  ✗ 第 {i//batch_size + 1} 批处理失败: {e}")
        print(f"  跳过此批次，继续处理...")
        continue

if db is not None:
    db.save_local("vector_db")
    print("向量数据库已保存到 vector_db/")
else:
    print("错误：未能创建向量数据库")