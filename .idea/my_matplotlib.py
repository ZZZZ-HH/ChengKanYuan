import fitz  # PyMuPDF
import re

def extract_matplotlib_data(pdf_path):
    """
    从Matplotlib生成的PDF中提取数据
    """
    doc = fitz.open(pdf_path)
    data_points = []

    for page in doc:
        # 提取所有文本块
        text_blocks = page.get_text("dict")["blocks"]

        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()

                        # 识别数据标签 (例如: "(2.5, 3.2)")
                        if re.match(r"\(?[\d\.]+\s*,\s*[\d\.]+\)?", text):
                            # 提取坐标值
                            coords = re.findall(r"[\d\.]+", text)
                            if len(coords) == 2:
                                x, y = map(float, coords)
                                data_points.append((x, y))

    return data_points

if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/导出页面自 四川雅砻江孟底沟水电站水轮机模型初步试验报告.pdf"
    # 使用示例
    data = extract_matplotlib_data(file_path)
    print("提取的数据点:", data)