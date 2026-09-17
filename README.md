# 龍門石窟北魏紀年題記分析平台

## 啟動

macOS 安裝 Python 3.10 以上後，雙擊「啟動平台.command」，以 Chrome 開啟 http://127.0.0.1:4180 。已建置來源 Excel 的153筆完整資料為 v0001。

- 全文輸入支援 AND、OR、NOT、括號、雙引號及反斜線跳脫。每次執行繼續縮小結果。
- 左側選擇後分類，勾選後按確認。同欄多值 OR、跨欄 AND。
- 分類值旁筆數可直接回查；重新查詢清除全部條件。
- 版本管理可瀏覽、比較及設為現行版；比較逐欄列出前後值。
- 單機按「匯入修訂版」選擇 Excel，成功後建立下一版本。警告可於版本驗證紀錄查看。
- 「備份」產生 backups/ 下的 ZIP；還原前自動保存現有資料。
- 「建立網路版」輸出 public-build/；將該目錄內容上傳一般靜態主機即可，尚未自動發布。公開版無管理寫入功能。
- 雙擊「停止平台.command」或使用畫面停止服務按鈕。

## GitHub Pages 發布

執行「建立網路版」後，將程式與 `public-build/` 提交並推送至 `main`。GitHub Actions 會把 `public-build/` 發布至 GitHub Pages；原始 Excel、`workspace-data/` 與 `backups/` 已由 `.gitignore` 排除。

## 模組導航

全文支援行內 Tag：左侧可切換 Metadata／Tag，Tag 依 term 的不重複文件數分類。搜尋與高亮只使用正文，完整資料內可展開「原始標記全文」。Tag 顯示名稱設定於 `tools/config.py` 的 `tagFacets`，對應 `SPEC/Data_SPEC.md` 5.3；資料版本保存設定快照。解析與資料包介面見 `tools/MARKUP.md`。

| 修改內容 | 入口 | 測試 |
|---|---|---|
| 資料欄位與用途 | tools/config.py | tests/test_packages.py |
| Excel解析驗證 | tools/importer.py | tests/test_packages.py |
| 全文Tag解析及分類設定 | tools/markup.py、tools/config.py | tests/test_markup.py |
| Metadata／Tag類別識別與文案 | web/core/facet-fields.js | tests/tag.test.js |
| 版本/備份/靜態建置 | tools/packages.py | tests/test_packages.py |
| 全文語法與索引 | web/core/query.js | tests/core.test.js |
| 後分類與排序 | web/core/facets.js | tests/core.test.js |
| 累積條件 | web/core/state.js | tests/core.test.js |
| 讀取與版本比較 | web/core/data.js | 瀏覽器驗證 |
| A版外觀 | web/app.js、web/style.css | 瀏覽器驗證 |
| 本機管理及啟停 | tools/manage.py | 本機驗證 |

執行測試：`npm test`、`python3 -m unittest discover -s tests -p 'test_*.py'`。

## Excel 全文批次標記工具

`tools/text_tagger.py` 依標記清單活頁簿的工作表順序與資料列順序，標記目標 Excel 的指定文字欄位。第一次使用時先安裝 Excel 函式庫：

```bash
python3 -m pip install -r requirements-tagger.txt
```

再修改程式開頭的 `TARGET_FILE`、`TARGET_SHEET`、`TARGET_COLUMN`、`TAG_LIST_FILE` 與 `OUTPUT_FILE`，然後執行：

```bash
python3 tools/text_tagger.py
```

也可用命令列暫時覆寫設定，例如：

```bash
python3 tools/text_tagger.py \
  --target-file metadataExample/來源.xlsx \
  --target-column 題記錄文 \
  --tag-list-file metadataExample/標記清單.xlsx \
  --output-file outputs/標記結果.xlsx
```

標記清單每個工作表都以第一列為標題，支援 `tagName`、`tagVal`、`@term`、`@RefId`；欄名不區分大小寫。`tagName` 與 `tagVal` 必填，另兩欄選填。程式需要 Python 3.10 以上及 `openpyxl`，輸出一定另存新檔，不會覆寫來源 Excel。

## 實作選擇

使用原生瀏覽器模組、Python標準函式庫；無套件下載、外部字型或後端資料庫。查詢完全在瀏覽器執行，本機服務僅提供檔案及本機管理操作。管理請求需要隨啟動產生的權杖並驗證來源。

空白尾列依資料規格現有建議忽略；已確認的必填欄位採阻擋驗證。原始儲存值不改寫；多值只在分類索引中拆分。包含公式的Excel會要求轉成確定值，避免讀取過期快取。

公開版不包含原始Excel；包含已發布版本的全部28欄。使用者條件保存在記憶體，重新整理即清除。

## 尚待完成的發布驗收

50,000筆/50 MB最大規模效能與120秒版本比較目標尚須實機量測，目前不能視為已通過完整規格驗收。

「更新程式」接受含 release.json 校驗清單的前端 ZIP 更新包，更新前自動備份，替換失敗回退，前版程式保存在 previous-release/。此更新器只更新 web/；Python 管理工具升級仍需人工替換並重新啟動。自動備份保留最近5份，手動備份不自動刪除。

已通過真實153筆資料的核心測試、版本與備份測試，以及 Chrome 桌面／手機尺寸的查詢、後分類、完整欄位與無結果操作測試。詳見 IMPLEMENTATION_STATUS.md。
