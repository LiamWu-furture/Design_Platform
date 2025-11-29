# author:LiamWu
# beginDate:2025/11/28
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


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
print(docs)