# pdf_main.py 修改後
from app.extraction.pdf.pdf_to_json import extract_pdf_to_json   # 改成絕對路徑
from app.extraction.pdf.json_to_df import (
    process_todays_settlement,
    process_future_settlement,
    process_aq_dq_ko
)
from app.task.task_mapping import (
    task1, task1_1, task2_700, task2_9988, task3_700, task3_9988)

# def main_pdf(pdf_path,output_path):
#     data = extract_pdf_to_json(pdf_path, output_path)
#     df = process_todays_settlement(data)
#     # df = process_future_settlement(data)
#     # df = process_aq_dq_ko(data)
#     return df

def main_pdf(pdf_path,output_path,task):
    data = extract_pdf_to_json(pdf_path, output_path)
    df = process_todays_settlement(data)
    task["pdf_today_settlement"](data)
    # df = process_future_settlement(data)
    # df = process_aq_dq_ko(data)
    return df


if __name__ == "__main__":
    from app.task.task_mapping import task1, task1_1
    task = task1_1
    pdf_path = task["pdf_path"]
    output_path = task["pdf_to_json"]
    df = main_pdf(pdf_path,output_path,task)