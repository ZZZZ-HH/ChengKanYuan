import fitz # PyMuPDF
import cv2
import numpy as np
import easyocr
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
import re
import tempfile

class CoordinateSystem:
    def __init__(self):
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        # 刻度
        self.x_ticks = {}
        self.y_ticks = {}

        # 图中原点x、y坐标
        self.origin = None

        # x轴终点x、y坐标
        self.x_end = None

        # y轴终点x、y坐标
        self.y_end = None

        self.image = None
        self.image_path = None
        self.reader = easyocr.Reader(['en']) # easyOCR

    def set_x_range(self, x_min, x_max):
        self.x_min = x_min
        self.x_max = x_max

    def set_y_range(self, y_min, y_max):
        self.y_min = y_min
        self.y_max = y_max

    def add_x_tick(self, value, position):
        self.x_ticks[value] = position

    def add_y_tick(self, value, position):
        self.y_ticks[value] = position

    def set_axes(self, origin, x_end, y_end):
        self.origin = origin
        self.x_end = x_end
        self.y_end = y_end

    def set_image(self, image, image_path):
        self.image = image
        self.image_path = image_path

    def is_valid(self):
        return (self.x_min is not None and self.x_max is not None and
                self.y_min is not None and self.y_max is not None and
                self.origin is not None and self.x_end is not None and
                self.y_end is not None and self.image is not None)

    def image_to_data(self, x_img, y_img):
        """图坐标->数据坐标"""
        if abs(self.x_end[1] - self.origin[1]) > 1 or abs(self.y_end[0] - self.origin[0]) > 1:
            print("非正交坐标系")
            return None, None

        # x轴方向比例
        x_ratio = (x_img - self.origin[0]) / (self.x_end[0] - self.origin[0])
        x_data = self.x_min + x_ratio * (self.x_max - self.x_min)

        # y轴方向比例（图坐标系y轴向下）
        y_ratio = (self.origin[1] - y_img) / (self.origin[1] - self.y_end[1])
        y_data = self.y_min + y_ratio * (self.y_max - self.y_min)

        return x_data, y_data

    def data_to_image(self, x_data, y_data):
        """数据坐标->图坐标"""
        if abs(self.x_end[1] - self.origin[1]) > 1 or abs(self.y_end[0] - self.origin[0]) > 1:
            print("非正交坐标系")
            return None, None

        # x轴方向比例
        x_ratio = (x_data - self.x_min) / (self.x_max - self.x_min)
        x_img = self.origin[0] + x_ratio * (self.x_end[0] - self.origin[0])

        # y轴方向比例（图坐标系y轴向下）
        y_ratio = (y_data - self.y_min) / (self.y_max - self.y_min)
        y_img = self.origin[1] - y_ratio * (self.origin[1] - self.y_end[1])

        return x_img, y_img

    def save(self, filename):
        """保存坐标系统"""
        if not self.is_valid():
            raise ValueError("坐标系统不完整")

        data = {
            "x_min": self.x_min,
            "x_max": self.x_max,
            "y_min": self.y_min,
            "y_max": self.y_max,
            "origin": self.origin,
            "x_end": self.x_end,
            "y_end": self.y_end,
            "x_ticks": self.x_ticks,
            "y_ticks": self.y_ticks,
            "image_path": self.image_path
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"坐标系统已保存到 {filename}")
        # TODO: 不保存额外文件，直接缓存下来，用完就扔

    @classmethod
    def load(cls, filename):
        """从文件加载坐标系统"""
        with open(filename, 'r') as f:
            data = json.load(f)

        coord_system = cls()
        coord_system.set_x_range(data["x_min"], data["x_max"])
        coord_system.set_y_range(data["y_min"], data["y_max"])
        coord_system.set_axes(data["origin"], data["x_end"], data["y_end"])

        # 刻度
        for value, pos in data["x_ticks"].items():
            coord_system.add_x_tick(float(value), tuple(pos))
        for value, pos in data["y_ticks"].items():
            coord_system.add_y_tick(float(value), tuple(pos))

        # 加载图
        if os.path.exists(data["image_path"]):
            coord_system.image = cv2.imread(data["image_path"])
            coord_system.image_path = data["image_path"]
            print(f"图已从 {data['image_path']} 加载")
        else:
            print(f"图 {data['image_path']} 未找到")

        return coord_system

