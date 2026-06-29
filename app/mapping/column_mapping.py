from typing import Dict, Any

# Task1：逐筆交易比對（Excel(A) 欄名 -> PDF(A) record 欄位）
_TASK1_MAPPING = {
    "Action": "Action",
    "Date": "trade_date",
    "Ticker": "Ticker",
    "Px": "price",
    "#": "#"
}

# Task2：Accumulator 合約層級比對（Excel(B) 欄名 -> PDF(B) record 欄位）
# 只列出 PDF(B)（合約確認書）真正會提供的欄位。
# KO(%)/(G/No G)/Notional Amt O/S/Cost Px/KO Px/Days Traded.../# Shares Traded/
# Amt Traded.../UnRzled Gain.../%.../#shs.../price today forumula/Remarks/「#」
# 這些欄位不是單份合約確認書 PDF 能提供的（人工填寫、Excel 公式計算，或需要其他頁
# 合約條款才能取得），不放在這個 mapping 裡，維持 Excel 原值不被覆蓋。
_TASK2_MAPPING = {
    "AQ / DQ": "aq_dq",
    "Date": "trade_date",
    "Daily Shares (DS)": "daily_shares",
    "Step-Up DS": "step_up_daily_shares",
    "Strike (%)": "strike_pct",
    "Tenor": "tenor",
    "Initial Px / Spot Px": "initial_price",
    "Strike Px": "accumulating_forward_price",
    "KO Date / Expiry Date": "expiration_date",
}


def get_pdf_column_mapping(task: Any) -> Dict[str, str]:
    """回傳 PDF 與 Excel 的欄位對應關係，依 task["task_name"] 分流。"""
    task_name = task.get("task_name", "") if isinstance(task, dict) else ""
    if task_name.startswith("task2"):
        return _TASK2_MAPPING
    return _TASK1_MAPPING
