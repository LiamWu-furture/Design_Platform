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
text = [doc.page_content for doc in chunks]
embeddings = DashScopeEmbeddings(
    model = "text-embedding-v4",
    dashscope_api_key =  "sk-69122c7a6960491685c6edc87c028dfa",
)
db = FAISS.from_documents(chunks,embeddings)
db.save_local("vector_db")