
import pdfplumber
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import re
from app.task.task_mapping import task1,task2_700

def extract_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """提取 PDF 內容，保留結構化資訊"""
    results = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            page_data = {
                "page": page_num,
                "width": page.width,
                "height": page.height,
                "text_blocks": [],
                "tables": []
            }

            # 提取帶位置的文字區塊
            words = page.extract_words()
            if words:
                text_blocks = []
                current_block = {"text": "", "x0": None, "top": None, "x1": None, "bottom": None}

                for word in words:
                    if current_block["x0"] is None:
                        current_block.update({
                            "text": word["text"],
                            "x0": word["x0"],
                            "top": word["top"],
                            "x1": word["x1"],
                            "bottom": word["bottom"]
                        })
                    else:
                        current_block["text"] += " " + word["text"]
                        current_block["x1"] = max(current_block["x1"], word["x1"])
                        current_block["bottom"] = max(current_block["bottom"], word["bottom"])

                if current_block["text"]:
                    text_blocks.append(current_block)

                page_data["text_blocks"] = text_blocks

            # 提取表格
            tables = page.extract_tables()
            for table in tables:
                page_data["tables"].append(table)

            page_data["full_text"] = page.extract_text() or ""
            results.append(page_data)

    return results


def save_to_json(data: List[Dict[str, Any]], output_path: str):
    """儲存為 JSON 檔案"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已輸出至：{output_path}")


def extract_pdf_to_json(pdf_path, output_path):
    # 如果有傳參數就用參數，沒有就用預設路徑

    if len(sys.argv) >= 2:
        pdf_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "extracted_output.json"

    else:
        # === 在這裡設定你常用的 PDF 路徑 ===
        # pdf_path = "/Users/mac/python project/invomag/app/extraction/pdf/input/pdf/cash_mgmt_report-16APR2026without_symbol.pdf"
        # output_path = "/Users/mac/python project/invomag/app/extraction/pdf/output/json/init.json"
        print("未偵測到命令列參數，使用預設路徑執行...")

    if not Path(pdf_path).exists():
        print(f"錯誤: 找不到檔案 {pdf_path}")
        sys.exit(1)

    # 後面的提取程式碼保持不變...
    print(f"開始處理: {pdf_path}")
    data = extract_pdf(pdf_path)

    save_to_json(data, output_path)

    return data



if __name__ == "__main__":
    task = task2_700
    pdf_path = task["pdf_path"]
    output_path = task["pdf_to_json"]
    extract_pdf_to_json(pdf_path, output_path)
