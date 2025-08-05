from PyQt5.QtCore import QObject, pyqtSignal

class BackendManager(QObject):
    model_changed = pyqtSignal(str) # 机组类型变化信号
    basic_params_changed = pyqtSignal(dict) # 电站基本参数变化信号
    tech_water_params_changed = pyqtSignal(dict) # 技术供水系统参数变化信号
    calculation_result_ready = pyqtSignal(dict) # 计算结果准备就绪

    def __init__(self):
        super().__init__()
        self.selected_model = ""
        self.basic_params = {}
        self.tech_water_params = {}
        self.calculation_results = {}

    def set_model(self, model_name):
        """机组类型"""
        self.selected_model = model_name
        self.model_changed.emit(model_name)

    def get_model(self):
        return self.selected_model

    def set_basic_params(self, params):
        """电站基本参数"""
        self.basic_params = params
        self.basic_params_changed.emit(params)
        # self.calculate_tech_water()

    def set_tech_water_param(self, key, value):
        """技术供水系统参数"""
        self.tech_water_params[key] = value

        self.calculate_tech_water()

    def calculate_tech_water(self):
        """技术供水系统计算"""
        results = {}

        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        """
        2.3 机组总用水量
        """
        total_calc = 0.0
        total_value = 0.0

        # 2.1
        for i in range(1, 5):
            calc_key = f"2.1.{i}.计算值"
            value_key = f"2.1.{i}.取值"

            calc_val = safe_float(self.tech_water_params.get(calc_key, 0))
            val_val = safe_float(self.tech_water_params.get(value_key, 0))

            total_calc += calc_val
            total_value += val_val

        # 2.2
        for i in range(1, 3):
            calc_key = f"2.2.{i}.计算值"
            value_key = f"2.2.{i}.取值"

            calc_val = safe_float(self.tech_water_params.get(calc_key, 0))
            val_val = safe_float(self.tech_water_params.get(value_key, 0))

            total_calc += calc_val
            total_value += val_val

        results["2.3.计算值"] = total_calc
        results["2.3.设计值"] = total_value

        # TODO 2.5只是确认设计值，有问题返回2.1和2.2修改，没问题往下
        # 计算2.5部分 (设计用水量)
        design_total = 0.0
        design_values = []

        for i in range(1, 7):  # 1-6项
            value_key = f"2.5.{i}"
            value = safe_float(self.tech_water_params.get(value_key, 0))
            design_values.append(value)
            design_total += value

        results["2.5.设计值"] = design_values
        results["2.5.总计"] = design_total

        # 存储计算结果
        self.calculation_results = results
        self.calculation_result_ready.emit(results)