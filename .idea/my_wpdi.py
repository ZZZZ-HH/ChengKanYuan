import cv2
import numpy as np
from wpdi import WPDI

def extract_chart_data(image_path):
    """
    使用WebPlotDigitizer算法提取图表数据
    """
    # 图像预处理
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # 初始化WPDI
    digitizer = WPDI()

    # 设置坐标系（需根据实际图表调整）
    digitizer.set_axis_points(
        x1=(50, 400),  # 像素坐标 (X轴起点)
        x2=(450, 400), # 像素坐标 (X轴终点)
        y1=(50, 400),  # 像素坐标 (Y轴起点)
        y2=(50, 50)    # 像素坐标 (Y轴终点)
    )

    digitizer.set_calibration_values(
        x1_val=0,     # 实际值 (X轴起点)
        x2_val=10,    # 实际值 (X轴终点)
        y1_val=0,     # 实际值 (Y轴起点)
        y2_val=100    # 实际值 (Y轴终点)
    )

    # 提取数据（自动模式）
    digitizer.load_image(binary)
    data = digitizer.extract_data(auto_mode=True)

    return data

if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/导出页面自 四川雅砻江孟底沟水电站水轮机模型初步试验报告.pdf"
    # 使用示例
    data_points = extract_chart_data(file_path)
    print("提取的数据点:", data_points[:5])  # 显示前5个点

    # 可视化提取结果
    import matplotlib.pyplot as plt
    x = [p[0] for p in data_points]
    y = [p[1] for p in data_points]
    plt.scatter(x, y)
    plt.title("提取的数据点")
    plt.show()