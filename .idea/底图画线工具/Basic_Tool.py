from PIL import Image, ImageDraw
import fitz # PyMuPDF
import numpy as np
import io
import cv2 # OpenCV
import os

import Process_Excel_Points as pep

def detect_grid_boundaries(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # 强化网格线
    kernel_h = np.ones((1, 15), np.uint8) # 水平线核
    kernel_v = np.ones((15, 1), np.uint8) # 垂直线核

    # 强化水平和垂直线
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_h, iterations=2)
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_v, iterations=2)

    # 合并水平和垂直线
    grid_lines = cv2.bitwise_or(horizontal, vertical)

    # 查找轮廓
    contours, _ = cv2.findContours(grid_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    best_rect = None

    for cnt in contours:
        # 近似多边形
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 寻找矩形轮廓
        if len(approx) == 4:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_rect = cv2.boundingRect(cnt)

    x, y, w, h = best_rect

    # 裁剪出初始网格区域
    grid_roi = img[y:y+h, x:x+w]

    # 网格区域内检测线条
    grid_gray = cv2.cvtColor(grid_roi, cv2.COLOR_RGB2GRAY)
    grid_edges = cv2.Canny(grid_gray, 50, 150, apertureSize=3)

    # 霍夫变换检测线条
    # 降低threshold检测更多线条
    # 增加minLineLength忽略短线段（可能是文字笔画）
    lines = cv2.HoughLinesP(grid_edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)

    if lines is not None:
        # 收集所有线条的端点
        all_x = []
        all_y = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            all_x.extend([x1, x2])
            all_y.extend([y1, y2])

        if all_x and all_y:
            # 用分位数排除异常值
            sorted_x = sorted(all_x)
            sorted_y = sorted(all_y)

            # 取1%和99%分位数，排除过长线条的影响
            lower_idx_x = int(len(sorted_x) * 0.01)
            upper_idx_x = int(len(sorted_x) * 0.99)
            lower_idx_y = int(len(sorted_y) * 0.01)
            upper_idx_y = int(len(sorted_y) * 0.99)

            inner_x1 = sorted_x[lower_idx_x]
            inner_x2 = sorted_x[upper_idx_x]
            inner_y1 = sorted_y[lower_idx_y]
            inner_y2 = sorted_y[upper_idx_y]

            x = x + inner_x1
            y = y + inner_y1
            w = inner_x2 - inner_x1
            h = inner_y2 - inner_y1

    return (x, y, x + w, y + h)

def map_coordinates_to_image(pdf_path, points, x_range, y_range, output_path, base_image=None):
    """
    points格式[(x1, y1), (x2, y2), ...]
    x_range格式(x_min, x_max)
    y_range格式(y_min, y_max)
    base_image: 基于现有图像继续绘制
    """
    if base_image is None:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0) # TODO: 可以拓展加载pdf的指定页数的功能

        images = page.get_images(full=True)
        xref = images[0][0] # TODO: 选择一页中的某张图
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        full_img = Image.open(io.BytesIO(image_bytes))
    else:
        full_img = base_image.copy()

    if base_image is None:
        # 自动检测网格边界
        grid_bbox = detect_grid_boundaries(full_img)
        print(f"检测到的网格区域: {grid_bbox}")
    else:
        grid_bbox = getattr(full_img, 'grid_bbox', None)
        if grid_bbox is None:
            grid_bbox = detect_grid_boundaries(full_img)
            full_img.grid_bbox = grid_bbox

    # 裁剪网格
    x1, y1, x2, y2 = grid_bbox
    grid_img = full_img.crop((x1, y1, x2, y2))
    grid_width, grid_height = grid_img.size

    # 创建绘图对象
    draw = ImageDraw.Draw(grid_img)

    # 坐标映射
    def map_coord(x, y):
        # 将实际坐标映射到网格图像像素位置
        x_percent = (x - x_range[0]) / (x_range[1] - x_range[0])
        y_percent = (y - y_range[0]) / (y_range[1] - y_range[0])
        pixel_x = int(x_percent * grid_width)
        pixel_y = int((1 - y_percent) * grid_height)
        return pixel_x, pixel_y

    # 像素坐标
    pixel_points = []
    for point in points:
        px, py = map_coord(*point)
        pixel_points.append((px, py))

    # 顺时针连接所有点
    for i in range(len(pixel_points)):
        start_point = pixel_points[i]
        end_point = pixel_points[(i + 1) % len(pixel_points)]
        draw.line([start_point, end_point], fill="red", width=4) # TODO: 这里修改划线的颜色

    # 绘制点
    marker_radius = 3 # 点自身大小
    for i, point in enumerate(pixel_points):
        px, py = point
        bbox = [
            (px - marker_radius, py - marker_radius),
            (px + marker_radius, py + marker_radius)
        ]
        draw.ellipse(bbox, fill="red", outline="white")

    full_img_copy = full_img.copy()
    full_img_copy.paste(grid_img, (x1, y1))
    full_img_copy.grid_bbox = grid_bbox

    full_img_copy.save(output_path)
    print(f"结果已保存至: {output_path}")

    return full_img_copy

