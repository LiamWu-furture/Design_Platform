import json
import re

def extract_json_from_text(text):
    """
    从文本中提取并解析JSON数据，支持处理Markdown代码块
    """
    if not text:
        return None

    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 1. 尝试去除 Markdown 代码块标记 (```json ... ```)
    # 匹配 ```json 或 ``` 开头，以及 ``` 结尾的内容
    markdown_pattern = r"```(?:json)?\s*(.*?)\s*```"
    match = re.search(markdown_pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # 2. 如果上面的失败，尝试寻找最外层的 {}
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = text[start_idx:end_idx+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
            
    return None
