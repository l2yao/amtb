# amtb

工具與資料庫，用於處理淨空老和尚（AMTB）教法。資料來源：https://www.amtb.tw/

本倉庫包含兩大部分：

## 1. LLM 維基（wiki）

以 Karpathy「LLM Wiki」模式維護的**傳統中文佛學知識庫**。LLM 負責讀取原始開示、撰寫並持續更新 wiki 頁面；人類負責選材、提問與審閱。

- **原始資料（不可更動）**：`amtb/doc/` — 10 大類別、1,269 個系列、約 15,000 頁開示文稿。
- **維基**：`amtb/wiki/` — LLM 撰寫的互相連結 Markdown 頁面（類別、主題、開示、概念、問答）。
- **綱要**：`AGENTS.md`（結構與工作流程）、`wiki/SCHEMA.md`（頁面範本）。

主要工作流程（詳見 `AGENTS.md`）：

- **ingest**：把一個系列整理成開示頁，並更新概念頁、索引與日誌。
- **query**：查維基並以引用（`〔17-001〕`）作答；好的問答會存回 `wiki/問答/`。
- **lint**：定期健康檢查（矛盾、孤兒頁、缺頁等）。

瀏覽方式：用 Obsidian 開啟 `amtb/wiki/`；導覽起點為 `wiki/README.md` 與 `wiki/index.md`。

## 2. 資料工具

`amtb/` 下的 Python 腳本，用於自 amtb.tw 抓取與轉檔：

```
# 從 amtb.tw 抓取分類選單（menu.json）
cd amtb
python fetch.py

# 依 menu.json + 範本產生網頁 markdown
python gen.py

# 下載 doc / pdf / mp3 / mp4 資料與影音
python download.py

# 將 .doc 轉成 .md（需 markitdown）
python doc_to_md.py
```

## 目錄結構

```
amtb/
  AGENTS.md            <- LLM 維基綱要（schema）
  amtb/
    doc/               <- 原始開示（唯讀）
    wiki/              <- LLM 維基（LLM 撰寫維護）
    fetch.py / gen.py / download.py / doc_to_md.py   <- 資料工具
  amtb_iptv/ budaedu/ google_classroom/ hwadzan/ youtube/   <- 其他資料
```
