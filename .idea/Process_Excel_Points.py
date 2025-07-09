import pandas as pd
from collections import defaultdict

def read_custom_points(file_path, point_coordinates):
    """
    从Excel文件中读取自定义位置的6个点坐标
    point_coordinates (list): 包含12个单元格位置的列表，格式为[x1_cell, y1_cell, x2_cell, y2_cell, ...]
    返回按纵坐标分组的点字典，格式为{y_value: [(x1, y), (x2, y)]}
    """
    if len(point_coordinates) != 12:
        raise ValueError("需要提供12个单元格位置（即6个点的横纵坐标）")

    df = pd.read_excel(file_path, header=None, sheet_name=0) # sheet是否需要指定？

    points = []

    for i in range(0, 12, 2):
        x_cell = point_coordinates[i]
        y_cell = point_coordinates[i+1]

        x = get_cell_value(df, x_cell)
        y = get_cell_value(df, y_cell)

        points.append((x, y))

    # 按纵坐标分组
    grouped_points = defaultdict(list)
    for point in points:
        x, y = point
        grouped_points[y].append((x, y))

    # 验证每组是否有两个点
    for y, points in grouped_points.items():
        if len(points) != 2:
            raise ValueError(f"纵坐标{y}的点数量不为2，请检查数据")

    return dict(grouped_points)

def get_cell_value(df, cell_ref):
    col_letter = cell_ref[0].upper()
    row_num = int(cell_ref[1:]) - 1 # 转换为0-based索引

    col_idx = ord(col_letter) - ord('A')
    return df.iloc[row_num, col_idx]

if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/数据点.xlsx"

    # 自定义点坐标位置
    # 格式为[x1_cell, y1_cell, x2_cell, y2_cell, ...]
    custom_points = [
        'A2', 'B2',  # 第一个点
        'A3', 'B3',  # 第二个点
        'A4', 'B4',  # 第三个点
        'A5', 'B5',  # 第四个点
        'A6', 'B6',  # 第五个点
        'A7', 'B7'   # 第六个点
    ]

    try:
        grouped_points = read_custom_points(file_path, custom_points)

        print("按纵坐标分组的数据点:")
        for y, points in grouped_points.items():
            print(f"纵坐标 {y}: ")
            for point in points:
                print(f"({point[0]}, {point[1]})")
            print()

        print("\n数据:")
        print(grouped_points)

    except Exception as e:
        print(f"{e}")