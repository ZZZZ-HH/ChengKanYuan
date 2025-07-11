import pdfplumber
import re
import matplotlib.pyplot as plt
import numpy as np

def extract_chart_labels(pdf_path):
    """
    提取图表中的轴标签和刻度值（修正版）
    """
    axis_labels = {"x": [], "y": []}
    tick_values = {"x": [], "y": []}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]
            page_height = page.height

            # 获取所有文本对象及其位置
            words = page.extract_words(
                x_tolerance=5,
                y_tolerance=5,
                keep_blank_chars=False,
                use_text_flow=True
            )

            print(f"页面高度: {page_height}")
            print(f"找到 {len(words)} 个文本对象")
            # 可视化文本位置（调试用）
            visualize_text_positions(words, page_height)

            for word in words:
                text = word["text"].strip()

                # 使用正确的键名获取位置信息
                top = word["top"]
                bottom = word["bottom"]
                left = word["x0"]
                right = word["x1"]

                # 计算文本高度（用于识别标签）
                text_height = bottom - top

                # 1. 识别轴标签 (通常较大且位于轴末端)
                if text_height > 10:  # 较大的文本通常是标签
                    if left < 50:  # 左侧位置 -> Y轴
                        axis_labels["y"].append(text)
                    elif top > page_height - 50:  # 底部位置 -> X轴
                        axis_labels["x"].append(text)

                # 2. 识别刻度值 (通常为数字且靠近轴线)
                elif re.match(r"^-?\d*\.?\d+$", text):  # 匹配数字
                    try:
                        value = float(text)
                        # Y轴刻度：位于左侧且高度在中间区域
                        if left < 100 and 50 < top < page_height - 50:
                            tick_values["y"].append(value)
                        # X轴刻度：位于底部
                        elif top > page_height - 50:
                            tick_values["x"].append(value)
                    except ValueError:
                        pass  # 忽略转换失败的情况

    except Exception as e:
        print(f"处理PDF时出错: {str(e)}")

    return axis_labels, tick_values

def visualize_text_positions(words, page_height):
    """
    可视化文本位置（用于调试）
    """
    plt.figure(figsize=(10, 12))

    # 绘制页面边界
    plt.plot([0, 600], [0, 0], 'k-', lw=1)  # 上边界
    plt.plot([0, 600], [page_height, page_height], 'k-', lw=1)  # 下边界
    plt.plot([0, 0], [0, page_height], 'k-', lw=1)  # 左边界

    # 绘制所有文本位置
    for i, word in enumerate(words):
        x = (word["x0"] + word["x1"]) / 2
        y = (word["top"] + word["bottom"]) / 2

        # 标记位置
        plt.plot(x, y, 'bo', markersize=3)
        plt.text(x, y, f'{i}:{word["text"]}', fontsize=8)

    plt.title("PDF文本位置可视化 (用于调试)")
    plt.xlabel("X位置")
    plt.ylabel("Y位置")
    plt.gca().invert_yaxis()  # PDF坐标系原点在左上角
    plt.grid(True, alpha=0.3)
    plt.savefig("text_positions_debug.png")
    plt.close()
    print("已保存文本位置可视化图: text_positions_debug.png")

# 使用示例
if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/导出页面自 四川雅砻江孟底沟水电站水轮机模型初步试验报告.pdf"
    # 提取标签和刻度
    axis_labels, tick_values = extract_chart_labels(file_path)

    print("\n提取结果:")
    print(f"X轴标签: {axis_labels['x']}")
    print(f"Y轴标签: {axis_labels['y']}")
    print(f"X轴刻度值: {sorted(tick_values['x'])}")
    print(f"Y轴刻度值: {sorted(tick_values['y'])}")

    # 可视化结果
    if tick_values["x"] and tick_values["y"]:
        plt.figure(figsize=(8, 6))
        plt.plot(tick_values["x"], tick_values["y"], 'ro-')
        plt.xlabel(axis_labels["x"][0] if axis_labels["x"] else "X轴")
        plt.ylabel(axis_labels["y"][0] if axis_labels["y"] else "Y轴")
        plt.title("提取的刻度值关系图")
        plt.grid(True)
        plt.savefig("extracted_ticks_plot.png")
        print("已保存刻度关系图: extracted_ticks_plot.png")