def extract_image_from_pdf(pdf_path, output_dir="output", page_num=0, dpi=300):
    """从PDF中提取图并保存"""
    # TODO: 不保存图
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    page = doc[page_num] # 自定义图所在页数

    # 高分辨率图
    zoom = 3.0 # 放大3倍
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    # 转换为numpy数组
    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

    # 转换为RGB格式
    if pix.n == 4: # 包含alpha通道
        image = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    else:
        image = img_array

    # 保存图
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    image_path = os.path.join(output_dir, f"{pdf_name}_page{page_num+1}.png")
    cv2.imwrite(image_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    print(f"PDF图已提取并保存到: {image_path}")
    return image, image_path

def auto_detect_axes(image, x_min, x_max, y_min, y_max):
    """自动检测坐标轴并识别刻度"""
    coord_system = CoordinateSystem()
    coord_system.set_x_range(x_min, x_max)
    coord_system.set_y_range(y_min, y_max)

    print("开始检测坐标轴")

    try:
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # 边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # 霍夫线变换检测直线
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

        if lines is None:
            raise ValueError("未检测到直线")

        # 水平和垂直线
        horizontal = []
        vertical = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi

            # 水平线(角度在-1到1度之间)
            if -1 < angle < 1:
                horizontal.append((x1, y1, x2, y2))

            # 垂直线(角度在89-91或-89--91度之间)
            elif (89 < angle < 91) or (-91 < angle < -89):
                vertical.append((x1, y1, x2, y2))

        if not horizontal:
            raise ValueError("未找到水平线")
        if not vertical:
            raise ValueError("未找到垂直线")

        # 最底部的水平线作为x轴（y坐标最大）
        x_axis = max(horizontal, key=lambda l: max(l[1], l[3]))
        x1, y1, x2, y2 = x_axis

        # 最左侧的垂直线作为y轴（x坐标最小）
        y_axis = min(vertical, key=lambda l: min(l[0], l[2]))
        x3, y3, x4, y4 = y_axis

        # 原点
        origin_x = x3 # y轴的x坐标
        origin_y = y1 # x轴的y坐标

        # 坐标轴
        coord_system.set_axes(
            (origin_x, origin_y),
            (x2, y2), # x轴终点
            (x4, y4) # y轴终点
        )

        print(f"坐标轴原点: ({origin_x:.1f}, {origin_y:.1f})")
        print(f"X轴: ({x1:.1f}, {y1:.1f}) -> ({x2:.1f}, {y2:.1f})")
        print(f"Y轴: ({x3:.1f}, {y3:.1f}) -> ({x4:.1f}, {y4:.1f})")

        is_orthogonal = True
        if abs(y1 - y2) > 1: # x轴不水平
            print(f"X轴不水平 (y1={y1}, y2={y2}, 差值={abs(y1-y2):.2f})")
            is_orthogonal = False

        if abs(x3 - x4) > 1: # y轴不垂直
            print(f"Y轴不垂直 (x3={x3}, x4={x4}, 差值={abs(x3-x4):.2f})")
            is_orthogonal = False

        if not is_orthogonal:
            print("非正交坐标系，坐标转换可能不准确")

        # 提取x轴区域（坐标轴上方50像素的区域）
        x_axis_height = 50
        x_axis_roi = image[
                     max(0, int(origin_y) - x_axis_height):int(origin_y), # 高度，y轴
                     int(min(x1, x2)):int(max(x1, x2)) # 宽度，x轴
                     ]

        # 提取y轴区域（坐标轴左侧50像素的区域）
        y_axis_width = 50
        y_axis_roi = image[
                     int(min(y3, y4)):int(max(y3, y4)), # 高度，y轴
                     max(0, int(origin_x) - y_axis_width):int(origin_x) # 宽度，x轴
                     ]

        # x轴刻度
        print("x轴刻度")
        x_ticks = ocr_recognize_ticks(coord_system.reader, x_axis_roi, 'x')
        for value, pos in x_ticks.items():
            abs_x = origin_x + pos[0]
            abs_y = origin_y - 5 # 在x轴上方显示
            coord_system.add_x_tick(value, (abs_x, abs_y))
            print(f"x刻度: {value} @ ({abs_x:.1f}, {abs_y:.1f})")

        # y轴刻度
        print("y轴刻度")
        y_ticks = ocr_recognize_ticks(coord_system.reader, y_axis_roi, 'y')
        for value, pos in y_ticks.items():
            abs_x = origin_x + 5 # 在y轴右侧显示
            abs_y = origin_y + pos[1]
            coord_system.add_y_tick(value, (abs_x, abs_y))
            print(f"y刻度: {value} @ ({abs_x:.1f}, {abs_y:.1f})")

        # 在图上绘制坐标轴
        img_with_axes = image.copy()
        cv2.line(img_with_axes, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
        cv2.line(img_with_axes, (int(x3), int(y3)), (int(x4), int(y4)), (0, 255, 0), 3)
        cv2.circle(img_with_axes, (int(origin_x), int(origin_y)), 8, (255, 0, 0), -1)

        # 绘制刻度
        for value, (x, y) in coord_system.x_ticks.items():
            cv2.circle(img_with_axes, (int(x), int(y)), 4, (255, 0, 0), -1)
            cv2.putText(img_with_axes, f"{value:.1f}", (int(x), int(y)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        for value, (x, y) in coord_system.y_ticks.items():
            cv2.circle(img_with_axes, (int(x), int(y)), 4, (255, 0, 0), -1)
            cv2.putText(img_with_axes, f"{value:.1f}", (int(x), int(y)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(img_with_axes, cv2.COLOR_BGR2RGB))
        plt.title("检测到的坐标轴和刻度")
        plt.axis('off')
        plt.show()

        print("\n坐标信息:")
        print(f"X轴范围: {x_min} 到 {x_max}")
        print(f"Y轴范围: {y_min} 到 {y_max}")
        print(f"原点: ({origin_x:.1f}, {origin_y:.1f})")
        print(f"X轴终点: ({x2:.1f}, {y2:.1f})")
        print(f"Y轴终点: ({x4:.1f}, {y4:.1f})")
        print(f"识别到 {len(coord_system.x_ticks)} 个x刻度和 {len(coord_system.y_ticks)} 个y刻度")

        return coord_system

    except Exception as e:
        print(f"坐标轴检测失败: {str(e)}")
        return None

def ocr_recognize_ticks(reader, image):
    """easyOCR识别坐标轴刻度"""
    # 转换为灰度，增强对比度
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化处理
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 形态学操作去除小噪点
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # 反转图（白底黑字->黑底白字）
    inverted = cv2.bitwise_not(cleaned)

    # 保存临时图用于OCR
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_path = temp_file.name
        cv2.imwrite(temp_path, inverted)

    # easyOCR识别文本
    results = reader.readtext(temp_path)

    os.unlink(temp_path)

    recognized = {}
    for result in results:
        text = result[1]
        bbox = result[0]

        text = re.sub(r'[^0-9.]', '', text) # 移除非数字字符
        if not text or text.count('.') > 1:
            continue

        try:
            value = float(text)

            x_center = (bbox[0][0] + bbox[2][0]) / 2
            y_center = (bbox[0][1] + bbox[2][1]) / 2

            recognized[value] = (x_center, y_center)
        except ValueError:
            continue

    return recognized

def plot_data_on_image(coord_system, data_points, output_path="output/result.png"):
    """在图像上绘制数据点"""
    if not coord_system.is_valid():
        print("坐标系统不完整，无法绘制数据点")
        return

    try:
        # 复制原始图像
        img_with_points = coord_system.image.copy()

        # 绘制坐标轴
        origin_x, origin_y = coord_system.origin
        x_end_x, x_end_y = coord_system.x_end
        y_end_x, y_end_y = coord_system.y_end

        cv2.line(img_with_points, (int(origin_x), int(origin_y)),
                 (int(x_end_x), int(x_end_y)), (0, 0, 255), 2)
        cv2.line(img_with_points, (int(origin_x), int(origin_y)),
                 (int(y_end_x), int(y_end_y)), (0, 255, 0), 2)

        # 绘制Excel数据点
        point_count = 0
        for y_value, points in data_points.items():
            for x_value, y_value in points:
                # 将数据坐标转换为图像坐标
                x_img, y_img = coord_system.data_to_image(x_value, y_value)

                # 在图像上绘制点
                cv2.circle(img_with_points, (int(x_img), int(y_img)), 8, (0, 0, 255), -1)
                cv2.putText(img_with_points, f"({x_value:.1f}, {y_value:.1f})",
                            (int(x_img) + 10, int(y_img) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                point_count += 1

        # 保存结果
        cv2.imwrite(output_path, cv2.cvtColor(img_with_points, cv2.COLOR_RGB2BGR))
        print(f"\n已绘制 {point_count} 个数据点到图像: {output_path}")

        # 显示结果
        plt.figure(figsize=(12, 8))
        plt.imshow(cv2.cvtColor(img_with_points, cv2.COLOR_BGR2RGB))
        plt.title("带数据点的特性曲线")
        plt.axis('off')
        plt.show()

        return True

    except Exception as e:
        print(f"绘图失败: {str(e)}")
        return False