def mark_points_and_connect(pdf_path, points, x_range, y_range, output_path, base_image=None):
    """
    标注多个点并按纵坐标排序后连线
    points: [(x1, y1), (x2, y2), ...] (最多3个点)
    x_range: (min, max)
    y_range: (min, max)
    """
    if base_image is None:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0) # TODO: 可以拓展加载pdf的指定页数的功能

        images = page.get_images(full=True)
        xref = images[0][0] # TODO: 选择一页中的某张图
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        full_img = Image.open(io.BytesIO(image_bytes))
    else:
        full_img = base_image.copy()

    if base_image is None:
        # 自动检测网格边界
        grid_bbox = detect_grid_boundaries(full_img)
        print(f"检测到的网格区域: {grid_bbox}")
    else:
        grid_bbox = getattr(full_img, 'grid_bbox', None)
        if grid_bbox is None:
            grid_bbox = detect_grid_boundaries(full_img)
            full_img.grid_bbox = grid_bbox

    # 裁剪网格
    x1, y1, x2, y2 = grid_bbox
    grid_img = full_img.crop((x1, y1, x2, y2))
    grid_width, grid_height = grid_img.size

    # 创建绘图对象
    draw = ImageDraw.Draw(grid_img)

    # 坐标映射
    def map_coord(x, y):
        # 将实际坐标映射到网格图像像素位置
        x_percent = (x - x_range[0]) / (x_range[1] - x_range[0])
        y_percent = (y - y_range[0]) / (y_range[1] - y_range[0])
        pixel_x = int(x_percent * grid_width)
        pixel_y = int((1 - y_percent) * grid_height)
        return pixel_x, pixel_y

    # 映射所有点坐标
    pixel_points = [map_coord(x, y) for x, y in points]

    # 按纵坐标排序（从大到小）
    sorted_points = sorted(pixel_points, key=lambda p: p[1])

    # 绘制点之间的连线
    if len(sorted_points) > 1:
        for i in range(len(sorted_points) - 1):
            start_point = sorted_points[i]
            end_point = sorted_points[i + 1]
            draw.line([start_point, end_point], fill="red", width=2)

    # 绘制点
    marker_radius = 6 # 点自身大小
    for i, point in enumerate(pixel_points):
        px, py = point
        bbox = [
            (px - marker_radius, py - marker_radius),
            (px + marker_radius, py + marker_radius)
        ]
        draw.ellipse(bbox, fill="red", outline="white")

    full_img_copy = full_img.copy()
    full_img_copy.paste(grid_img, (x1, y1))
    full_img_copy.grid_bbox = grid_bbox

    full_img_copy.save(output_path)
    print(f"点标注结果已保存至: {output_path}")

    return full_img_copy

if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/数据点.xlsx"

    # 自定义点坐标位置
    # 格式为[x1_cell, y1_cell, x2_cell, y2_cell, ...]
    custom_points = [
        'A2', 'B2',  # 1
        'A3', 'B3',  # 2
        'A4', 'B4',  # 3
        'A5', 'B5',  # 4
        'A6', 'B6',  # 5
        'A7', 'B7'   # 6
    ]

    points = pep.read_custom_points(file_path, custom_points)

    pdf_path = "C:/Users/13438/Desktop/导出页面自 四川雅砻江孟底沟水电站水轮机模型初步试验报告.pdf"

    # 输入坐标轴范围
    x_axis_range = (100, 1000)
    y_axis_range = (55, 90)

    result_image = map_coordinates_to_image(
        pdf_path=pdf_path,
        points=points,
        x_range=x_axis_range,
        y_range=y_axis_range,
        output_path="结果.png"
    )