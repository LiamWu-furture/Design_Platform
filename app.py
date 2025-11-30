from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
from dotenv import load_dotenv
from deepseek_api import call_deepseek_api, generate_design_stream
from visualize import generate_visualizations
from utils import extract_json_from_text
import json
import time
import threading
import uuid
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# 全局字典存储设计结果（用于解决Generator中无法使用session的问题）
# 结构: {task_id: {'data': result_data, 'created_at': datetime}}
design_results = {}

def cleanup_old_results():
    """定期清理过期的设计结果（保留24小时）"""
    while True:
        time.sleep(3600)  # 每小时检查一次
        now = datetime.now()
        expired_keys = []
        for task_id, info in design_results.items():
            if now - info['created_at'] > timedelta(hours=24):
                expired_keys.append(task_id)
        
        for key in expired_keys:
            # 清理关联的图片文件
            try:
                if key in design_results:
                    result_data = design_results[key].get('data', {})
                    images = result_data.get('images', {})
                    for img_path in images.values():
                        if img_path and os.path.exists(img_path):
                            os.remove(img_path)
            except Exception as e:
                print(f"Error cleaning up files for task {key}: {e}")
                
            del design_results[key]

# 启动清理线程
cleanup_thread = threading.Thread(target=cleanup_old_results, daemon=True)
cleanup_thread.start()

@app.route('/')
def index():
    return render_template('index.html', active_tab='input')

@app.route('/thinking', methods=['POST'])
def thinking():
    """显示AI思考页面"""
    # 生成唯一的任务ID
    task_id = str(uuid.uuid4())
    
    # 保存表单数据到session
    session['design_params'] = {
        'material_type': request.form.get('material_type'),
        'bandgap_min': request.form.get('bandgap_min'),
        'bandgap_max': request.form.get('bandgap_max'),
        'thickness_min': request.form.get('thickness_min'),
        'thickness_max': request.form.get('thickness_max'),
        'target_application': request.form.get('target_application'),
        'additional_requirements': request.form.get('additional_requirements', ''),
        'deep_thinking': request.form.get('deep_thinking', 'yes')
    }
    session['task_id'] = task_id
    
    return render_template('thinking.html', active_tab='thinking', **session['design_params'])

