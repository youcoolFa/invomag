import re
from typing import List, Dict, Any

# ====================== Pattern 集中定義 ======================

pattern_today = (
    r"(\d+\.HK)"                        # 股票代號
    r"(?:\s+AQ)?"                       # 可選的 AQ
    r"\s*-\s*BOT\s+"                    # BOT
    r"([\d,]+)\s+shares\s+@"            # 股數
    r"\s*HKD\s+([\d.]+)\s+"             # 價格
    r"(?:-\s*KO\s+)?"                   # 可選的 - KO
    r"HKD\s+\(([\d,.-]+)\)\s+"          # 總金額
    r"(\d{2}-[A-Za-z]{3}-\d{2})\s+"     # Trade Date
    r"(\d{2}-[A-Za-z]{3}-\d{2})"        # Settlement Date
)

pattern_future = (
    r"(\d+\.HK)"                        # 股票代號
    r"(?:\s+AQ)?"                       # 可選 AQ
    r"\s*-\s*BOT\s+"                    # BOT
    r"([\d,]+)\s+shares\s+@"            # 股數
    r"\s*HKD\s+([\d.]+)\s+"             # 價格
    r"HKD\s+\(([\d,.-]+)\)\s+"          # 總金額
    r"(\d{2}-[A-Za-z]{3}-\d{2})\s+"     # Trade Date
    r"(\d{2}-[A-Za-z]{3}-\d{2})"        # Settlement Date
)

pattern_ko = (
    r"(\d+\.HK)"                        # 股票代號
    r"(?:\s+AQ)?"                       # 可選 AQ
    r"\s*-\s*BOT\s+"                    # BOT
    r"([\d,]+)\s+shares\s+@"            # 股數
    r"\s*HKD\s+([\d.]+)\s+"             # 價格
    r"-\s*KO\s+"                        # - KO（必有）
    r"HKD\s+\(([\d,.-]+)\)\s+"          # 總金額
    r"(\d{2}-[A-Za-z]{3}-\d{2})\s+"     # KO Date
    r"(\d{2}-[A-Za-z]{3}-\d{2})"        # Settlement Date
)

