# SCHEMA.md — 頁面範本與範例

This file documents the exact page templates and examples for the wiki. Reference `AGENTS.md` for the overall schema. All page content is Traditional Chinese.

## 頁面類型速覽

| 類型 | 位置 | frontmatter `type` |
|---|---|---|
| 類別頁 | `wiki/<類別>.md` | `category` |
| 主題頁 | `wiki/<類別>/<主題>.md` | `topic` |
| 開示頁 | `wiki/<類別>/<CODE>.md` | `source` |
| 概念頁 | `wiki/概念/<概念>.md` | `concept` |
| 問答頁 | `wiki/問答/<題目>.md` | `answer` |

## 範本

### 類別頁 (category)

```markdown
---
type: category
tags: [淨土]
sources: 90
updated: 2026-08-04
---

# 淨土五經一論

此類別涵蓋淨土宗的根本經論：…（一段綜合說明）。

## 主題

- [[無量壽經]] — …
- [[阿彌陀經]] — …

## 開示一覽

依 [[index|索引]] 與 [[raw-manifest|原始清單]] 查閱。
```

### 主題頁 (topic)

```markdown
---
type: topic
category: 淨土五經一論
tags: [無量壽經]
updated: 2026-08-04
---

# 無量壽經

經義大要：…

## 開示

- [[02-034]] — …
- [[02-041]] — …

## 相關概念

- [[概念/阿彌陀佛]] [[概念/四十八願]]
```

### 開示頁 (source) — 每個系列一頁

```markdown
---
type: source
category: 認識佛教
topic: 認識佛陀教育
code: 17-001
title: 認識佛教
date: 1991/12
place: 美國邁阿密
pages: 7
raw: doc/認識佛教/認識佛陀教育/17-001/
media: [mp3]
tags: [認識佛教, 佛教教育]
created: 2026-08-04
updated: 2026-08-04
---

# 認識佛教（17-001）

- **檔名**：17-001
- **類別**：認識佛教 / 認識佛陀教育
- **集數**：共 7 集
- **日期地點**：1991/12，美國邁阿密
- **原始路徑**：`doc/認識佛教/認識佛陀教育/17-001/`

## 概要

一段話說明本開示講什麼。

## 重點

- 要點一〔17-001-0001〕
- 要點二

## 相關概念

- [[概念/佛教教育]] [[概念/三皈依]]

## 相關頁面

- [[認識佛陀教育]] — 主題頁
- [[17-005]] — 同題材其他開示

## 原始資料與影音

- **原始資料夾**：[GitHub](https://github.com/l2yao/amtb/tree/main/amtb/doc/認識佛教/認識佛陀教育/17-001)（doc/pdf/md 全部集數）
- **第一集** 〔17-001-0001〕：文字 [md](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0001.md) · [doc](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0001.doc) · [pdf](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0001.pdf) ｜ 影音 [mp3](https://tw4.hwadzan.info/redirect/media/mp3/17/17-001/17-001-0001.mp3)
- **末集** 〔17-001-0007〕：文字 [md](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0007.md) · [doc](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0007.doc) · [pdf](https://github.com/l2yao/amtb/blob/main/amtb/doc/認識佛教/認識佛陀教育/17-001/0007.pdf) ｜ 影音 [mp3](https://tw4.hwadzan.info/redirect/media/mp3/17/17-001/17-001-0007.mp3)

> 媒體類型由該系列於分類 JSON 的旗標決定：`mp3`（mp3=1）、`himp4`（himp4=1）、`mp4`（mp4=1 且 himp4=0）。少數系列旗標雖為 1，影音檔仍可能 404（例如 18-023）。
```

### 概念頁 (concept)

```markdown
---
type: concept
tags: [戒律]
sources: [16-001, 17-001]
updated: 2026-08-04
---

# 五戒

定義：…

## 各開示的講法

- [[16-001]] — 強調 …
- [[17-001]] — …

## 要點

- …

## 相關概念

- [[概念/十善]] [[概念/三皈依]]

## 引用出處

- 〔16-001〕〔17-001〕
```

### 問答頁 (answer)

```markdown
---
type: answer
tags: [比較]
updated: 2026-08-04
---

# 標題

**問題**：…

**回答**：…

## 出處

- 〔CODE〕
- [[17-001]]

## 相關頁面

- …
```

## 命名與連結規則

- 檔名：概念/主題用中文名；開示頁用代碼（如 `17-001.md`）。檔名不含空格。
- 內部連結：`[[頁面名]]`；開示頁連結代碼 `[[17-001]]`；概念頁用 `[[概念/念佛]]`。
- 引用：`〔17-001〕` 引用整個系列，`〔17-001-0001〕` 引用特定一集。
- 開示頁需附 `## 原始資料與影音` 區段，提供：原始資料夾的 GitHub 連結（`https://github.com/l2yao/amtb/tree/main/amtb/doc/<路徑>`）、第一集與末集的文字（`md`/`doc`/`pdf`，GitHub blob：`https://github.com/l2yao/amtb/blob/main/amtb/doc/<路徑>/<NNNN>.<副檔名>`）與影音連結。中文路徑在 URL 中須以 UTF-8 百分比編碼。
- 影音連結格式（AMTB CDN 重新導向，`parent` 為 `code` 之首段，如 `17-001` → `17`；`NNNN` 為集數補零至四位）：
  - mp3：`https://tw4.hwadzan.info/redirect/media/mp3/{parent}/{code}/{code}-{NNNN}.mp3`
  - himp4：`https://tw4.hwadzan.info/redirect/media/himp4/{parent}/{code}/{code}-{NNNN}.mp4`
  - mp4：`https://tw4.hwadzan.info/redirect/media/mp4/{parent}/{code}/{code}-{NNNN}.mp4`
  - 依 frontmatter `media` 列出之類型取用。

## 前導資料 (frontmatter)

可用欄位：

| 欄位 | 說明 | 例 |
|---|---|---|
| `type` | 頁面類型 | `source` |
| `category` | 類別（中文） | `認識佛教` |
| `topic` | 主題（中文） | `認識佛陀教育` |
| `code` | 系列代碼 | `17-001` |
| `title` | 開示題目 | `認識佛教` |
| `date` | 日期，`YYYY-M` 或 `YYYY-MM-DD` | `1991/12` → `1991-12` |
| `place` | 地點 | `美國邁阿密` |
| `pages` | 集數 | `7` |
| `raw` | 原始資料夾路徑 | `doc/認識佛教/認識佛陀教育/17-001/` |
| `media` | 可取得的影音類型（取自分類 JSON 旗標） | `[mp3]` / `[mp3, himp4]` |
| `tags` | 標籤 | `[淨土, 阿彌陀佛]` |
| `created` / `updated` | 日期 | `2026-08-04` |
| `sources` | 概念頁引用的系列代碼 | `[16-001, 17-001]` |

## 長度規則

- 單頁約 150 行內；超過則拆分。
- 概念頁、問答頁隨內容演化而更新，不需每次重寫。
