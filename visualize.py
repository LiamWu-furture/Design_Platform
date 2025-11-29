import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import re

# 使用非交互式后端
matplotlib.use('Agg')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def format_chemical_formula(text):
    """
    将化学式中的数字转换为下标格式 (LaTeX)
    例如: TiO2 -> TiO$_2$, Al2O3 -> Al$_2$O$_3$
    """
    if not text:
        return ""
    
    # 如果已经是LaTeX格式或者包含其他特殊字符，可能不需要处理
    if '$' in text:
        return text
        
    # 匹配化学式中的数字，将其替换为 $_{数字}$
    # 排除掉可能是厚度或其他数值的情况（这里简单假设紧跟在字母后的数字是化学式下标）
    # 使用正则：([a-zA-Z])(\d+) -> \1$_{\2}$
    formatted_text = re.sub(r'([a-zA-Z])(\d+)', r'\1$_{\2}$', text)
    
    return formatted_text

def generate_visualizations(design_data, task_id=None):
    """
    根据设计数据生成可视化图像
    
    Args:
        design_data: 包含layers和performance的设计数据字典
        task_id: 任务ID，用于生成唯一的文件名
        
    Returns:
        dict: 包含图像路径的字典
    """
    image_paths = {}
    
    # 确保输出目录存在
    os.makedirs('static/images', exist_ok=True)
    
    # 文件名前缀
    prefix = f"{task_id}_" if task_id else ""
    
    # 生成层叠结构图
    if 'layers' in design_data and design_data['layers']:
        # 主结构图：隐藏吸收层的详细标签，避免拥挤
        structure_path = generate_structure_plot(design_data['layers'], prefix, hide_absorber_labels=True)
        image_paths['structure'] = structure_path
        
        # 生成吸收层细节图
        absorber_layers = [l for l in design_data['layers'] if '吸收' in l.get('name', '') or 'Absorber' in l.get('name', '')]
        if absorber_layers:
            # 细节图：显示所有标签
            absorber_path = generate_structure_plot(absorber_layers, prefix + "absorber_", title="Absorber Layer Details", hide_absorber_labels=False)
            image_paths['absorber'] = absorber_path
    
    # 生成性能曲线图
    if 'performance' in design_data and 'responsivity_data' in design_data['performance']:
        performance_path = generate_performance_plot(design_data['performance'], prefix)
        image_paths['performance'] = performance_path
    
    return image_paths

def generate_structure_plot(layers, prefix="", title="Detector Layer Structure", hide_absorber_labels=False):
    """
    生成叠层结构的堆叠条形图
    
    Args:
        layers: 层结构列表
        prefix: 文件名前缀
        title: 图表标题
        hide_absorber_labels: 是否隐藏吸收层的标签
        
    Returns:
        str: 图像相对路径
    """
    # 增加画布高度以容纳外部标签
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 提取数据
    materials = [layer['material'] for layer in layers]
    names = [layer.get('name', '') for layer in layers]
    thicknesses = [layer['thickness'] for layer in layers]
    total_thickness = sum(thicknesses)
    
    # 创建颜色映射
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(materials)))
    
    # 绘制堆叠条形图
    bottom = 0
    for i, (material, thickness, name) in enumerate(zip(materials, thicknesses, names)):
        ax.barh(0, thickness, left=bottom, height=0.5, 
               color=colors[i], label=f'{material} ({thickness} nm)',
               edgecolor='black', linewidth=1.5)
        
        # 检查是否需要隐藏该层的标签
        is_absorber = '吸收' in name or 'Absorber' in name
        should_label = not (hide_absorber_labels and is_absorber)
        
        if should_label:
            # 智能标签定位
            mid_x = bottom + thickness / 2
            ratio = thickness / total_thickness
            
            # 如果层足够厚(>15%)，标签放在内部
            if ratio > 0.15:
                ax.text(mid_x, 0, f'{material}\n{thickness}nm', 
                       ha='center', va='center', fontsize=10, fontweight='bold', color='white')
            # 如果层较薄，使用引线标注在外部
            else:
                # 交替上下显示，避免重叠
                is_top = i % 2 == 0
                y_pos = 0.45 if is_top else -0.45
                
                ax.annotate(f'{material}\n{thickness}nm',
                           xy=(mid_x, 0.25 if is_top else -0.25),
                           xytext=(mid_x, y_pos),
                           ha='center', va='center',
                           fontsize=10, fontweight='bold',
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        bottom += thickness
    
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlim(0, bottom * 1.05)
    ax.set_xlabel('Thickness (nm)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_yticks([])
    
    # 调整图例位置到图表下方，避免挤压绘图区域
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize=10, ncol=3)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    output_path = f'static/images/{prefix}structure.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_performance_plot(performance, prefix=""):
    """
    生成性能曲线图（响应度 vs 波长）
    
    Args:
        performance: 性能数据字典
        prefix: 文件名前缀
        
    Returns:
        str: 图像相对路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 提取响应度数据
    responsivity_data = performance.get('responsivity_data', [])
    
    if responsivity_data:
        wavelengths = [point[0] for point in responsivity_data]
        responsivities = [point[1] for point in responsivity_data]
        
        # 绘制曲线
        ax.plot(wavelengths, responsivities, 'b-', linewidth=2.5, marker='o', 
               markersize=8, markerfacecolor='red', markeredgecolor='darkred',
               markeredgewidth=1.5, label='Responsivity')
        
        # 填充曲线下方区域
        ax.fill_between(wavelengths, responsivities, alpha=0.3)
        
        ax.set_xlabel('Wavelength (nm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Responsivity (A/W)', fontsize=12, fontweight='bold')
        ax.set_title('Detector Spectral Response', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
        
        # 添加性能指标文本
        if 'quantum_efficiency' in performance:
            qe = performance['quantum_efficiency']
            ax.text(0.02, 0.98, f'Quantum Efficiency: {qe}%', 
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', bbox=dict(boxstyle='round', 
                   facecolor='wheat', alpha=0.5))
    else:
        # 如果没有数据，生成示例曲线
        wavelengths = np.linspace(400, 1600, 50)
        responsivities = np.exp(-(wavelengths - 1000)**2 / 100000) * 0.8
        
        ax.plot(wavelengths, responsivities, 'b-', linewidth=2.5, marker='o',
               markersize=6, markerfacecolor='red', label='Responsivity (示例)')
        ax.fill_between(wavelengths, responsivities, alpha=0.3)
        
        ax.set_xlabel('Wavelength (nm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Responsivity (A/W)', fontsize=12, fontweight='bold')
        ax.set_title('Detector Spectral Response (示例数据)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=10)
    
    plt.tight_layout()
    
    output_path = f'static/images/{prefix}performance.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path
