from typing import Dict, Any

# 目前所有 task 類型的欄位對應關係皆相同。
# 若未來不同 task 需要不同對應，請改為依 task["task_name"] 分流，
# 而不要依賴 pdf_path 檔名字串（Streamlit 上傳後的暫存路徑不含 task 名稱，會比對失敗）。
_DEFAULT_MAPPING = {
    "Action": "Action",
    "Date": "trade_date",
    "Ticker": "Ticker",
    "Px": "price",
    "#": "#"
}


def get_pdf_column_mapping(task: Any) -> Dict[str, str]:
    """回傳 PDF 與 Excel 的欄位對應關係。"""
    return _DEFAULT_MAPPING
