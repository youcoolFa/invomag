import streamlit as st
import sys
from pathlib import Path
import tempfile

# ====================== 重要：加入路徑 ======================
sys.path.append(str(Path(__file__).resolve().parents[2]))

# ====================== 匯入模組 ======================
from app.task.task_mapping import get_task_template
from app.task1_main3 import main, OUTPUT_DIR

st.set_page_config(page_title="PDF vs Excel 比對工具", layout="wide")
st.title("📊 PDF vs Excel 比對與更新工具")


def save_uploaded_file(uploaded_file, temp_dir: Path) -> Path:
    """把 st.file_uploader 上傳的檔案寫入暫存路徑，回傳該路徑。"""
    dest_path = temp_dir / uploaded_file.name
    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest_path


def run_task(task_key: str, task_name: str, pdf_files, excel_file):
    """儲存上傳檔案、組裝 task、執行 main()，結果寫入該任務專屬的 session_state key。"""
    if any(f is None for f in pdf_files) or excel_file is None:
        st.error("請上傳所有必要的 PDF 與 Excel 檔案！")
        return

    with st.spinner("正在執行比對與更新，請稍候..."):
        try:
            temp_dir = Path(tempfile.mkdtemp())
            excel_path = save_uploaded_file(excel_file, temp_dir)
            pdf_paths = [save_uploaded_file(f, temp_dir) for f in pdf_files]

            task = get_task_template(task_name)
            task["excel"] = str(excel_path)
            task["pdf_path"] = str(pdf_paths[0])
            task["pdf_to_json"] = str(temp_dir / "extracted.json")

            result_path = main(task)

            result_key = f"{task_key}_result"
            if result_path:
                st.success("✅ 執行完成！已產生更新後的 Excel")
                st.session_state[result_key] = result_path
            else:
                st.success("✅ 執行完成！PDF 與 Excel 資料完全一致，無需更新。")
                st.session_state.pop(result_key, None)

        except Exception as e:
            st.error(f"執行失敗：{str(e)}")
            import traceback
            st.code(traceback.format_exc())


def render_download_button(task_key: str):
    """若該任務已有執行結果，顯示對應的下載按鈕。"""
    result_path = st.session_state.get(f"{task_key}_result")
    if not result_path:
        return
    st.divider()
    st.caption("📥 下載更新後的 Excel")
    with open(result_path, "rb") as f:
        st.download_button(
            label="下載",
            data=f,
            file_name=Path(result_path).name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key=f"{task_key}_download",
        )


def render_task_block(task_key: str, task_name: str, title: str, pdf_labels: list, supported: bool = True):
    """渲染一個任務區塊：N 個 PDF 上傳器 + 1 個 Excel 上傳器 + 執行按鈕 + 下載按鈕。"""
    with st.container(border=True):
        st.subheader(title)

        if not supported:
            st.info("🚧 尚未支援，敬請期待")

        pdf_files = [
            st.file_uploader(label, type=["pdf"], key=f"{task_key}_pdf_{i}", disabled=not supported)
            for i, label in enumerate(pdf_labels)
        ]
        excel_file = st.file_uploader(
            "上傳 Excel 檔案", type=["xlsx", "xls"], key=f"{task_key}_excel", disabled=not supported
        )

        st.caption(f"輸出：執行後自動產生於 `{OUTPUT_DIR.name}/`，可在下方下載")

        run_clicked = st.button(
            "🚀 執行" if supported else "Task3 尚未支援",
            key=f"{task_key}_run",
            type="primary",
            disabled=not supported,
        )

        if supported and run_clicked:
            run_task(task_key, task_name, pdf_files, excel_file)

        if supported:
            render_download_button(task_key)


# ====================== 三區塊並列 ======================
col1, col2, col3 = st.columns(3)

with col1:
    render_task_block(
        task_key="task1",
        task_name="task1",
        title="Task1：PDF(A) → Excel(A)",
        pdf_labels=["PDF(A) 結算報告"],
    )

with col2:
    render_task_block(
        task_key="task2",
        task_name="task2",
        title="Task2：PDF(B) → Excel(B)",
        pdf_labels=["PDF(B) Accumulator 合約確認書"],
    )

with col3:
    render_task_block(
        task_key="task3",
        task_name="task3",
        title="Task3：PDF(A) + PDF(B) → Excel(B)",
        pdf_labels=["PDF(A) 結算報告", "PDF(B) Accumulator 合約確認書"],
        supported=False,
    )
