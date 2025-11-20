import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

# 使用非交互式后端
matplotlib.use('Agg')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def generate_visualizations(design_data):
    """
    根据设计数据生成可视化图像
    
    Args:
        design_data: 包含layers和performance的设计数据字典
        
    Returns:
        dict: 包含图像路径的字典
    """
    image_paths = {}
    
    # 确保输出目录存在
    os.makedirs('static/images', exist_ok=True)
    
    # 生成层叠结构图
    if 'layers' in design_data and design_data['layers']:
        structure_path = generate_structure_plot(design_data['layers'])
        image_paths['structure'] = structure_path
    
    # 生成性能曲线图
    if 'performance' in design_data and 'responsivity_data' in design_data['performance']:
        performance_path = generate_performance_plot(design_data['performance'])
        image_paths['performance'] = performance_path
    
    return image_paths

def generate_structure_plot(layers):
    """
    生成叠层结构的堆叠条形图
    
    Args:
        layers: 层结构列表
        
    Returns:
        str: 图像相对路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 提取数据
    materials = [layer['material'] for layer in layers]
    thicknesses = [layer['thickness'] for layer in layers]
    
    # 创建颜色映射
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(materials)))
    
    # 绘制堆叠条形图
    bottom = 0
    for i, (material, thickness) in enumerate(zip(materials, thicknesses)):
        ax.barh(0, thickness, left=bottom, height=0.5, 
               color=colors[i], label=f'{material} ({thickness} nm)',
               edgecolor='black', linewidth=1.5)
        
        # 添加文本标签
        ax.text(bottom + thickness/2, 0, f'{material}\n{thickness}nm', 
               ha='center', va='center', fontsize=10, fontweight='bold')
        
        bottom += thickness
    
    ax.set_ylim(-0.5, 0.5)
    ax.set_xlim(0, bottom * 1.05)
    ax.set_xlabel('Thickness (nm)', fontsize=12, fontweight='bold')
    ax.set_title('Detector Layer Structure', fontsize=14, fontweight='bold')
    ax.set_yticks([])
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    output_path = 'static/images/structure.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path

def generate_performance_plot(performance):
    """
    生成性能曲线图（响应度 vs 波长）
    
    Args:
        performance: 性能数据字典
        
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
    
    output_path = 'static/images/performance.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    return output_path
