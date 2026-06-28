import pandas as pd
from typing import Set, Tuple

from app.mapping.column_mapping import get_pdf_column_mapping
from app.mapping.unit_union import normalize_dataframes

KEY_COLUMNS = ["Action", "Date", "Ticker", "Px", "#"]


def compare_pdf_excel(pdf_df, excel_df, task) -> Tuple[Set, pd.DataFrame]:
    """
    比對 PDF 與 Excel 的關鍵欄位
    支援 Excel 為空或缺少欄位的情況
    """
    pdf_mapping = get_pdf_column_mapping(task)

    # ====================== PDF 欄位重命名 ======================
    rename_dict = {v: k for k, v in pdf_mapping.items()}
    pdf_df = pdf_df.rename(columns=rename_dict).copy()

    # ====================== 建立 PDF 的 _match_key ======================
    pdf_df["_match_key"] = pdf_df[KEY_COLUMNS].apply(tuple, axis=1)

    # ====================== [修改] 檢查 Excel 是否可用 ======================
    # 新增此段：判斷 Excel 是否為空，或是否缺少 KEY_COLUMNS 所需欄位
    excel_has_columns = not excel_df.empty and all(col in excel_df.columns for col in KEY_COLUMNS)

    if not excel_has_columns:
        # [修改] 當 Excel 為空或缺少必要欄位時，直接把 PDF 所有資料視為需新增
        print("⚠️ Excel 為空或缺少必要欄位，將把 PDF 所有資料視為需新增")
        missing_keys = set(pdf_df["_match_key"])
        return missing_keys, pdf_df
    # =====================================================================

    # ====================== Excel 有資料時正常比對 ======================
    excel_df, pdf_df = normalize_dataframes(excel_df, pdf_df, KEY_COLUMNS)

    excel_df["_match_key"] = excel_df[KEY_COLUMNS].apply(tuple, axis=1)
    pdf_df["_match_key"] = pdf_df[KEY_COLUMNS].apply(tuple, axis=1)

    excel_keys = set(excel_df["_match_key"])
    pdf_keys = set(pdf_df["_match_key"])
    missing_in_excel = pdf_keys - excel_keys

    print(f"Excel 共有 {len(excel_keys)} 筆唯一組合")
    print(f"PDF 共有 {len(pdf_keys)} 筆唯一組合")
    print(f"PDF 有但 Excel 沒有的組合：{len(missing_in_excel)} 筆")

    return missing_in_excel, pdf_df
