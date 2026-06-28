import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import shutil
import tempfile
import os
from datetime import datetime

# ====================== 重要：加入路徑 ======================
sys.path.append(str(Path(__file__).resolve().parents[2]))

# ====================== 匯入模組 ======================
from app.task.task_mapping import get_task_template
from app.task1_main3 import main
from app.extraction.pdf.json_to_df import process_todays_settlement

st.set_page_config(page_title="PDF vs Excel 比對工具", layout="wide")
st.title("📊 PDF vs Excel 比對與更新工具")

# ====================== 檔案上傳區 ======================
col1, col2 = st.columns(2)

with col1:
    uploaded_excel = st.file_uploader("上傳 Excel 檔案", type=["xlsx", "xls"])

with col2:
    uploaded_pdf = st.file_uploader("上傳 PDF 檔案", type=["pdf"])

# ====================== Run 按鈕 ======================
if st.button("🚀 Run 比對與更新", type="primary"):
    if not uploaded_excel or not uploaded_pdf:
        st.error("請同時上傳 Excel 和 PDF 檔案！")
    else:
        with st.spinner("正在執行比對與更新，請稍候..."):
            try:
                # 建立暫存資料夾
                temp_dir = Path(tempfile.mkdtemp())

                # 儲存上傳的檔案
                excel_path = temp_dir / uploaded_excel.name
                pdf_path = temp_dir / uploaded_pdf.name

                with open(excel_path, "wb") as f:
                    f.write(uploaded_excel.getbuffer())

                with open(pdf_path, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())

                # ====================== 建立 task ======================
                task = get_task_template()
                task["excel"] = str(excel_path)
                task["pdf_path"] = str(pdf_path)
                task["pdf_today_settlement"] = process_todays_settlement

                # ====================== 執行主程式 ======================
                # [修改] 接收 main() 的回傳值
                result_path = main(task)

                if result_path:
                    # 有更新時才顯示成功訊息與儲存路徑
                    st.success("✅ 執行完成！已產生更新後的 Excel")
                    st.session_state["updated_excel_path"] = result_path
                else:
                    # 沒有差異時不產生檔案，也不顯示下載按鈕
                    st.success("✅ 執行完成！PDF 與 Excel 資料完全一致，無需更新。")
                    # 清除之前可能存在的下載路徑
                    if "updated_excel_path" in st.session_state:
                        del st.session_state["updated_excel_path"]

            except Exception as e:
                st.error(f"執行失敗：{str(e)}")
                import traceback
                st.code(traceback.format_exc())

# ====================== 下載區 ======================
if "updated_excel_path" in st.session_state:
    st.divider()
    st.subheader("📥 下載更新後的 Excel")

    with open(st.session_state["updated_excel_path"], "rb") as f:
        st.download_button(
            label="下載更新後的 Excel",
            data=f,
            file_name=Path(st.session_state["updated_excel_path"]).name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
