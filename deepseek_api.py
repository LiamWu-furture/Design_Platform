import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

import json
import time
from utils import extract_json_from_text

# 导入 RAG 服务
try:
    from rag_service import _retriever, initialize_rag
    RAG_AVAILABLE = True
    # 确保 RAG 系统已初始化
    initialize_rag()
except Exception as e:
    print(f"RAG 系统不可用: {e}")
    RAG_AVAILABLE = False
    _retriever = None

# 初始化OpenAI客户端，使用DeepSeek的base_url
if DEEPSEEK_API_KEY:
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
else:
    client = None

def get_academic_references(user_prompt):
    """
    从知识库检索与设计需求相关的学术文献
    
    Args:
        user_prompt: 用户的设计需求
        
    Returns:
        str: 相关学术文献内容，如果 RAG 不可用则返回空字符串
    """
    if not RAG_AVAILABLE or _retriever is None:
        return ""
    
    try:
        # 构建检索查询，提取关键信息
        search_queries = [
            f"光电探测器设计 {user_prompt}",
            "叠层光电探测器结构",
            "量子效率优化方法"
        ]
        
        all_docs = []
        for query in search_queries:
            docs = _retriever.invoke(query)
            all_docs.extend(docs)
        
        # 去重并限制文档数量
        unique_docs = []
        seen_content = set()
        for doc in all_docs:
            content_hash = hash(doc.page_content[:100])  # 使用前100字符作为去重依据
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_docs.append(doc)
                if len(unique_docs) >= 5:  # 最多5个文档片段
                    break
        
        if not unique_docs:
            return ""
        
        # 格式化文献内容
        references = "\n\n".join([
            f"【参考文献片段 {i+1}】\n{doc.page_content}"
            for i, doc in enumerate(unique_docs)
        ])
        
        return references
        
    except Exception as e:
        print(f"检索学术文献失败: {e}")
        return ""

SYSTEM_PROMPT = """你是一位专业的光电探测器设计专家，精通半导体物理、材料科学和光电器件工程。
你的任务是根据用户提供的参数，设计一个高性能的叠层光电探测器。

设计时需要考虑：
1. 材料的禁带宽度与目标波长的匹配
2. 各层厚度对光吸收和载流子收集的影响
3. 异质结界面的能带匹配
4. 暗电流的抑制
5. 量子效率的优化

请严格按照JSON格式输出设计结果，包含layers（层结构）、performance（性能参数）、optimization_suggestions（优化建议）和explanation（设计说明）。
"""

SYSTEM_PROMPT_WITH_RAG = """你是一位专业的光电探测器设计专家，精通半导体物理、材料科学和光电器件工程。
你的任务是根据用户提供的参数和学术文献资料，设计一个高性能的叠层光电探测器。

**重要要求**：
1. 你必须参考提供的【学术文献】中的设计思路、材料选择和性能参数
2. 设计方案应基于文献中的实验数据和理论分析
3. 在 explanation 字段中明确说明你参考了哪些文献内容，以及如何应用这些知识
4. 优化建议应结合文献中的最新研究成果

设计时需要考虑：
1. 材料的禁带宽度与目标波长的匹配（参考文献中的材料特性）
2. 各层厚度对光吸收和载流子收集的影响（参考文献中的优化参数）
3. 异质结界面的能带匹配（参考文献中的界面工程）
4. 暗电流的抑制（参考文献中的抑制策略）
5. 量子效率的优化（参考文献中的效率提升方法）

请严格按照JSON格式输出设计结果，包含layers（层结构）、performance（性能参数）、optimization_suggestions（优化建议）和explanation（设计说明，必须引用文献）。
"""

