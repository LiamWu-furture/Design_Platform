import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode


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
    使用 pyecharts 生成水平层叠结构图（从底到顶）
    
    Args:
        layers: 层结构列表
        prefix: 文件名前缀
        
    Returns:
        str: 图像相对路径
    """
    from pyecharts.charts import Bar
    
    # 提取数据（反转顺序，从底层到顶层）
    layers_reversed = list(reversed(layers))
    layer_labels = []
    thicknesses = []
    colors_list = []
    
    # 定义专业配色方案
    color_palette = [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
        '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#73a9c6'
    ]
    
    total_thickness = sum(layer['thickness'] for layer in layers)
    
    # 构建数据
    for i, layer in enumerate(layers_reversed):
        name = layer.get('name', layer['material'])
        material = layer['material']
        thickness = layer['thickness']
        
        # 构建标签：层名 + 材料 + 厚度
        if name != material:
            label = f"{name}\n{material}\n{thickness}nm"
        else:
            label = f"{material}\n{thickness}nm"
        
        layer_labels.append(label)
        thicknesses.append(thickness)
        colors_list.append(color_palette[i % len(color_palette)])
    
    # 创建水平条形图
    bar = (
        Bar(init_opts=opts.InitOpts(
            theme=ThemeType.LIGHT,
            width="100%",
            height=f"{max(600, len(layers) * 80)}px",  # 根据层数动态调整高度
            bg_color="#ffffff"
        ))
        .add_xaxis(layer_labels)
        .add_yaxis(
            series_name="Thickness",
            y_axis=thicknesses,
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                formatter="{c} nm",
                font_size=13,
                font_weight="bold",
                color="#333"
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode("""
                    function(params) {{
                        var colorList = {colors};
                        return colorList[params.dataIndex];
                    }}
                """.format(colors=colors_list)),
                border_color="#fff",
                border_width=2
            ),
        )
        .reversal_axis()  # 反转坐标轴，变成水平条形图
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Detector Layer Structure",
                subtitle=f"Total: {total_thickness} nm | {len(layers)} Layers | Bottom → Top",
                title_textstyle_opts=opts.TextStyleOpts(font_size=22, font_weight="bold"),
                subtitle_textstyle_opts=opts.TextStyleOpts(font_size=14, color="#666"),
                pos_left="center"
            ),
            xaxis_opts=opts.AxisOpts(
                name="Thickness (nm)",
                name_location="middle",
                name_gap=35,
                name_textstyle_opts=opts.TextStyleOpts(font_size=14, font_weight="bold"),
                axislabel_opts=opts.LabelOpts(font_size=12),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=0.2))
            ),
            yaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    font_size=12,
                    font_weight="bold",
                    interval=0,  # 显示所有标签
                    rotate=0
                ),
                axisline_opts=opts.AxisLineOpts(is_show=True),
                axisTick_opts=opts.AxisTickOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="shadow",
                formatter="{b}<br/>Thickness: {c} nm",
                background_color="rgba(50,50,50,0.9)",
                border_color="#333",
                border_width=1,
                textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=13)
            ),
            legend_opts=opts.LegendOpts(is_show=False),  # 隐藏图例，信息已在坐标轴显示
        )
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
    
    # 获取性能参数
    qe = performance.get('quantum_efficiency', 'N/A')
    qe_type = performance.get('quantum_efficiency_type', '')
    dark_current = performance.get('dark_current', 'N/A')
    wavelength_range = performance.get('wavelength_range', [min(wavelengths), max(wavelengths)])
    
    # 构建副标题
    subtitle_parts = []
    if qe != 'N/A':
        subtitle_parts.append(f"{qe_type} {qe}%" if qe_type else f"QE: {qe}%")
    if dark_current != 'N/A':
        subtitle_parts.append(f"Dark Current: {dark_current} A")
    subtitle_parts.append(f"Range: {wavelength_range[0]}-{wavelength_range[1]} nm")
    subtitle = " | ".join(subtitle_parts)
    
    # 创建折线图
    line = (
        Line(init_opts=opts.InitOpts(
            theme=ThemeType.LIGHT,
            width="100%",
            height="600px",
            bg_color="#ffffff"
        ))
        .add_xaxis([str(w) for w in wavelengths])
        .add_yaxis(
            series_name="Responsivity",
            y_axis=responsivities,
            is_smooth=True,
            symbol="circle",
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=3, color="#5470c6"),
            areastyle_opts=opts.AreaStyleOpts(
                opacity=0.2,
                color="#5470c6"
            ),
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Peak", symbol_size=60),
                ],
                label_opts=opts.LabelOpts(font_size=12, font_weight="bold")
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Average")],
                linestyle_opts=opts.LineStyleOpts(type_="dashed", color="#91cc75")
            ),
            itemstyle_opts=opts.ItemStyleOpts(
                color="#5470c6",
                border_color="#fff",
                border_width=2
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Detector Spectral Response",
                subtitle=subtitle,
                title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight="bold"),
                subtitle_textstyle_opts=opts.TextStyleOpts(font_size=13, color="#666")
            ),
            xaxis_opts=opts.AxisOpts(
                name="Wavelength (nm)",
                name_location="middle",
                name_gap=35,
                name_textstyle_opts=opts.TextStyleOpts(font_size=14, font_weight="bold"),
                type_="category",
                axislabel_opts=opts.LabelOpts(font_size=11, rotate=45),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=0.2))
            ),
            yaxis_opts=opts.AxisOpts(
                name="Responsivity (A/W)",
                name_location="middle",
                name_gap=50,
                name_textstyle_opts=opts.TextStyleOpts(font_size=14, font_weight="bold"),
                axislabel_opts=opts.LabelOpts(font_size=11),
                splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=0.2))
            ),
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                axis_pointer_type="cross",
                formatter="Wavelength: {b} nm<br/>Responsivity: {c} A/W",
                background_color="rgba(50,50,50,0.9)",
                border_color="#333",
                border_width=1,
                textstyle_opts=opts.TextStyleOpts(color="#fff")
            ),
            legend_opts=opts.LegendOpts(
                pos_top="5%",
                pos_right="5%",
                textstyle_opts=opts.TextStyleOpts(font_size=12)
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    type_="slider",
                    range_start=0,
                    range_end=100,
                    pos_bottom="5%"
                ),
                opts.DataZoomOpts(type_="inside")
            ],
        )
    )
    
    output_path = f'static/images/{prefix}performance.html'
    line.render(output_path)
    
    return output_path
