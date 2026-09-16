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

| 修改內容 | 入口 | 測試 |
|---|---|---|
| 資料欄位與用途 | tools/config.py | tests/test_packages.py |
| Excel解析驗證 | tools/importer.py | tests/test_packages.py |
| 版本/備份/靜態建置 | tools/packages.py | tests/test_packages.py |
| 全文語法與索引 | web/core/query.js | tests/core.test.js |
| 後分類與排序 | web/core/facets.js | tests/core.test.js |
| 累積條件 | web/core/state.js | tests/core.test.js |
| 讀取與版本比較 | web/core/data.js | 瀏覽器驗證 |
| A版外觀 | web/app.js、web/style.css | 瀏覽器驗證 |
| 本機管理及啟停 | tools/manage.py | 本機驗證 |

執行測試：`npm test`、`python3 -m unittest discover -s tests -p 'test_*.py'`。

## 實作選擇

使用原生瀏覽器模組、Python標準函式庫；無套件下載、外部字型或後端資料庫。查詢完全在瀏覽器執行，本機服務僅提供檔案及本機管理操作。管理請求需要隨啟動產生的權杖並驗證來源。

空白尾列依資料規格現有建議忽略；已確認的必填欄位採阻擋驗證。原始儲存值不改寫；多值只在分類索引中拆分。包含公式的Excel會要求轉成確定值，避免讀取過期快取。

公開版不包含原始Excel；包含已發布版本的全部28欄。使用者條件保存在記憶體，重新整理即清除。

## 尚待完成的發布驗收

50,000筆/50 MB最大規模效能與120秒版本比較目標尚須實機量測，目前不能視為已通過完整規格驗收。

「更新程式」接受含 release.json 校驗清單的前端 ZIP 更新包，更新前自動備份，替換失敗回退，前版程式保存在 previous-release/。此更新器只更新 web/；Python 管理工具升級仍需人工替換並重新啟動。自動備份保留最近5份，手動備份不自動刪除。

已通過真實153筆資料的核心測試、版本與備份測試，以及 Chrome 桌面／手機尺寸的查詢、後分類、完整欄位與無結果操作測試。詳見 IMPLEMENTATION_STATUS.md。
