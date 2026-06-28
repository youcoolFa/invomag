
# Project Structure

## 1. Extraction Data

### 1.1 Data Extraction
- 從 PDF 提取相關要處理的數據（轉換為 JSON 格式）
- 從 Excel 提取相關要處理的欄位（使用 Pandas DataFrame 格式）
- 建立 PDF 與 Excel 的原始資料來源對應關係

### 1.2 PDF JSON Processor
- 負責處理 PDF 轉換後的不規則 JSON 資料
- 找出資料中的 pattern（例如：交易描述、日期、金額、KO 狀態等）
- 將不規則資料轉換為有規律、結構化的格式
- 輸出標準化的 JSON 結構，方便後續處理

---

## 2. Task Manager

### 2.1 Task Definition
- 將整體工作拆分為多個獨立的 Task（Task 1、Task 2、... Task 10）
- 定義每個 Task 的工作內容與目標
- 每個 Task 應包含：
  - 負責的股票代碼（如 700.HK、9988.HK）
  - 處理的 Accumulator / Decumulator 類型
  - 預期輸出結果

### 2.2 Data Allocation
- 將 PDF 處理後的資料分配到對應的 Task
- 將 Excel 資料分配到對應的 Task
- 建立 Task 與資料來源的對應關係（可由 `path_management.py` 管理）

---

## 3. Mapping

### 3.1 Column Mapping
- 將 PDF 處理後的 Pandas 欄位，對應到 Excel 的 Pandas 欄位
- 建立欄位對應表（Mapping Table）

### 3.2 Data Calculation
- 執行必要的計算邏輯（如累計股數、Step-Up 計算、金額計算等）
- 處理 A1、a2、a3、a4 等變數的計算公式

### 3.3 Update Excel
- 將計算後的結果更新回 Excel 的 Pandas DataFrame
- 準備好要寫回 Excel 的最終資料

---

## 4. Looping

### 4.1 Task Looping
- 依序執行 Task 1、Task 2、... Task 10
- 每個 Task 獨立完成 Extraction → Mapping → Calculation → Update 流程

### 4.2 Output
- 完成所有 Task 後，輸出更新後的 Excel 檔案
- 更新指定的 Excel Sheet
- 可選擇是否產生 log 或執行結果報告

---

## 整體流程圖（建議）