def call_deepseek_api(user_prompt, model="deepseek-reasoner", use_rag=True):
    """
    调用DeepSeek API进行探测器设计（非流式）
    
    Args:
        user_prompt: 用户提示词
        model: 模型名称，默认为 "deepseek-reasoner" (R1)，可选 "deepseek-chat" (V3)
        use_rag: 是否使用 RAG 增强，默认为 True
    """
    if not client:
        return {
            'status': 'error',
            'message': 'API密钥未配置，请在.env文件中设置DEEPSEEK_API_KEY'
        }
    
    try:
        # 检索学术文献
        academic_refs = ""
        if use_rag and RAG_AVAILABLE:
            academic_refs = get_academic_references(user_prompt)
        
        # 根据是否有文献选择不同的系统提示词
        if academic_refs:
            system_prompt = SYSTEM_PROMPT_WITH_RAG
            # 将文献添加到用户提示词中
            enhanced_prompt = f"""【学术文献】
{academic_refs}

【设计需求】
{user_prompt}

请基于以上学术文献和设计需求，给出专业的探测器设计方案。"""
        else:
            system_prompt = SYSTEM_PROMPT
            enhanced_prompt = user_prompt
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': enhanced_prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False
        )
        
        content = response.choices[0].message.content
        
        return {
            'status': 'success',
            'content': content,
            'used_rag': bool(academic_refs)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'API调用失败: {str(e)}'
        }

