import json
import pandas as pd
from pathlib import Path
from app.extraction.pdf.pattern_recon import (
    parse_settlement_records,
    parse_future_settlement,
    parse_aq_dq_ko,
    parse_accumulator_pdf_text
)
# from pdf_to_json import extract_pdf_to_json


# ====================== 路徑設定 ======================
# JSON_PATH = Path("/Users/mac/python project/invomag/app/extraction/pdf/output/json/init.json")
OUTPUT_DIR = Path(__file__).resolve().parent / "output" / "csv"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_fields_to_csv(df: pd.DataFrame, filename: str):
    """儲存 DataFrame 為 CSV"""
    # OUTPUT_DIR = task["pdf_to_json"]
    if df.empty:
        print(f"⚠️ 沒有資料可輸出：{filename}")
        return
    csv_path = OUTPUT_DIR / filename
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 已輸出 CSV：{csv_path}")
    print(f"   共 {len(df)} 列 × {len(df.columns)} 欄\n")


# ====================== 三個處理函數 ======================

def process_todays_settlement(data) -> pd.DataFrame:
    # if not JSON_PATH.exists():
    #     print(f"找不到檔案: {JSON_PATH}")
    #     return pd.DataFrame()
    #
    # with open(JSON_PATH, "r", encoding="utf-8") as f:
    #     data = json.load(f)

    full_text = data[0]["full_text"]
    print("=== 開始解析 Today’s settlement ===\n")

    records = parse_settlement_records(full_text)

    if records:
        print(f"成功解析 {len(records)} 筆交易\n")
        df = pd.DataFrame(records)                    # ← 直接轉 DataFrame
        save_fields_to_csv(df, "today_settlement_fields.csv")
        return df
    else:
        print("沒有解析到任何交易紀錄\n")
        return pd.DataFrame()


def process_future_settlement(data) -> pd.DataFrame:
    # if not JSON_PATH.exists():
    #     print(f"找不到檔案: {JSON_PATH}")
    #     return pd.DataFrame()

    # with open(JSON_PATH, "r", encoding="utf-8") as f:
    #     data = json.load(f)

    full_text = data[0]["full_text"]
    print("=== 開始解析 Future Settlement ===\n")

    records = parse_future_settlement(full_text)
    if records:
        print(f"成功解析 {len(records)} 筆交易\n")
        df = pd.DataFrame(records)                    # ← 直接轉 DataFrame
        save_fields_to_csv(df, "future_settlement_fields.csv")
        return df
    else:
        print("沒有解析到任何交易紀錄\n")
        return pd.DataFrame()


def process_aq_dq_ko(data) -> pd.DataFrame:
    # if not JSON_PATH.exists():
    #     print(f"找不到檔案: {JSON_PATH}")
    #     return pd.DataFrame()

    # with open(JSON_PATH, "r", encoding="utf-8") as f:
    #     data = json.load(f)

    full_text = data[0]["full_text"]
    print("=== 開始解析 AQ/DQ KO ===\n")

    records = parse_aq_dq_ko(full_text)
    if records:
        print(f"成功解析 {len(records)} 筆交易\n")
        df = pd.DataFrame(records)                    # ← 直接轉 DataFrame
        save_fields_to_csv(df, "aq_dq_ko_fields.csv")
        return df
    else:
        print("沒有解析到任何交易紀錄\n")
        return pd.DataFrame()


def process_accumulator(data) -> pd.DataFrame:
    full_text = data[0]["full_text"]
    print("=== 開始解析 Accumulator 合約 ===\n")

    records = parse_accumulator_pdf_text(full_text)
    if records:
        print(f"成功解析 {len(records)} 筆合約\n")
        df = pd.DataFrame(records)
        save_fields_to_csv(df, "accumulator_fields.csv")
        return df
    else:
        print("沒有解析到任何合約資料\n")
        return pd.DataFrame()


# ====================== Task -> PDF 解析函數 註冊表 ======================
# 新增 task 類型時，只需在這裡登記對應的解析函數，不需要修改 pdf_main.py。
TASK_PARSERS = {
    "task1": process_todays_settlement,
    "task2": process_accumulator,
}


def get_pdf_parser_for_task(task) -> callable:
    """依 task["task_name"] 前綴查表，回傳對應的 PDF 解析函數。"""
    task_name = task.get("task_name", "") if isinstance(task, dict) else ""
    for prefix, parser in TASK_PARSERS.items():
        if task_name.startswith(prefix):
            return parser
    raise ValueError(f"找不到 task_name='{task_name}' 對應的 PDF 解析函數")


# if __name__ == "__main__":
#     df1 = process_todays_settlement(data)
#     df2 = process_future_settlement(data)
#     df3 = process_aq_dq_ko(data)
#
#     print("\n=== Today’s settlement ===")
#     print(df1)
#     print("\n=== Future Settlement ===")
#     print(df2)
#     print("\n=== AQ/DQ KO ===")
#     print(df3)
