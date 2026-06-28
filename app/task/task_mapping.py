# task_mapping.py
from pathlib import Path
from app.extraction.pdf.json_to_df import (
    process_todays_settlement,
    process_future_settlement,
    process_aq_dq_ko
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_task_template(task_name: str = "default"):
    """回傳一個乾淨的任務模板，供 Streamlit 動態填入路徑"""
    return {
        "task_name": task_name,
        "pdf_path": None,
        "pdf_to_json": None,
        "excel": None,
        "excel_to_csv": PROJECT_ROOT / "app" / "extraction" / "excel" / "output",
        "pdf_today_settlement": None,
    }


task1 = get_task_template("task1")
task1_1 = get_task_template("task1_1")
task2_700 = get_task_template("task2_700")
task2_9988 = get_task_template("task2_9988")
task3_700 = get_task_template("task3_700")
task3_9988 = get_task_template("task3_9988")
