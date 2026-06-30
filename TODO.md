# Todo List

## Accumulator / Decumulator 任務追蹤

### 待辦事項

- [ ] **Task3 - DQ 真實資料驗證**
  - 目前僅使用合成 DQ 文字進行測試
  - 需取得含有 **DQ KO** 記錄的真實 PDF
  - 完成端對端驗證（解析 → 匹配 → Remarks 回填）

- [ ] **Task3 - 匹配邏輯最終確認**
  - 確認 `task3_main.py` 中的 `_MATCH_FIELDS` 已正確對應 `type` 欄位
  - 確認 `ko_lookup` 字典的鍵值建構與 `type` 欄位一致
  - 測試混合 AQ + DQ 的 Excel 回填情境

- [ ] **Task3 - 異常情況處理**
  - 評估是否需要在 `parse_aq_dq_ko()` 中加入 `type` 為 `None` 時的警告訊息

- [ ] **Task3 - 回歸測試**
  - 確認已存在 Remarks 的資料不會被覆寫
  - 測試多頁 PDF 的解析與回填行為

### 完成事項

- [X] **task3**
- [X] **test task1, task2**
  - task1 test (empty excel / excel X 2 pdf)
  - task2 test (empty excel / excel X pdf)
- [X] **task2 and task3 mapping**
  - task2 and task3 mapping with symbol
  - task2&3 excel column name
  - pdf extraction result
  - pdf column name
  - mapping with code
  - task1,2,3 UI done
- [X] **UI**
- [X] **mapping problem**
  - 日期格式先對齊
- [X] **test1.1**
  - test Apr 17 pdf (mapping_main hv problem)
  - check the output
- [X] **mapping of task2**
  - checking task2 column of df pdf and df excel
  - mapping of the columns
  - check this 3 function again (json_to_df.py, column_mapping.py, main_pdf.py)
- [X] **1. task1_main2.py**
  - 把所有的 main 都串連起來
  - 測試 17 Apr 有否成功
  - 完成最後 todo 的日期條件
- [X] **1. Union units excel df and pdf df**
  - 統一 excel df 及 pdf df 的單位
  - 把 column mapping logic 從 task_mapping 中分離出來
  - 把 task_mapping 變成 mapping_main.py (column_mapping.py and unit_union.py)
- [X] **1. Rename Excel Tasks**
  - 重新命名 Excel 檔案中的任務名稱
  - 統一任務命名規則（例如：`Task1_700HK_AQ`、`Task2_9988HK_AQ` 等）
  - 更新所有相關的任務標籤（A1, A2, A3...）
- [X] **2. Task1 Manager (`task1_mapping.py`)**
  - 建立 Task 1 的專屬管理程式
  - 負責讀取 PDF 資料與 Excel 資料的路徑

### 備註

- 目前重點先處理 Task 1 的流程
- 所有路徑建議使用相對路徑或設定 config 統一管理
