import pandas as pd
from typing import Set, Tuple

from app.mapping.column_mapping import get_pdf_column_mapping
from app.mapping.unit_union import normalize_dataframes

KEY_COLUMNS = ["Action", "Date", "Ticker", "Px", "#"]

# Task2（Accumulator 合約層級比對）：只用 PDF(B) 真正能提供的欄位做比對鍵。
# KO(%)/Strike Px/Tenor/Days Traded.../# Shares Traded 是執行期間才累積或人工/公式維護的欄位，
# 單份合約確認書 PDF 不會提供，不應放進比對鍵，否則永遠比不對。
KEY_COLUMNS2 = [
    "AQ / DQ",
    "Date",
    "Daily Shares (DS)",
    "Step-Up DS",
]


def _get_key_columns(task) -> list:
    """依 task 類型回傳比對用的關鍵欄位組合。"""
    task_name = task.get("task_name", "") if isinstance(task, dict) else ""
    if task_name.startswith("task2"):
        return KEY_COLUMNS2
    return KEY_COLUMNS


def compare_pdf_excel(pdf_df, excel_df, task) -> Tuple[Set, pd.DataFrame]:
    """
    比對 PDF 與 Excel 的關鍵欄位
    支援 Excel 為空或缺少欄位的情況
    """
    pdf_mapping = get_pdf_column_mapping(task)
    key_columns = _get_key_columns(task)

    # ====================== PDF 欄位重命名 ======================
    rename_dict = {v: k for k, v in pdf_mapping.items()}
    pdf_df = pdf_df.rename(columns=rename_dict).copy()

    # ====================== 建立 PDF 的 _match_key ======================
    pdf_df["_match_key"] = pdf_df[key_columns].apply(tuple, axis=1)

    # ====================== 檢查 Excel 是否可用 ======================
    # Excel 為空，或缺少 key_columns 所需欄位時，直接把 PDF 所有資料視為需新增
    excel_has_columns = not excel_df.empty and all(col in excel_df.columns for col in key_columns)

    if not excel_has_columns:
        print("⚠️ Excel 為空或缺少必要欄位，將把 PDF 所有資料視為需新增")
        missing_keys = set(pdf_df["_match_key"])
        return missing_keys, pdf_df
    # =====================================================================

    # ====================== Excel 有資料時正常比對 ======================
    excel_df, pdf_df = normalize_dataframes(excel_df, pdf_df, key_columns)

    excel_df["_match_key"] = excel_df[key_columns].apply(tuple, axis=1)
    pdf_df["_match_key"] = pdf_df[key_columns].apply(tuple, axis=1)

    excel_keys = set(excel_df["_match_key"])
    pdf_keys = set(pdf_df["_match_key"])
    missing_in_excel = pdf_keys - excel_keys

    print(f"Excel 共有 {len(excel_keys)} 筆唯一組合")
    print(f"PDF 共有 {len(pdf_keys)} 筆唯一組合")
    print(f"PDF 有但 Excel 沒有的組合：{len(missing_in_excel)} 筆")

    return missing_in_excel, pdf_df
