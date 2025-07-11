import pdfplumber
import pandas as pd

def extract_tables_from_pdf(pdf_path):
    """
    从PDF中提取所有表格数据
    """
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取当前页所有表格
            tables = page.extract_tables({
                "vertical_strategy": "lines",
                "horizontal_strategy": "lines"
            })

            for table in tables:
                # 转换为DataFrame
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

    return all_tables

if __name__ == "__main__":
    file_path = "C:/Users/13438/Desktop/导出页面自 四川雅砻江孟底沟水电站水轮机模型初步试验报告.pdf"
    # 使用示例
    tables = extract_tables_from_pdf(file_path)
    for i, table in enumerate(tables):
        table.to_csv(f"table_{i}.csv", index=False)
        print(f"提取表格 {i}:\n", table.head())