def generate_design_stream(prompt, model_type='deepseek-reasoner', use_rag=True):
    """
    生成器函数，用于流式调用DeepSeek API并返回特定格式的进度数据
    
    Args:
        prompt: 用户提示词
        model_type: 模型类型
        use_rag: 是否使用 RAG 增强，默认为 True
    """
    if not client:
        yield json.dumps({
            'step': -1,
            'error': 'API密钥未配置',
            'progress': 0
        }) + '\n'
        return

    # 确定模型显示名称
    model_display = "AI推理模型" if model_type == 'deepseek-reasoner' else "AI大模型"

    # RAG 检索阶段
    academic_refs = ""
    if use_rag and RAG_AVAILABLE:
        yield json.dumps({'step': 3, 'message': '📚 检索学术文献...', 'progress': 25, 'log': True}) + '\n'
        time.sleep(0.2)
        
        academic_refs = get_academic_references(prompt)
        
        if academic_refs:
            yield json.dumps({'step': 3, 'message': '✅ 已检索到相关学术文献，将用于增强设计', 'progress': 28, 'log': True}) + '\n'
        else:
            yield json.dumps({'step': 3, 'message': '⚠️ 未找到相关文献，使用标准设计模式', 'progress': 28, 'log': True}) + '\n'
        time.sleep(0.2)

    yield json.dumps({'step': 3, 'message': f'调用{model_display} API', 'progress': 30}) + '\n'
    time.sleep(0.3)
    
    yield json.dumps({'step': 3, 'message': f'🔗 连接{model_display} API...', 'progress': 35, 'log': True}) + '\n'
    yield json.dumps({'step': 3, 'message': f'📡 发送设计请求到{model_display}模型...', 'progress': 38, 'log': True}) + '\n'
    yield json.dumps({'step': 3, 'message': f'✅ 连接成功，{model_display}开始推理...', 'progress': 40, 'log': True}) + '\n'

    try:
        # 根据是否有文献选择不同的系统提示词和用户提示词
        if academic_refs:
            system_prompt = SYSTEM_PROMPT_WITH_RAG
            enhanced_prompt = f"""【学术文献】
{academic_refs}

【设计需求】
{prompt}

请基于以上学术文献和设计需求，给出专业的探测器设计方案。在设计说明中请明确引用文献内容。"""
        else:
            system_prompt = SYSTEM_PROMPT
            enhanced_prompt = prompt
        
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': enhanced_prompt}
        ]
        
        response = client.chat.completions.create(
            model=model_type,
            messages=messages,
            stream=True
        )
        
        reasoning_content = ""
        content = ""
        reasoning_count = 0
        content_count = 0
        
        for chunk in response:
            # 处理推理过程（仅R1模型有）
            if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                reasoning_chunk = chunk.choices[0].delta.reasoning_content
                reasoning_content += reasoning_chunk
                reasoning_count += 1
                
                # 每收到5个推理chunk输出一次日志
                if reasoning_count % 5 == 0:
                    current_progress = min(40 + reasoning_count // 5, 60)
                    preview = reasoning_content[-50:].replace('\n', ' ')
                    yield json.dumps({
                        'step': 4,
                        'message': f' {model_display}推理中: ...{preview}',
                        'progress': current_progress,
                        'log': True
                    }) + '\n'
            
            # 处理最终内容
            elif chunk.choices[0].delta.content:
                content_chunk = chunk.choices[0].delta.content
                content += content_chunk
                content_count += 1
                
                # 每收到3个内容chunk输出一次日志
                if content_count % 3 == 0:
                    current_progress = min(60 + content_count // 3, 70)
                    yield json.dumps({
                        'step': 4,
                        'message': f'✨ {model_display}生成方案中... (已生成 {len(content)} 字符)',
                        'progress': current_progress,
                        'log': True
                    }) + '\n'
        
        yield json.dumps({
            'step': 4,
            'message': f' 推理完成！推理 {len(reasoning_content)} 字符，方案 {len(content)} 字符',
            'progress': 75,
            'log': True
        }) + '\n'
        
        # 返回最终的完整内容，作为一个特殊的消息类型，或者让调用者自己解析
        # 这里我们不直接yield结果对象，而是让调用者知道API调用已完成，并提供内容
        # 但为了保持流的一致性，我们可以在生成器最后返回结果
        
        yield json.dumps({'step': 5, 'message': '解析设计方案', 'progress': 80}) + '\n'
        time.sleep(0.5)

        # 使用 utils 中的函数解析
        design_data = extract_json_from_text(content)
        
        if not design_data:
            yield json.dumps({
                'step': -1,
                'error': 'API返回的数据格式不正确，无法解析为JSON',
                'progress': 0
            }) + '\n'
            return

        # 成功解析，将数据传回
        # 注意：这里我们用一个特殊的 type 来标识这是最终数据
        yield json.dumps({
            'type': 'result',
            'design_data': design_data,
            'reasoning_content': reasoning_content
        }) + '\n'

    except Exception as e:
        yield json.dumps({
            'step': -1,
            'error': f'API调用失败: {str(e)}',
            'progress': 0
        }) + '\n'

def call_deepseek_api_stream(user_prompt, log_callback=None):
    """
    调用DeepSeek R1 API进行探测器设计（流式输出，带推理过程）
    
    Args:
        user_prompt: 用户的设计需求
        log_callback: 日志回调函数，用于实时输出AI思考过程
        
    Returns:
        dict: 包含status、content和reasoning_content的字典
    """
    if not DEEPSEEK_API_KEY:
        return {
            'status': 'error',
            'message': 'API密钥未配置，请在.env文件中设置DEEPSEEK_API_KEY'
        }
    
    try:
        if log_callback:
            log_callback('🔗 连接推理大模型 API...')
        
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt}
        ]
        
        if log_callback:
            log_callback('📡 发送设计请求到深度学习模型...')
        
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=True
        )
        
        if log_callback:
            log_callback('✅ 连接成功，R1开始推理...')
        
        reasoning_content = ""
        content = ""
        reasoning_count = 0
        content_count = 0
        
        for chunk in response:
            # 处理推理过程
            if chunk.choices[0].delta.reasoning_content:
                reasoning_chunk = chunk.choices[0].delta.reasoning_content
                reasoning_content += reasoning_chunk
                reasoning_count += 1
                
                # 每收到20个推理chunk输出一次日志
                if reasoning_count % 20 == 0 and log_callback:
                    log_callback(f' AI正在深度推理... (推理 {len(reasoning_content)} 字符)')
            
            # 处理最终内容
            elif chunk.choices[0].delta.content:
                content_chunk = chunk.choices[0].delta.content
                content += content_chunk
                content_count += 1
                
                # 每收到10个内容chunk输出一次日志
                if content_count % 10 == 0 and log_callback:
                    log_callback(f' AI正在生成方案... (已生成 {len(content)} 字符)')
        
        if log_callback:
            log_callback(f' 推理完成！推理过程 {len(reasoning_content)} 字符，方案 {len(content)} 字符')
        
        return {
            'status': 'success',
            'content': content,
            'reasoning_content': reasoning_content
        }
        
    except Exception as e:
        if log_callback:
            log_callback(f'❌ API调用失败: {str(e)}')
        return {
            'status': 'error',
            'message': f'API调用失败: {str(e)}'
        }
