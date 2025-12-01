# author:LiamWu
# beginDate:2025/12/01
# 功能：向现有的向量数据库追加新的PDF文档
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
import os


# 检查向量数据库是否存在
if not os.path.exists("vector_db"):
    print("错误：向量数据库不存在！")
    print("请先运行 vector_database_save.py 创建初始数据库")
    exit(1)

# 配置 Embedding 模型
embeddings = DashScopeEmbeddings(
    model = "text-embedding-v4",
    dashscope_api_key =  "sk-69122c7a6960491685c6edc87c028dfa",
)

# 加载现有的向量数据库
print("正在加载现有向量数据库...")
db = FAISS.load_local("vector_db", embeddings, allow_dangerous_deserialization=True)
print(f"✓ 已加载现有数据库")

# 加载新的PDF文档（可以指定特定文件夹或文件）
# 方式1：从指定文件夹加载所有PDF
new_data_folder = './data_new'  # 新数据文件夹，可根据需要修改

if os.path.exists(new_data_folder):
    print(f"从 {new_data_folder} 文件夹加载新文档...")
    loader = DirectoryLoader(
        new_data_folder,
        glob = "**/*.pdf",
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs = loader.load()
    print(f"已加载 {len(docs)} 个新文档区块")
else:
    # 方式2：手动指定单个或多个PDF文件
    print("data_new 文件夹不存在，使用手动指定文件模式")
    pdf_files = [
        # 在这里添加要追加的PDF文件路径
        # 例如: './data/new_paper1.pdf',
        #      './data/new_paper2.pdf',
    ]
    
    if not pdf_files:
        print("错误：未指定要添加的PDF文件！")
        print("请在代码中指定 pdf_files 列表，或创建 data_new 文件夹并放入PDF文件")
        exit(1)
    
    docs = []
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"加载文件: {pdf_file}")
            loader = PyPDFLoader(pdf_file)
            docs.extend(loader.load())
        else:
            print(f"警告：文件不存在，跳过: {pdf_file}")
    
    print(f"已加载 {len(docs)} 个新文档区块")

if len(docs) == 0:
    print("没有新文档需要添加，退出")
    exit(0)

# 文本切块
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200,
    separators=['\n\n','\n','.',' ',""]
)
chunks = text_splitter.split_documents(docs)
print(f"新文档已被划分成 {len(chunks)} 个可嵌入区块")

# 分批追加到现有数据库
batch_size = 25  # 每批处理 25 个文档
print(f"开始分批追加到向量数据库，每批 {batch_size} 个区块...")

success_count = 0
fail_count = 0

for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    batch_num = i//batch_size + 1
    print(f"处理第 {batch_num} 批 ({i+1}-{min(i+batch_size, len(chunks))}/{len(chunks)})...")
    
    try:
        # 为当前批次创建临时向量数据库
        batch_db = FAISS.from_documents(batch, embeddings)
        # 合并到主数据库
        db.merge_from(batch_db)
        print(f"  ✓ 第 {batch_num} 批追加成功")
        success_count += len(batch)
    except Exception as e:
        print(f"  ✗ 第 {batch_num} 批追加失败: {e}")
        print(f"  跳过此批次，继续处理...")
        fail_count += len(batch)
        continue

# 保存更新后的数据库
print("\n正在保存更新后的向量数据库...")
db.save_local("vector_db")
print("=" * 60)
print(f"✓ 向量数据库已更新并保存到 vector_db/")
print(f"  成功追加: {success_count} 个区块")
if fail_count > 0:
    print(f"  失败跳过: {fail_count} 个区块")
print("=" * 60)
