class CoordinateSystem:
    def __init__(self):
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.origin = None # 原点坐标
        self.x_end = None # x轴终点
        self.y_end = None # y轴终点
        self.image = None # 原始图像
        self.image_path = None # 图像保存路径