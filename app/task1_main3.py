# task1_main3.py
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime

from app.extraction.pdf.pdf_main import main_pdf
from app.extraction.excel.excel_main import main_excel
from app.mapping.mapping_main import compare_pdf_excel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "final_output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

KEY_COLUMNS = ["Action", "Date", "Ticker", "Px", "#"]


def main(task):
    print("正在使用 mapping_main.py 進行比對...\n")

    if task.get("pdf_today_settlement") is None:
        from app.extraction.pdf.json_to_df import process_todays_settlement
        task["pdf_today_settlement"] = process_todays_settlement

    excel_path = Path(task["excel"])
    pdf_path = Path(task["pdf_path"])
    json_output_path = task["pdf_to_json"]

    # 讀取 PDF 與 Excel
    pdf_df = main_pdf(str(pdf_path), str(json_output_path), task)
    excel_df = main_excel([str(excel_path)])

    # ====================== 修改後的空值檢查 ======================
    if pdf_df.empty:
        print("⚠️ PDF 或 Excel 資料為空，無法進行比對")
        return None

    if excel_df.empty:
        print("⚠️ Excel 為空，但 PDF 有資料，將繼續新增")

    # 比對
    missing_keys, pdf_df = compare_pdf_excel(pdf_df, excel_df, task)

    print(f"\n需要新增的資料筆數：{len(missing_keys)}")

    # ====================== 修改重點 ======================
    if not missing_keys:
        print("✅ Excel 已包含 PDF 所有資料，無需更新。")
        return None   # [修改] 沒有差異就回傳 None

    # 取出要新增的資料
    to_add = pdf_df[pdf_df["_match_key"].isin(missing_keys)][KEY_COLUMNS].drop_duplicates().copy()

    print(f"\n發現 {len(to_add)} 筆需要新增的資料：")
    print(to_add)

    # ====================== 只有需要更新時才產生新檔案 ======================
    wb = load_workbook(excel_path)
    ws = wb.active

    # 從第2列開始寫入（假設第1列是標題）
    start_row = ws.max_row + 1
    for r_idx, row in enumerate(dataframe_to_rows(to_add, index=False, header=False), start_row):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    # 產生新的檔案名稱
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"Task2_Updated_{timestamp}.xlsx"
    new_file_path = OUTPUT_DIR / new_filename

    wb.save(new_file_path)
    wb.close()

    print(f"\n✅ 已產生更新後的 Excel：{new_file_path}")
    return str(new_file_path)   # [修改] 回傳新檔案路徑
