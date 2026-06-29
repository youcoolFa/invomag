# unit_union.py（建議使用此版本）
import pandas as pd
from typing import List, Tuple
from datetime import datetime


def normalize_dataframes(
    excel_df: pd.DataFrame,
    pdf_df: pd.DataFrame,
    key_columns: List[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    excel_df = excel_df.copy()
    pdf_df = pdf_df.copy()

    for col in key_columns:
        if col not in excel_df.columns or col not in pdf_df.columns:
            continue

        if col == "Date":
            # Excel: 20260414 → 14/Apr/26
            excel_df[col] = excel_df[col].apply(
                lambda x: _convert_excel_date_to_str(x) if pd.notna(x) else x
            )
            # PDF: 14-Apr-26 → 14/Apr/26
            pdf_df[col] = pdf_df[col].apply(
                lambda x: _normalize_pdf_date(x) if pd.notna(x) else x
            )
            continue

        # 其他欄位型態處理（維持原樣）
        excel_dtype = excel_df[col].dtype
        if pd.api.types.is_integer_dtype(excel_dtype):
            pdf_df[col] = pd.to_numeric(pdf_df[col], errors="coerce").astype("Int64")
        elif pd.api.types.is_float_dtype(excel_dtype):
            pdf_df[col] = pd.to_numeric(pdf_df[col], errors="coerce").round(4)
        elif pd.api.types.is_string_dtype(excel_dtype) or excel_dtype == object:
            pdf_df[col] = pdf_df[col].astype(str).str.strip()
        else:
            pdf_df[col] = pd.to_numeric(pdf_df[col], errors="coerce")

    return excel_df, pdf_df


def _convert_excel_date_to_str(date_val):
    # openpyxl 對有日期格式的儲存格會回傳 datetime 物件
    if isinstance(date_val, datetime):
        return date_val.strftime("%d/%b/%y")

    if isinstance(date_val, str):
        for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%d/%b/%y", "%d-%b-%y", "%d-%b-%Y"):
            try:
                return datetime.strptime(date_val, fmt).strftime("%d/%b/%y")
            except ValueError:
                continue
        return date_val

    # Excel 數字格式日期，例如 20260414 (YYYYMMDD)
    try:
        date_str = str(int(date_val))
        if len(date_str) == 8:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%d/%b/%y")
        return date_str
    except (ValueError, TypeError):
        return date_val


def _normalize_pdf_date(date_val):
    if isinstance(date_val, str):
        # Task1 PDF 日期為 2 位數年（14-Apr-26），Task2 Accumulator PDF 為 4 位數年（16-Mar-2026）
        for fmt in ("%d-%b-%y", "%d/%b/%y", "%d-%b-%Y", "%d/%b/%Y"):
            try:
                return datetime.strptime(date_val, fmt).strftime("%d/%b/%y")
            except ValueError:
                continue
    return date_val
