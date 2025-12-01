import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.globals import ThemeType


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
        structure_path = generate_structure_plot(design_data['layers'], prefix)
        image_paths['structure'] = structure_path
    
    # 生成性能曲线图
    if 'performance' in design_data and 'responsivity_data' in design_data['performance']:
        performance_path = generate_performance_plot(design_data['performance'], prefix)
        image_paths['performance'] = performance_path
    
    return image_paths

def generate_structure_plot(layers, prefix=""):
    """
    使用 pyecharts 生成叠层结构的堆叠条形图
    
    Args:
        layers: 层结构列表
        prefix: 文件名前缀
        
    Returns:
        str: 图像相对路径
    """
    # 提取数据
    materials = [f"{layer['material']} ({layer['thickness']}nm)" for layer in layers]
    thicknesses = [layer['thickness'] for layer in layers]
    
    # 创建堆叠条形图
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1200px", height="600px"))
        .add_xaxis(["Layer Structure"])
    )
    
    # 添加每一层
    for i, (material, thickness) in enumerate(zip(materials, thicknesses)):
        bar.add_yaxis(
            material,
            [thickness],
            stack="stack1",
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
        )
    
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="Detector Layer Structure", subtitle="Thickness (nm)"),
        xaxis_opts=opts.AxisOpts(name=""),
        yaxis_opts=opts.AxisOpts(name="Thickness (nm)"),
        legend_opts=opts.LegendOpts(pos_right="5%", orient="vertical"),
    )
    
    output_path = f'static/images/{prefix}structure.html'
    bar.render(output_path)
    
    return output_path

def generate_performance_plot(performance, prefix=""):
    """
    使用 pyecharts 生成性能曲线图（响应度 vs 波长）
    
    Args:
        performance: 性能数据字典
        prefix: 文件名前缀
        
    Returns:
        str: 图像相对路径
    """
    # 提取响应度数据
    responsivity_data = performance.get('responsivity_data', [])
    
    if responsivity_data:
        wavelengths = [point[0] for point in responsivity_data]
        responsivities = [point[1] for point in responsivity_data]
    else:
        # 示例数据
        wavelengths = list(range(400, 1601, 50))
        responsivities = [0.1 + 0.5 * (1 - abs(w - 1000) / 600) for w in wavelengths]
    
    # 创建折线图
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="1000px", height="600px"))
        .add_xaxis([str(w) for w in wavelengths])
        .add_yaxis(
            "Responsivity",
            responsivities,
            is_smooth=True,
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(type_="max", name="最大值")]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Detector Spectral Response",
                subtitle=f"Quantum Efficiency: {performance.get('quantum_efficiency', 'N/A')}%" if 'quantum_efficiency' in performance else ""
            ),
            xaxis_opts=opts.AxisOpts(name="Wavelength (nm)", type_="category"),
            yaxis_opts=opts.AxisOpts(name="Responsivity (A/W)"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
        )
    )
    
    output_path = f'static/images/{prefix}performance.html'
    line.render(output_path)
    
    return output_path
