from PyQt5.QtCore import QObject, pyqtSignal
import math

def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

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
        print(self.tech_water_params)

    def calculate_tech_water(self):
        """技术供水系统计算"""
        results = {}

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

        """
        2.6 供水管设计
        """
        self.calculate_pipe_diameters(results)

        # 存储计算结果
        self.calculation_results = results
        self.calculation_result_ready.emit(results)
        print(results)

    def calculate_pipe_diameters(self, results):
        """计算所有供水管的管径"""
        # 获取总用水量和流速范围
        total_water = results.get("2.3.设计值", 0.0)
        vj_min = safe_float(self.tech_water_params.get("2.6.流速Vj.最小值", 1.0))
        vj_max = safe_float(self.tech_water_params.get("2.6.流速Vj.最大值", 3.0))

        # 计算总管径
        d_min_phys, d_max_phys = self.calculate_pipe_diameter(total_water, vj_min, vj_max)
        results.update({
            "2.6.1 总管.计算管径d.最小值": d_min_phys, # 物理最小管径
            "2.6.1 总管.计算管径d.最大值": d_max_phys, # 物理最大管径
        })

        kl_value = safe_float(self.tech_water_params.get("2.1.1.取值", 0))
        tl_value = safe_float(self.tech_water_params.get("2.1.2.取值", 0))
        sd_value = safe_float(self.tech_water_params.get("2.1.3.取值", 0))
        xd_value = safe_float(self.tech_water_params.get("2.1.4.取值", 0))
        sd2_value = safe_float(self.tech_water_params.get("2.2.1.取值", 0))
        zz_value = safe_float(self.tech_water_params.get("2.2.2.取值", 0))

        # 计算各分管管径
        results.update(self.calculate_sub_pipe("2.6.2 上导轴承油冷却器供水管", sd_value, vj_min, vj_max))
        results.update(self.calculate_sub_pipe("2.6.3 推力轴承油冷却器供水管", tl_value, vj_min, vj_max))
        results.update(self.calculate_sub_pipe("2.6.4 下导轴承油冷却器供水管", xd_value, vj_min, vj_max))
        results.update(self.calculate_sub_pipe("2.6.5 空气冷却器供水管", kl_value, vj_min, vj_max))
        results.update(self.calculate_sub_pipe("2.6.6 水导轴承冷却水供水管", sd2_value, vj_min, vj_max))
        results.update(self.calculate_sub_pipe("2.6.7 主轴密封供水供水管", zz_value, vj_min, vj_max))

    def calculate_pipe_diameter(self, flow, v_min, v_max):
        try:
            flow_m3s = flow / 3600.0

            # 最小管径（对应最大流速）
            d_min = 1.13 * math.sqrt(flow_m3s / v_max)

            # 最大管径（对应最小流速）
            d_max = 1.13 * math.sqrt(flow_m3s / v_min)

            return (d_min, d_max)
        except Exception as e:
            print(f"管径计算错误: {e}")

    def calculate_sub_pipe(self, pipe_key, flow, v_min, v_max):
        d_min_phys, d_max_phys = self.calculate_pipe_diameter(flow, v_min, v_max)

        return {
            f"{pipe_key}.计算管径d.最小值": d_min_phys, # 物理最小管径
            f"{pipe_key}.计算管径d.最大值": d_max_phys, # 物理最大管径
        }