PATTERNS_ACCUMULATOR = {
    "Trade Date": (
        r"Trade Date\s*:\s*"                    # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Expiration Date": (
        r"Expiration Date\s*:\s*"               # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Termination Date": (
        r"Termination Date\s*:\s*"              # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Shares": (
        r"Shares\s*:\s*"                        # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Bloomberg Ticker": (
        r"Bloomberg Ticker\s*:\s*"              # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Buyer of Shares": (
        r"Buyer of Shares\s*:\s*"               # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Seller of Shares": (
        r"Seller of Shares\s*:\s*"              # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Maximum Number of Scheduled Trading Days": (
        r"Maximum Number of Scheduled Trading Days\s*:\s*"   # 欄位名稱
        r"(\d+)"                                             # 擷取數字
    ),
    "Guaranteed Period End Date": (
        r"Guaranteed Period End Date\s*:\s*"    # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
    "Daily Number of Shares (DS)": (
        r"Daily Number of Shares \(DS\)\s*:\s*" # 欄位名稱
        r"(\d+)"                                # 擷取數字
    ),
    "Step-up Daily Number of Shares (St-DS)": (
        r"Step-up Daily Number of Shares \(St-DS\)\s*:\s*"  # 欄位名稱
        r"(\d+)"                                            # 擷取數字
    ),
    "Maximum Number of Nominal Shares": (
        r"Maximum Number of Nominal Shares\s*:\s*"          # 欄位名稱
        r"([\d,]+)"                                         # 擷取數字（含逗號）
    ),
    "Initial Price": (
        r"Initial Price\s*:\s*HKD\s*"           # 欄位名稱 + 貨幣單位
        r"([\d.]+)"                             # 擷取價格
    ),
    "Accumulating Forward Price (AFP)": (
        r"Accumulating Forward Price \(AFP\)\s*:\s*HKD\s*"  # 欄位名稱 + 貨幣單位
        r"([\d.]+)"                                         # 擷取價格
    ),
    "Closing Price": (
        r"Closing Price\s*:\s*"                 # 欄位名稱
        r"(.+?)(?:\n|$)"                        # 擷取值
    ),
}




def parse_settlement_records(
    text: str,
    source: str = "Today’s settlement"
) -> List[Dict[str, Any]]:
    """解析 Today’s settlement 區段（含 KO 判斷）"""
    records = []

    section_match = re.search(
        r"Today’s settlement:.*?(?=Deposit\(s\) maturing today:)",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if not section_match:
        return records

    content = section_match.group(0)

    for m in re.finditer(pattern_today, content):
        ko_flag = "KO" if "- KO" in m.group(0) else None

        record = {
            "Ticker": m.group(1).replace(".HK", ""),   # ← 已移除 .HK
            "type": "Accumulator" if "AQ" in m.group(0) else "Normal",
            "Action": "Buy",
            "#": int(m.group(2).replace(",", "")),
            "price": float(m.group(3)),
            "total_amount": float(m.group(4).replace(",", "")),
            "trade_date": m.group(5),
            "settlement_date": m.group(6),
            "ko": ko_flag,
        }
        records.append(record)

    return records


def parse_future_settlement(
    text: str,
    source: str = "Future Settlement"
) -> List[Dict[str, Any]]:
    """解析 Future Settlement 區段"""
    records = []

    section_match = re.search(
        r"Future Settlement:.*?(?=AQ/\s*DQ\s*KO:)",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if not section_match:
        return records

    content = section_match.group(0)

    for m in re.finditer(pattern_future, content):
        ko_flag = "KO" if "- KO" in m.group(0) else None

        record = {
            "Ticker": m.group(1).replace(".HK", ""),   # ← 已移除 .HK
            "type": "Accumulator" if "AQ" in m.group(0) else "Normal",
            "Action": "Buy",
            "#": int(m.group(2).replace(",", "")),
            "price": float(m.group(3)),
            "total_amount": float(m.group(4).replace(",", "")),
            "trade_date": m.group(5),
            "settlement_date": m.group(6),
            "ko": ko_flag,
        }
        records.append(record)

    return records


def parse_aq_dq_ko(
    text: str,
    source: str = "AQ/DQ KO"
) -> List[Dict[str, Any]]:
    """解析 AQ/DQ KO 區段"""
    records = []

    section_match = re.search(
        r"AQ/\s*DQ\s*KO:.*?(?=No of shares)",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if not section_match:
        return records

    content = section_match.group(0)

    for m in re.finditer(pattern_ko, content):
        ko_flag = "KO" if "- KO" in m.group(0) else None

        record = {
            "Ticker": m.group(1).replace(".HK", ""),   # ← 已移除 .HK
            "type": "Accumulator" if "AQ" in m.group(0) else "Normal",
            "Action": "Buy",
            "#": int(m.group(2).replace(",", "")),
            "price": float(m.group(3)),
            "total_amount": float(m.group(4).replace(",", "")),
            "Date": m.group(5),
            "settlement_date": m.group(6),
            "ko": ko_flag,
        }
        records.append(record)

    return records


def parse_accumulator_pdf_text(text: str) -> List[Dict[str, Any]]:
    """
    解析 Accumulator PDF 內容，回傳 List[Dict] 格式
    """
    records = []
    data = {}

    for key, pattern in PATTERNS_ACCUMULATOR.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # 型態轉換
            if key in ["Maximum Number of Scheduled Trading Days",
                       "Daily Number of Shares (DS)",
                       "Step-up Daily Number of Shares (St-DS)"]:
                value = int(value)
            elif key in ["Initial Price", "Accumulating Forward Price (AFP)"]:
                value = float(value)
            elif key == "Maximum Number of Nominal Shares":
                value = int(value.replace(",", ""))
            data[key] = value

    if data:
        record = {
            "Ticker": data.get("Bloomberg Ticker", "").replace(".HK", ""),
            "type": "Accumulator",
            "Action": "Buy" if data.get("Buyer of Shares") else None,
            "#": data.get("Daily Number of Shares (DS)"),
            "price": data.get("Initial Price"),
            "total_amount": None,
            "trade_date": data.get("Trade Date"),
            "settlement_date": data.get("Expiration Date"),
            "expiration_date": data.get("Expiration Date"),
            "termination_date": data.get("Termination Date"),
            "initial_price": data.get("Initial Price"),
            "accumulating_forward_price": data.get("Accumulating Forward Price (AFP)"),
            "daily_shares": data.get("Daily Number of Shares (DS)"),
            "step_up_daily_shares": data.get("Step-up Daily Number of Shares (St-DS)"),
            "max_nominal_shares": data.get("Maximum Number of Nominal Shares"),
            "ko": None,
        }
        records.append(record)

    return records



# ====================== 使用範例 ======================
if __name__ == "__main__":
    # 假設這是你從 PDF 提取出來的 raw text
    raw_text = """Trade Date : 16-Mar-2026
    Expiration Date : 16-Mar-2027
    ...
    Initial Price : HKD 563.0000
    Accumulating Forward Price (AFP) : HKD 503.6035 ..."""

    result = parse_accumulator_pdf_text(raw_text)

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
