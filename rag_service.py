# author:LiamWu
# beginDate:2025/12/01
# 功能：RAG 核心服务模块，用于设计增强
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 配置 API Key
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', 'sk-69122c7a6960491685c6edc87c028dfa')
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY

# 全局变量：向量数据库和检索器
_db = None
_retriever = None

def initialize_rag():
    """初始化 RAG 系统，加载向量数据库"""
    global _db, _retriever
    
    if _db is not None:
        return True
    
    try:
        # 检查向量数据库是否存在
        if not os.path.exists("vector_db"):
            print("警告：向量数据库不存在，RAG 功能将不可用")
            return False
        
        # 加载向量数据库
        print("正在加载向量数据库...")
        _db = FAISS.load_local(
            "vector_db",
            DashScopeEmbeddings(model="text-embedding-v4"),
            allow_dangerous_deserialization=True
        )
        _retriever = _db.as_retriever(search_kwargs={"k": 5})
        print("✓ RAG 系统初始化成功")
        return True
    except Exception as e:
        print(f"✗ RAG 系统初始化失败: {e}")
        return False

# 应用启动时自动初始化
initialize_rag()