@app.route('/api/design', methods=['POST'])
def api_design():
    """异步API端点，执行实际的设计工作"""
    try:
        # 从session获取参数和task_id
        params = session.get('design_params', {})
        task_id = session.get('task_id')
        
        material_type = params.get('material_type')
        bandgap_min = params.get('bandgap_min')
        bandgap_max = params.get('bandgap_max')
        thickness_min = params.get('thickness_min')
        thickness_max = params.get('thickness_max')
        target_application = params.get('target_application')
        additional_requirements = params.get('additional_requirements', '')
        deep_thinking = params.get('deep_thinking', 'yes')
        
        # 返回进度更新
        def generate_progress():
            yield json.dumps({'step': 1, 'message': '接收设计参数', 'progress': 10}) + '\n'
            time.sleep(0.3)
            
            yield json.dumps({'step': 2, 'message': '构建提示词', 'progress': 20}) + '\n'
            time.sleep(0.5)
            
            # 构建提示词
            prompt = f"""请设计一个叠层光电探测器，参数如下：
材料类型: {material_type}
禁带宽度范围: {bandgap_min}-{bandgap_max} eV
厚度范围: {thickness_min}-{thickness_max} nm
目标应用: {target_application}
额外要求: {additional_requirements}

请务必包含完整的层叠结构，必须明确包含以下功能层：
1. 顶电极 (Top Electrode)
2. 电子传输层 (Electron Transport Layer, ETL)
3. 光吸收层 (Absorber Layer) - **特别要求**：光吸收层严禁使用单一均质材料。请将其设计为复合结构（如量子阱结构、超晶格结构、异质结或梯度带隙结构），并在返回的layers列表中将其拆分为具体的子层（例如："吸收层(量子阱)"、"吸收层(量子垒)"等）。
4. 空穴传输层 (Hole Transport Layer, HTL)
5. 底电极 (Bottom Electrode)
以及其他必要的缓冲层或接触层。

请以JSON格式返回设计结果，包含以下字段：
{{
    "layers": [
        {{"name": "层名称(如:顶电极/ETL/吸收层/HTL/底电极)", "material": "材料名称", "thickness": 厚度值(nm), "bandgap": 禁带宽度(eV), "function": "详细功能描述", "fabrication_process": "详细制备工艺"}},
        ...
    ],
    "performance": {{
        "wavelength_range": [最小波长(nm), 最大波长(nm)],
        "responsivity_data": [[波长1, 响应度1], [波长2, 响应度2], ...],
        "quantum_efficiency": 量子效率(%),
        "quantum_efficiency_type": "IQE"或"EQE" (明确注明是内量子效率还是外量子效率),
        "dark_current": 暗电流(A)
    }},
    "optimization_suggestions": ["建议1", "建议2", ...],
    "explanation": "设计说明"
}}"""
            
            # 确定模型
            model_type = "deepseek-reasoner" if deep_thinking == 'yes' else "deepseek-chat"
            
            # 调用封装好的流式生成器
            # 注意：这里是一个生成器调用另一个生成器，我们需要遍历它
            for chunk_str in generate_design_stream(prompt, model_type):
                chunk_data = json.loads(chunk_str)
                
                # 如果是最终结果类型
                if chunk_data.get('type') == 'result':
                    design_data = chunk_data['design_data']
                    
                    yield json.dumps({'step': 6, 'message': '生成可视化', 'progress': 90}) + '\n'
                    
                    # 生成可视化
                    image_paths = generate_visualizations(design_data)
                    
                    # 赋予每一层视觉属性
                    # 在3D wrapper中居中
                    # 添加层间距
                    GAP = 10
                    NORMAL_HEIGHT = 40
                    ABSORBER_HEIGHT = 20
                    
                    # 计算总视觉高度
                    total_visual_height = 0
                    for layer in design_data['layers']:
                        is_absorber = '吸收' in layer.get('name', '') or 'Absorber' in layer.get('name', '')
                        h = ABSORBER_HEIGHT if is_absorber else NORMAL_HEIGHT
                        layer['visual_height'] = h
                        total_visual_height += h
                    
                    if design_data['layers']:
                        total_visual_height += (len(design_data['layers']) - 1) * GAP
                    
                    start_y = (400 - total_visual_height) / 2
                    
                    current_y = start_y
                    for i, layer in enumerate(design_data['layers']):
                        # 计算每一层的Y坐标
                        layer['y_position'] = current_y
                        current_y += layer['visual_height'] + GAP
                    
                    # 保存结果
                    result_data = {
                        'design_data': design_data,
                        'images': image_paths,
                        'user_input': {
                            'material_type': material_type,
                            'bandgap_range': f"{bandgap_min}-{bandgap_max} eV",
                            'thickness_range': f"{thickness_min}-{thickness_max} nm",
                            'target_application': target_application,
                            'additional_requirements': additional_requirements
                        }
                    }
                    
                    if task_id:
                        design_results[task_id] = {
                            'data': result_data,
                            'created_at': datetime.now()
                        }
                    
                    yield json.dumps({
                        'step': 7,
                        'message': '完成',
                        'progress': 100,
                        'redirect': '/result'
                    }) + '\n'
                    return
                
                # 普通进度/日志消息直接透传
                yield chunk_str

        return app.response_class(generate_progress(), mimetype='application/json')
        
    except Exception as e:
        return jsonify({
            'step': -1,
            'error': f'系统错误: {str(e)}',
            'progress': 0
        })

@app.route('/result')
def result():
    """显示设计结果"""
    task_id = session.get('task_id')
    
    if not task_id or task_id not in design_results:
        return redirect(url_for('index'))
    
    result_data = design_results[task_id]['data']
    
    return render_template('result.html', active_tab='result', **result_data)

@app.route('/design', methods=['POST'])
def design():
    try:
        # 获取表单数据
        material_type = request.form.get('material_type')
        bandgap_min = request.form.get('bandgap_min')
        bandgap_max = request.form.get('bandgap_max')
        thickness_min = request.form.get('thickness_min')
        thickness_max = request.form.get('thickness_max')
        target_application = request.form.get('target_application')
        additional_requirements = request.form.get('additional_requirements', '')
        
        # 构建提示词
        prompt = f"""请设计一个叠层光电探测器，参数如下：
材料类型: {material_type}
禁带宽度范围: {bandgap_min}-{bandgap_max} eV
厚度范围: {thickness_min}-{thickness_max} nm
目标应用: {target_application}
额外要求: {additional_requirements}

请务必包含完整的层叠结构，必须明确包含以下功能层：
1. 顶电极 (Top Electrode)
2. 电子传输层 (Electron Transport Layer, ETL)
3. 光吸收层 (Absorber Layer) - **特别要求**：光吸收层严禁使用单一均质材料。请将其设计为复合结构（如量子阱结构、超晶格结构、异质结或梯度带隙结构），并在返回的layers列表中将其拆分为具体的子层（例如："吸收层(量子阱)"、"吸收层(量子垒)"等）。
4. 空穴传输层 (Hole Transport Layer, HTL)
5. 底电极 (Bottom Electrode)
以及其他必要的缓冲层或接触层。

请以JSON格式返回设计结果，包含以下字段：
{{
    "layers": [
        {{"name": "层名称(如:顶电极/ETL/吸收层/HTL/底电极)", "material": "材料名称", "thickness": 厚度值(nm), "bandgap": 禁带宽度(eV), "function": "详细功能描述", "fabrication_process": "详细制备工艺"}},
        ...
    ],
    "performance": {{
        "wavelength_range": [最小波长(nm), 最大波长(nm)],
        "responsivity_data": [[波长1, 响应度1], [波长2, 响应度2], ...],
        "quantum_efficiency": 量子效率(%),
        "quantum_efficiency_type": "IQE"或"EQE" (明确注明是内量子效率还是外量子效率),
        "dark_current": 暗电流(A)
    }},
    "optimization_suggestions": ["建议1", "建议2", ...],
    "explanation": "设计说明"
}}"""
        
        # 调用DeepSeek API
        api_response = call_deepseek_api(prompt)
        
        if api_response['status'] == 'error':
            return render_template('result.html', 
                                 error=api_response['message'],
                                 user_input={
                                     'material_type': material_type,
                                     'bandgap_range': f"{bandgap_min}-{bandgap_max} eV",
                                     'thickness_range': f"{thickness_min}-{thickness_max} nm",
                                     'target_application': target_application,
                                     'additional_requirements': additional_requirements
                                 })
        
        # 解析JSON响应
        design_data = extract_json_from_text(api_response['content'])
        
        if not design_data:
            return render_template('result.html', 
                                 error="API返回的数据格式不正确，无法解析为JSON",
                                 raw_response=api_response['content'],
                                 user_input={
                                     'material_type': material_type,
                                     'bandgap_range': f"{bandgap_min}-{bandgap_max} eV",
                                     'thickness_range': f"{thickness_min}-{thickness_max} nm",
                                     'target_application': target_application,
                                     'additional_requirements': additional_requirements
                                 })
        
        # 生成可视化
        temp_task_id = str(uuid.uuid4())
        image_paths = generate_visualizations(design_data, temp_task_id)
        
        # 渲染结果页面
        return render_template('result.html',
                             design_data=design_data,
                             images=image_paths,
                             user_input={
                                 'material_type': material_type,
                                 'bandgap_range': f"{bandgap_min}-{bandgap_max} eV",
                                 'thickness_range': f"{thickness_min}-{thickness_max} nm",
                                 'target_application': target_application,
                                 'additional_requirements': additional_requirements
                             })
        
    except Exception as e:
        return render_template('result.html', 
                             error=f"系统错误: {str(e)}",
                             user_input={
                                 'material_type': request.form.get('material_type', ''),
                                 'bandgap_range': f"{request.form.get('bandgap_min', '')}-{request.form.get('bandgap_max', '')} eV",
                                 'thickness_range': f"{request.form.get('thickness_min', '')}-{request.form.get('thickness_max', '')} nm",
                                 'target_application': request.form.get('target_application', ''),
                                 'additional_requirements': request.form.get('additional_requirements', '')
                             })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
