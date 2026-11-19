# 經銷線上訂貨系統：AI 交接文件

> 給接手的 AI：這份文件描述艾盟仕（EMERS GROUP）批發事業處四套經銷線上訂貨系統的完整現況。讀完這份，再讀範本 repo 的程式碼，就能接手維護、修改或複製新品牌。
> 文件更新：2026-11-19 14:30（Asia/Taipei，Grok Bot；DSTC、WAAC 現況見第 9 節）。以 GitHub repo 最新 commit 為準；文件和程式碼衝突時，相信程式碼，並回報差異。

## 0. 先知道這些

- 負責人：Marc Wang（王柏棛），批發事業處業務經理。公司帳號 `marc_wang@emers.com`（Google Workspace），GitHub 帳號 `marcwang13`。
- 溝通：繁體中文（台灣），直接講重點，文字不要有 AI 腔。
- 四套系統**程式碼幾乎一樣**，只差商品資料、品牌色、名稱字串和 localStorage key。後端 `Code.gs` 四套之間約差 20 行（品牌色、Excel 檔名、寄件名稱，另有健康檢查文字、訂單頁標題、信件主旨與內文中的品牌名）；複製新品牌時以 `diff` 比對範本逐行改。
- 範本是 SUN DAY RED FW27（`sdr-fw27-order`）。新功能先在範本做，再同步到其他三套。
- 不要做的事：不輸入任何登入密碼、不幫人建帳號、不在網站或給客戶的檔案放供貨價或外幣價。需要授權、建 repo、驗證碼的步驟交給 Marc 本人。

## 0.5 多個 AI 輪流維護（同步規則，一定要照做）

Marc 同時用 Claude 和 Grok Bot 維護這四套系統，一次只會有一邊在改。目的是其中一邊額度用完時，另一邊可以直接接手，而且換電腦也一樣。

1. **GitHub repo 是唯一正本。** 本機不留任何非 repo 的修改；開工前一定先 `git pull`（或重新 clone）拿 main 最新版。
2. **改完一定推回 main。** 不留沒合併的分支或只改在本機的東西。
3. **後端 `Code.gs` 一律先改 repo 裡的檔案**，commit 之後再貼到 Apps Script，部署用「管理部署作業 → 新版本」。不要只在 Apps Script 編輯器裡改，否則 repo 會落後。
4. **每次改動都在本文件第 11 節「變更紀錄」加一行**（日期、哪個 AI、哪套系統、改了什麼、commit），跟程式改動放在同一個 commit。
5. 本文件四個 repo 各放一份，內容相同。改了其中一份，四份都要同步更新。
6. ADMIN_KEY 等密碼不准寫進 repo。

## 1. 系統清單

| 代號 | 品牌／季 | 狀態 | 客戶網址 | repo | 商品筆數（款色）／款數 | 訂單編號前綴 | 主題色 | localStorage 前綴 |
|---|---|---|---|---|---|---|---|---|
| SDR | SUN DAY RED FW27 | 上線收單中（範本） | https://marcwang13.github.io/sdr-fw27-order/ | marcwang13/sdr-fw27-order | 207／105 | `FW27-` | `#610e0e` 酒紅 | `sdr-` |
| DST | DESCENTE 27FW Early Buy | 上線收單中 | https://marcwang13.github.io/dst-27fw-order/ | marcwang13/dst-27fw-order | 69／23 | `DST27-` | `#0a3f94` 藍 | `dst-` |
| DSTC | DESCENTE 27FW 正式訂貨（27Q3Q4 Convention） | 建置中（台灣定價待定；網頁不顯示價格，Excel 附韓幣 MSRP） | https://marcwang13.github.io/dst-27fw-main-order/ | marcwang13/dst-27fw-main-order | 1,114／456 | `DSTC27-` | `#0a3f94` 藍 | `dstc-` |
| WAAC | WAAC FW26 現貨（現有庫存接單） | 建置中（repo／後台都還沒建） | https://marcwang13.github.io/waac-fw26-stock-order/ | marcwang13/waac-fw26-stock-order | 19／11（25 個尺寸 SKU，168 件） | `WAAC26S-` | `#141414` 黑＋`#c8102e` 紅 | `waac-` |
| BYS | BLACK YAK 27SS | 未完成（已上線，未正式開放） | https://marcwang13.github.io/by-27ss-order/ | marcwang13/by-27ss-order | 747／349 | `BYS27-` | `#141414` 黑 | `bys-` |
| BYF | BLACK YAK 27FW | 未完成（已上線，未正式開放） | https://marcwang13.github.io/by-27fw-order/ | marcwang13/by-27fw-order | 150／148 | `BYF27-` | `#141414` 黑 | `byf-` |

### 各系統後端

| 代號 | Apps Script 端點（`config.js` 的 SUBMIT_URL） | 後台試算表 |
|---|---|---|
| SDR | https://script.google.com/macros/s/AKfycbzJ_l8ZTP4zOzK1WKJmpcfBKnd9N05hL8rUMr5lVLTGMHsGIYpq2udV0DXDecC-Q1dX/exec | https://docs.google.com/spreadsheets/d/1MD9-FCwtUrQM6K79bi6HDbZpdlpNj9qLk5dAu_pBRic/edit |
| DST | https://script.google.com/macros/s/AKfycbxxlmSXignxS5EE7Bd2vpPw3Z7HRcg9bb9BeN5tlCDfLMYUDFugMGcS4rv4rJydck_bcw/exec | https://docs.google.com/spreadsheets/d/1dWV3TyPOV__bduxdHDoBe-FieMdV02vr9-qjQrgkbpU/edit |
| DSTC | https://script.google.com/macros/s/AKfycbxvudd7CBJzFcuxFbhq1_huI9BwEY3zXGxW-_ODDJrs2SSTNJmPVLJYULRk_uiDaqzy/exec | https://docs.google.com/spreadsheets/d/1Z3xtNZ-P6mepW-d0DIFg8O96bDfxRFOoU15BjaZko5w/edit |
| WAAC | （待部署：emerswhlsystem.marc@gmail.com 名下新建） | （待建立：「WAAC FW26 現貨 線上訂單」） |
| BYS | https://script.google.com/macros/s/AKfycbwBKPi33bXNrIS7rdRpSJegQRBtljhtXKfEU-oBY0vMHUpBSzSNCfgaxdkttTdwETbT/exec | https://docs.google.com/spreadsheets/d/1elXDIBFt4J-eMZOjU8NhwVbCh2-8_u0o2RBk4c21_sE/edit |
| BYF | https://script.google.com/macros/s/AKfycbwob2mjChGVJGGnlyVB-Vd9eEeXhcEOMb7IQUO4udmiKlLHLi3R7QNZPimVoFE3ozf2/exec | https://docs.google.com/spreadsheets/d/1IhJqFN5_V9B45q0lNpt9ZKe2ByYbM8C9YhaYwGP6JUo/edit |

試算表與 Apps Script 都在公司帳號 `marc_wang@emers.com` 底下。Apps Script 專案列表：https://script.google.com/home/my

### 收單現況（2026-11-02 10:40 用 list API 讀後台；SDR 12／6,785／40,779,200 不變，DST 已增至 14 張）

| 代號 | 訂單數 | 件數 | 零售金額（台幣） | 備註 |
|---|---|---|---|---|
| SDR | 12 | 6,785 | 40,779,200 | 雷根兩店（高夢、西門）分兩張單 |
| DST | 14 | 25,002 | 70,320,100 | 雷根 16 分店一張連鎖單 19,219 件；動力主義 4 店分 4 張單 |
| BYS | 0 | 0 | 0 | 還沒開放 |
| BYF | 0 | 0 | 0 | 還沒開放 |

## 2. 架構

```
經銷商瀏覽器
  │ 開客戶網址（純靜態頁）
  ▼
[前台] GitHub Pages：marcwang13/<brand>-<season>-order
  │ index.html  單一檔案的前端（HTML+CSS+JS，無框架、無 build）
  │ data.js     商品資料 window.SDR_ITEMS（BY 另有 BY_RUNS、BY_CFG）
  │ imgs.js     縮圖 base64，window.SDR_IMG
  │ big/        大圖
  │ config.js   window.SDR_CONFIG = { SUBMIT_URL }
  │
  │ fetch POST，body 是 JSON 字串，Content-Type: text/plain;charset=utf-8（避開 CORS 預檢）
  │ fetch GET ?action=list&key=…（管理頁）
  ▼
[收單] Google Apps Script 網頁應用程式（綁在試算表上）
  │ 執行身分：我（marc_wang@emers.com）；存取：任何人
  │ LockService 排隊寫入
  ├─► [後台] Google 試算表「<品牌> <季> 線上訂單」
  └─► [通知] MailApp：驗證碼信、新單／修改（附 Excel 訂單本）、取消信
```

前台沒有資料庫。「我的訂單」和管理頁都即時讀試算表，所以直接改試算表＝系統同步改。

外部函式庫（前端用 CDN 動態載入）：ExcelJS（產 Excel 訂單本、交單檔）、SheetJS（匯入 Excel）。

## 3. repo 檔案

```
<repo>/
├── index.html          前端全部程式（約 14 萬字元；SDR 83 個函式，DST／BYS／BYF 85～86 個，BY 多 SZL、fullSizes、szConv 等）
├── data.js             商品資料
├── imgs.js             縮圖（base64）
├── big/                大圖（檔名對應商品 doll 欄位的 hash）
├── config.js           SUBMIT_URL
├── apps-script/Code.gs 後端（471 行）；改完要貼到 Apps Script 並重新部署
├── README.md
└── tools/              （只有 BY 兩套）gen.py 重產 data.js；parse.py 讀原廠匯出；fw_zh.py 中文品名；szconv.py 尺寸對照
                        實際：BYS＝brand.py、fw_zh.py、gen.py、gen2.py、parse.py、szconv.py；BYF＝fw_zh.py、gen.py、gen2.py、parse.py（沒有 szconv.py）
```

### data.js 商品欄位（一筆＝一個款色）

| 欄位 | 意思 |
|---|---|
| `id` | 唯一 key（SDR／DST 是「分頁-序號」，BY 是色碼 SKU） |
| `sheet` | 前台分頁（品類大分類） |
| `mon` | 月份／系列篩選值 |
| `theme`、`drop`、`monTag` | 主題、Drop、月份標記 |
| `cat` | 品類（交單分類 `divOf()` 也看這欄） |
| `gen` | 性別：男／女／中性 |
| `style` | 款號 |
| `zh`、`en` | 中文品名、英文品名 |
| `color`、`cc`、`sku` | 顏色、色號、色碼 SKU |
| `sizes` | 這個款色有開的尺寸 |
| `price` | 台灣建議售價（台幣），**網站上唯一可顯示的價格** |
| `fab`、`tech`、`ov`、`dt`、`series`、`note`、`icon` | 材質、機能、商品概述、細節、系列、備註、標章 |
| `launch`、`eta` | 上市月份、到貨日 |
| `doll` | 圖片 hash，對 `imgs.js` 與 `big/` |
| `part`、`run` | 上身 top／下身 bottom；尺寸段 key |
| `div` | （選填）強制指定交單分類 APP／ACC／FTW |
| BY 專用：`krw`、`whl`、`whlr`、`tw` | 韓國售價、內部選款標記、選款理由、台灣市場建議 |

### 各系統分頁（`sheet`）

- SDR：服裝-男 120、服裝-女 16、配件 38、球袋 6、鞋款 27
- DST：上衣 TOUGH 33、羽絨 23、GORE-TEX 13
- BYS：上身 352、下身 132、配件 246、鞋款 17
- BYF：上身 105、下身 39、套裝 6（**尺寸全是 `ASSORTED`，只填總數量，沒有尺寸段**）

### index.html 重要常數與函式

- 常數：`SHEETS`、`MONTH_ORDER`、`SIZE_COLS`（各分頁尺寸段）、`SHARE`／`SHARE_CAT`（前季尺寸銷售佔比）、`HKEY`（已送出紀錄 key）、`DRAFT_KEY`（草稿 key）、`AKEY`（登入 token key）、`OV_COL`／`GEN_COL`（圓餅圖色）、`FIXED`（Excel 訂單本固定欄）、`HO_BRAND`／`HO_FILE`／`HO_KEY`／`HO_DISC`（交單檔）。
- 下單：`renderList`、`itemHTML`、`matrixHTML`、`submit`、`xlsxForMail`、`post`。
- 連鎖分店：`brList`、`brDialog`、`openBranchMgr`、`branchTableHTML`、`branchesForExport`。
- 我的訂單：`startMine`、`renderMine`、`loadOrderToForm`。
- Excel：`buildBook`、`exportBook`、`importBook`、`loadExcelJS`、`loadSheetJS`。
- 管理：`startAdmin`、`renderAdmin`、`adminList`、`orderDetailHTML`、`adminSubmit`、`exitAdminEdit`、`reloadAdmin`。
- 下單分析：`analyzeLines`、`anAdminHTML`、`orderAnalysisHTML`、`anGroupOf`、`anSeries`。作廢不計；對不到商品標「找不到商品」。Excel 總表用公式，函式在 `buildBook`。
- 一鍵統整交單：`buildHandoff`、`exportHandoff`、`handoffCheck`、`divOf`、`hoUnits`、`hoSizes`。按鈕會先呼叫 `window.SDR_ADMIN.list()` 重新讀取最新訂單，`handoffCheck()` 檢查每張有效單（含各分店）明細件數＝訂單件數，不一致就提示稍後再按、不產出檔案。2026-11-02 先在 DST 做（57e31f4），已同步到 SDR、BYS、BYF。
- 右上角管理者登入：搜尋註解「右上角管理者登入」（約第 1246 行），按鈕 `#adm-btn`。

### 各系統字串差異（複製新品牌時要改的地方）

| 項目 | SDR | DST | BYS | BYF |
|---|---|---|---|---|
| `<title>` | SDR FW27 線上訂貨 | DESCENTE 27FW Early Buy 訂貨 | BLACK YAK 27SS 經銷訂貨 | BLACK YAK 27FW 經銷訂貨 |
| localStorage | sdr-auth、sdr-admin、sdr-dev、sdr-ho、sdr-fw27-sent-v1、sdr-fw27-draft-v1 | dst-auth、dst-admin、dst-dev、dst-ho、dst-27fw-sent-v1、dst-27fw-draft-v1 | bys-auth、bys-admin、bys-dev、bys-ho、bys-27ss-sent-v1、bys-27ss-draft-v1 | byf-auth、byf-admin、byf-dev、byf-ho、byf-27fw-sent-v1、byf-27fw-draft-v1 |
| HO_BRAND | SUN DAY RED FW27 | DESCENTE 27FW EARLY BUY | BLACK YAK 27SS | BLACK YAK 27FW |
| HO_FILE | SDR_FW27 | DESCENTE_27FW | BLACKYAK_27SS | BLACKYAK_27FW |
| Code.gs 寄件名稱（客戶） | SUN DAY RED 台灣 | DESCENTE 台灣 | BLACK YAK 台灣 | BLACK YAK 台灣 |
| Code.gs 寄件名稱（內部） | SDR FW27 線上訂貨 | DESCENTE 27FW 線上訂貨 | BLACK YAK 27SS 線上訂貨 | BLACK YAK 27FW 線上訂貨 |
| Code.gs 色碼 | #610e0e | #0a3f94 | #141414 | #141414 |

CSS 的 `--brand` 每套有兩個值（主色＋深色變體，例 SDR `#610e0e`／`#5a0d0e`），換色時兩個都要改。

注意：四套的 `config.js` 都用 `window.SDR_CONFIG`、商品都叫 `window.SDR_ITEMS`。同一頁要載入兩套以上就得改名。

## 4. 收單 API（四套共用）

全部打該系統的 `…/exec`。POST body 是 JSON 字串，header `Content-Type: text/plain;charset=utf-8`。

| 方法 | action | 參數 | 回傳 | 誰能用 |
|---|---|---|---|---|
| GET | （無） | — | 文字「… 收單程式運作中」，可當健康檢查 | 任何人 |
| GET | `list` | `key` | `{orders:[…]}` 含明細；錯誤 `{error:'forbidden'}` | 管理者 |
| POST | `otp_send` | `email` | `ok`／`wait`（60 秒內重送）／`invalid_email` | 任何人 |
| POST | `otp_verify` | `email`、`code` | `{email, token}` 或 `{error:'bad_code'/'expired'/'too_many'}` | 任何人 |
| POST | `mine` | `auth:{email,token}` | `{orders:[…]}`，只回這個帳號的單 | 已登入客戶 |
| POST | （無 action）＝送單 | `auth`、`oid`、`lines[]`、`store`、`contact`、`phone`、`email`、`note`、`branches`、`_xlsx`（base64）、`_xlsxName` | `ok`／`login_required`／`invalid` | 已登入客戶；同 oid 再送＝修改 |
| POST | `cancel` | `auth`、`oid` | 刪除結果 | 下單本人 |
| POST | `status` | `key`、`oid`、`status`（預設「已確認」） | `ok`／`forbidden` | 管理者 |
| POST | `admin_save` | `key`、`oid`、`lines[]`、`notifyCustomer` 等 | `ok`／`forbidden` | 管理者 |
| POST | `admin_delete` | `key`、`oid` | 刪除結果／`forbidden` | 管理者；內部呼叫 `cancel_(ss, oid, '', true)` 跳過帳號檢查 |

`lines[]` 每筆：`sheet`、`mon`、`style`、`sku`、`en`、`zh`、`color`、`size`、`qty`、`price`、`branch`（連鎖單才有）。

訂單編號：`<前綴><YYMMDD>-<HHmm><3 碼亂數>`，例 `FW27-261028-1544MTN`。

`key` 就是 Apps Script 指令碼屬性 `ADMIN_KEY`。四套統一用同一組，數值向 Marc 拿，**不要寫進前端程式、README 或給客戶的文件**（repo 是公開的）。

### Code.gs 函式

`adminOk_`、`doGet`、`json_`、`listOrders_`、`setStatus_`、`doPost`、`saveOrder_`、`sheet_`、`logSheet_`、`findOid_`、`removeOid_`、`sizeCmp_`、`tabName_`、`writeOrderTab_`、`rebuildOrderTabs`（手動執行：補建每店分頁）、`cancel_`、`orderHtml_`、`notify_`、`customerMail_`、`authSecret_`、`normEmail_`、`tokenFor_`、`authEmail_`、`otpSend_`、`otpVerify_`、`out_`。

常數：`NOTIFY_TO`、`ORDER_HEAD`、`LINE_HEAD`、`SIZE_ORDER`、`RESERVED_TABS`。

指令碼屬性：`ADMIN_KEY`（手動設，改了立即生效）、`AUTH_SECRET`（第一次用自動產生，改了所有客人要重新登入）。

## 5. 後台試算表

| 分頁 | 內容 |
|---|---|
| 訂單 | 一張單一列：送出時間、訂單編號、經銷商／店名、聯絡人、電話、Email、訂單備註、款色數、件數、零售金額、分店數、分店、狀態、帳號 Email、最後修改 |
| 明細 | 一個款色尺寸一列：送出時間、訂單編號、經銷商／店名、分店、分頁、月份、款號、色碼 SKU、英文品名、中文品名、顏色、尺寸、數量、台灣建議售價、零售金額 |
| <店名> | 每張單自動開一頁，款色一列、尺寸橫排 |
| _紀錄（隱藏） | 收過的訂單編號，不能刪 |

- 狀態：「已送出」→「已確認」只是內部標記，客人還能改。要鎖單就把狀態改「作廢」，之後客人再送也不會寫入。
- 「最後修改」：`業務 YYYY/MM/DD HH:mm`（管理頁改的）或 `客人 …`（客人自己改的）。

## 6. 登入、權限、通知

- **客戶登入**：Email 收 6 位數驗證碼，10 分鐘有效，錯 5 次作廢，60 秒內不能重寄。開放註冊。token 用 HMAC-SHA256（AUTH_SECRET）簽章，存在瀏覽器 `<前綴>-auth`。每套各自簽章，四套要各登一次。
- **權限**：每張單記「帳號 Email」，只有同帳號能改、刪；換裝置同 Email 登入就看得到。
- **管理者**：網站右上角「管理者登入」→ 輸入密碼 → 前端打 `GET ?action=list&key=` 驗證，對了存進 localStorage `<前綴>-admin` 並跳到「訂單彙整」；按鈕變「登出管理者」。舊的 `?admin=<key>` 網址也還能用（帶入後網址上的 key 自動清掉；`?admin=off` 登出）。
- **通知收件人（四套相同）**：`marc_wang@emers.com,zero_wang@emers.com,zoe_chang@emers.com,vince_tian@emers.com,david_wu@emers.com,benson_wang@emers.com,max_lee@emers.com,kai_weng@emers.com`，另外寄給客戶本人。
- **信件**：新單、修改（附完整 Excel 訂單本）、客人取消、業務刪除（內部「訂單取消（業務刪除）」、客人「訂單已由業務取消」）、業務調整（可選是否通知客人）。回信地址是 NOTIFY_TO 第一位。

## 7. 功能

**客戶前台**：品類分頁、月份／系列篩選、搜尋、只看已下單；商品卡（娃娃圖／CAD 款式圖／實體圖點擊放大、商品說明與材質、完整尺寸段，沒開的尺寸斜線灰格）；前季尺寸銷售佔比；連鎖分店模式（分店 × 尺寸矩陣，匯出總數版或連鎖版，連鎖版多「分店配貨」頁）；下單總覽圓餅圖（品類、性別，件數與金額）；下載／匯入傳統 Excel 訂單本；草稿自動存；我的訂單（修改、刪除按兩次、Excel、CSV）。只顯示台灣建議售價。

**管理頁（訂單彙整）**：所有訂單列表、圓餅圖、下單分析、看明細、編輯訂單、Excel／CSV、全部明細 CSV、標記已確認、刪除訂單（按兩次）、**一鍵統整交單**。

**下單分析**（訂單彙整裡，圓餅圖下面）：依大類、分頁、系列、經銷商各一張表。每張有款色數（款號＋顏色，一個色碼算 1）、尺寸數（款號＋顏色＋有填數量的尺寸）、件數、零售金額、件數佔比、金額佔比。可切「全部」或單一經銷商。展開「看明細」看該單的拆分；連鎖單各分店標題有該店的款色、尺寸、件數、金額，整張單同一款色只算 1。作廢不計入。對不到商品的明細，大類和系列標「找不到商品」。

大類依各系統目錄。SDR：服裝（男裝＋女裝）、配件（含球袋）、鞋款。DST 這季都是服裝，依品類分成上衣（T 恤、POLO）、外套（羽絨外套、輕量羽絨、GORE-TEX 外套）、背心（含羽絨背心）、長褲，跟三個分頁（上衣 TOUGH、羽絨、GORE-TEX）不同。系列：SDR 取商品資料「系列：」後面的名稱，沒標則用主題；DST 取系列欄的「產品線｜主題」（例如 PREMIUM TECH ESSENTIAL｜TOUGH、SNOW｜CANON；NEO｜NEO 只寫 NEO），訂貨窗口不另拆，沒有系列欄就用主題。

Excel 訂單本「總表」有同樣的分頁、大類、系列（款色數、尺寸數、訂購總數、零售金額），公式連到各分頁的隱藏欄（大類鍵、系列鍵、尺寸格數）。改黃色數量格，已列出的列會重算；本來沒下、這次才開始下的系列，要重新匯出才會出現。這份 xlsx 在瀏覽器產生，Apps Script 不用改。經銷商那張表只在管理頁，因為一份訂單本就是一家。

**一鍵統整交單**：下載 `<HO_FILE>_交單彙整_YYYYMMDD.xlsx`，給品牌方交單。
- 只算狀態不是「作廢」的單；一般單一店一區塊，連鎖單每分店一區塊（「店名 分店名」），同名合併。
- 折數統一 5 折（`HO_DISC=0.5`），「總表」B4 可改，三個分頁的 WHL 一起重算。
- 分頁順序：總表、APP(衣)、ACC(配)、FTW(鞋)。`divOf()` 依 sheet＋cat 分類：鞋／靴→FTW；衣／衫／褲／裙／外套／背心／T恤／POLO／套裝→APP；配件／球袋／帽／手套／襪／包／毛巾／皮帶／球Tee／球桿套／眼鏡／燈／登山杖→ACC；其餘 APP；商品有 `div` 欄位就照欄位。
- APP／ACC／FTW 版面：左邊資訊欄（STYLE NO.、STYLE & COLOR、COLOR、顏色、CATEGORY、IMAGE、STYLE NAME、中文品名、GENDER、月份、TW-SRP）→ WHSL TTL 區（粉紅，公式加總各店）→ 各店區塊（黃色店名）。每區上方有 SRP TTL、WHL TTL 兩列；最下 TOTAL 列；凍結在第 7 列；橫向一頁寬。
- 總表（BY 客戶）：每店 APP／ACC／FTW 件數與 SRP 金額、客戶 TTL、件數佔比、SRP 加總、金額佔比、×折數 WHL；整體加總；品類佔比。全部用公式連到各分頁。

## 8. 常見維護操作

| 要做的事 | 怎麼做 |
|---|---|
| 改前端（文案、功能、商品） | 改 repo 檔案 → push 到 main → GitHub Pages 約 1 分鐘生效。改完用瀏覽器實際打開確認。 |
| 改後端 | 改 repo 的 `apps-script/Code.gs` → 打開試算表 → 擴充功能 → Apps Script → 先比對線上程式碼和 repo 是否一致 → 整份貼上（編輯器可用 `monaco.editor.getModels()[0].setValue(code)`）→ Ctrl+S → **部署 → 管理部署 → 鉛筆 → 版本選「新版本」→ 部署**。這樣端點網址不變。不要用「新增部署作業」，那會產生新網址。 |
| 新增／改商品 | SDR、DST：直接改 `data.js`（缺圖時一併補 `imgs.js` 與 `big/`）。BY：改原廠匯出檔後跑 `tools/gen.py` 重產。 |
| 改通知名單 | 改四套 `Code.gs` 的 `NOTIFY_TO`，四套都重新部署。 |
| 改管理密碼 | Apps Script → 專案設定 → 指令碼屬性 `ADMIN_KEY`，立即生效，不用重新部署。四套要一起改。 |
| 鎖單／作廢 | 試算表「訂單」分頁的狀態改「作廢」。 |
| 補店名分頁 | Apps Script 編輯器選 `rebuildOrderTabs` 執行。 |
| 範本加新功能 | 先做在 SDR，驗證後同步到 DST、BYS、BYF（前端 push、後端重新部署）。 |
| 開新品牌 | 照第 10 節。 |

測試：可用 Playwright 開頁面，攔截 `script.google.com` 的請求回假資料，跑下單、管理頁、交單檔；交單檔用 LibreOffice 重算後核對總表與各分頁 TTL／SRP／WHL。真實流程測試要用 Marc 信箱收驗證碼，測完刪測試單。

## 9. 待辦與已知問題

### BLACK YAK 27SS／27FW（未完成）
- [ ] 售價暫估：台幣價＝韓國 MSRP × 0.0245（`tools/gen.py` 的 `FX`），四捨五入到十位，沒含關稅運費。要換成正式台灣建議售價。
- [ ] 尺寸對照只是參考（上衣韓國尺碼→字母、褲腰 cm→英吋、鞋 mm→US），不是原廠尺寸表。
- [ ] 27FW 尺寸全是 `ASSORTED`（只填總量），拿到尺寸段後要改成實際尺寸。
- [ ] 後台沒有任何訂單，全流程測試（登入→下單→通知信→修改→刪除→管理者登入→一鍵統整交單）還沒跑過。
- [ ] 客戶版「快速上手」文件、經銷商通知信還沒做。
- 前季尺寸銷售佔比：剛代理沒有資料，已關閉。DST、BYS、BYF 的 `shareFor()` 要 `window.DST_SHARE_ON` 為真才顯示，目前沒設；`SHARE` 表是從 SDR 複製過來的殘留資料，之後有真資料再換掉並打開開關。只有 SDR 有開。

### DESCENTE 27FW 正式訂貨（DSTC，`dst-27fw-main-order`）現況與 2026-11-18 改動（Grok）

**網頁（`index.html`）**
- **原廠日期全拿掉**：data.js 已刪 eta／launch／etd 欄位；`mon` 欄位還在（已 +1 個月），只供內部用，網頁、CSV、Excel 都不顯示。卡片沒有 ETA 標籤、沒有月份篩選；清單改依大類（上身／下身／配件／鞋類）分組，「只看已下單」時標題是「分頁 · 大類」。也沒有交期。
- **價格**：網頁完全不顯示韓幣或任何金額，卡片價格位置固定顯示「台灣定價待定」；`#t-amt` 金額格隱藏。韓幣只出現在下載的 Excel／CSV（欄名「韓幣 MSRP(₩)」「韓幣金額(₩)」）。台灣定價確定後：把 data.js 每筆 `price` 換成台幣，卡片 `.price` 改回顯示價格、打開 `#t-amt`，Excel／CSV 欄名改回「台灣建議售價／零售金額」，並從 `dataNotes()` 拿掉第一條。
- **篩選列（上方三排膠囊，同樣式）**：第一排 性別（全部／男／女／中性）→ 第二排 大類（全部／上身／下身／配件／鞋類）→ 第三排 系列分頁。三者交集，下排數字依上排選擇計算；0 筆的膠囊變淡不能按；選了之後目前分頁沒東西會自動跳到第一個有的分頁（`fixSel()`）。桌機分頁列換行、手機橫滑並自動捲到選中的分頁。資料 `gen` 只有 男 246／女 246／中性 622（配件 153、鞋 156 都算中性；女配件 41）。大類由 `cgOf()` 算：div FTW＝鞋類、ACC＝配件、part bottom＝下身、其他＝上身。
- **資料待更新說明**：頁首一個條列區（`#dnote`，由 `dataNotes(true)` 產生，數字即時計算）：台灣定價待定、尺寸參考 DESCENTE 尺寸對照表待原廠更新（含各性別尺寸段）、各色開放尺寸原廠未附暫依性別全段開放、實體圖待更新、部分款式圖為多色合圖、到貨月份待確認、18 款色原廠暫定品名、157 款色材質待提供（多為鞋）、5 款色顏色／色號待確認。同一份清單（`dataNotes(false)`，第一條改寫成附韓幣 MSRP）放在 Excel 訂單本「總表」G 欄；各分頁 B2 提示見總表。每張卡片尺寸區上方小字「尺寸待更新（目前參考前季）」，沒有實體圖的再加「・實體圖待更新」。
- **單色款式圖**：`pc.js`（`window.DSTC_PC={品號色:[左,上,右,下] 比例]}`）告訴前端怎麼從多色款式圖 `big/<hash>.jpg` 裁出單一配色；`applyPC()` 用 canvas 在瀏覽器裁（卡片、放大、Excel 款式圖欄都用裁好的）。目前 897／926 個多色圖款色已單色（自動 418＋人工目視 479），剩 29 款色仍是多色合圖。產生工具與人工指派紀錄在 emers-whl-system `tools/dstc_percolor/`（README 有步驟；注意 review.py 會 import match2 而重寫 crops.json）。
- **按鈕**：卡片圖片下「款式圖」（單色裁切）＋「實體圖」。`it.photos` 只放實體圖：目前 141 款色（全是鞋，實際是原廠多色配色渲染圖，43 張共用）有，其他款色「實體圖」按鈕灰掉。原本「全部配色」按鈕已拿掉。Excel 第 4 欄改名「實體圖」。
- **其他**：WHL logo 在標題左邊；沒有管理入口（訂單彙整按鈕只有管理者看得到）；不放任何會員 Email。

**Excel／CSV**
- 訂單本各分頁欄位：KEY、No.、款式圖、實體圖、主題、Drop、品類、性別、款號、中文品名、英文品名、顏色、色號、色碼 SKU、Icon、布料、系列／尺寸、商品概述、商品細節、材質與科技、備註、韓幣 MSRP(₩)、各尺寸、訂購總數、韓幣金額(₩)（後面是隱藏的分析鍵）。沒有月份／ETA。
- 匯入是依表頭名稱讀，`SKIP` 正規式含 月份／ETA／MSRP／韓幣／₩，所以舊檔（有 ETA、月份、韓國參考價欄）照樣能匯入。2026-11-18 測過：下載→填數量→匯入→套用 OK。
- **還沒改的後端**：`apps-script/Code.gs` 的訂單明細表頭仍有「月份」、通知信合計寫「參考金額 ₩」。要改的話先改 repo 再貼 Apps Script、部署新版本（需要 Marc 授權），本輪沒動。

**內部網站串接**：emers-whl-system 內部站已把這套列進預訂單系統（key `dst-27fw-main`，頁面 `pre.dstc`），比照 ftw 做法。DSTC 後台試算表沒有開「知道連結的人可檢視」，內部站讀不到，所以筆數顯示「筆數待更新」；要 Marc 開共用或改用系統帳號讀取。

**部署方式**：這個 repo 用 GH_TOKEN_WHL `git push` 會 403，所以改檔後放在 box 的 `/workspace/upl2/`、`/workspace/upl3/dst-27fw-main-order/`，由 Marc（或 Grok 的瀏覽器）在 GitHub 網頁「Add file → Upload files」上傳。已上線：ac245f3（pc.js 418 款色）；之後本機 commit fa2d052（pc.js 897）、c01980d 與本輪（拿掉 ETA、三排篩選、實體圖、待更新說明、韓幣 MSRP 欄）待上傳。

**過往參考（2026-11-19，Claude）**：`ref.js`（`window.DSTC_REF`）由 `tools/build_ref.py` 從 emers-whl-system 的 `dealer/data/chain_*`、`internal/data/direct_chain_*` 算出。區域：直營依主檔 region；動力新竹巨城、中和環球＝北部，其餘門市＝中部；雷根大甲＝中部、其餘＝南部（天王暫列南部，待 Marc 確認）。雷根、動力目前沒有 25FW 整季資料，中部、南部畫面不顯示資料期間提醒（Marc 11/19 要求拿掉），ref.js 也不放體系名稱與期間。每月 POS 匯入後重跑：`python3 tools/build_ref.py --whl ../emers-whl-system --xlsx 對照表.xlsx`，再更新 index.html 的 `ref.js?v=`。

### WAAC FW26 現貨（`waac-fw26-stock-order`）現況（2026-11-19，Grok）
- 用途：手上已到貨的現貨新品接單，不是預訂。以 DST Early Buy 前台為底、Code.gs 以 DSTC（含會員票券 SSO）為底。
- 商品：WAAC FW26 帽款＋桿頭套 19 款色／11 款，全部 ACC（品類：棒球帽、遮陽帽、漁夫帽、護耳帽、桿頭套）。來源 Excel 分頁 FW26（款號、色號、品號、SRP、Order 欄）。
- 庫存：每個尺寸有 `stock`（現有庫存）與 `pn`（品號）。來源＝WHL 每日倉庫庫存（emers-whl-system `unmatched_stock_codes.csv`，2026-11-19 的資料；這批品號還不在 WHL 主檔，所以內部站庫存頁看不到），25 個品號全對到，數量跟 Excel 的 Order 欄一致。`window.WAAC_STOCK_DATE` 顯示在頁首。
- 數量上限（2026-11-19 Marc 決定：只限單張訂單）：卡片每個尺寸顯示「庫存 N」，一張訂單各尺寸（連鎖分店合計）不能超過現有庫存，不扣其他訂單。輸入超過會自動壓回並提示；送單時 Code.gs `stockCheck_` 再擋一次（錯誤 `over_stock:[...]`）。`LIMIT_ACROSS_ORDERS = false`、index.html `USE_AVAIL = false`（不呼叫 `avail`）；要改先送出先占，兩個都改 true。多張單合計超過庫存由業務在款色彙總分配。
- 卡片直接顯示材質與產地（代碼行下方，手機版上下兩行），沒有「材質與產地」展開按鈕。
- 更新庫存：改 `tools/build_data.py`（重產 data.js）＋ Code.gs 的 `STOCK`／`STOCK_DATE` 常數（兩邊要一致），Code.gs 改完要部署新版本。
- 價格：顯示「建議售價」（SRP，NT$2,800／3,800）；HO 分店配貨折數沿用範本 0.5，未確認。
- 圖片：只有原廠 Excel 內嵌的線稿／實體混合小圖，多色合圖已裁成單色（`tools/crop.py`），沒有放大處理；沒有獨立實體圖。品名、中文顏色為暫定。頁首「資料待更新說明」列出這幾點。
- 前台沒有任何登入後台的入口；訂單彙整（刪除訂單、一鍵統整交單）只能從內部站 03 卡片「訂單彙整」開（#admin=會員票券，Code.gs 用指令碼屬性 PREORDER_SSO_SECRET 驗證）。
- 內部站串接（emers-whl-system，已改未部署）：key `waac-fw26-stock`、權限 `pre.waacs`；試算表 ID 待填（tools/preorder_counts.py、tools/preorders_sync.py、internal/preorder-view.js、sys-preorder.html／index.html 後台連結）。

### 入口網站串接（規劃中）
Marc 要把四套系統（含後台、管理頁）串進另一個入口網站。可行做法：

| 做法 | 怎麼做 | 注意 |
|---|---|---|
| 連結（最穩） | 入口放按鈕，新分頁開客戶網址 | 不用改程式 |
| iframe 內嵌 | `<iframe src="https://marcwang13.github.io/<repo>/">` | Safari 會隔離 iframe 的儲存，客人可能每次都要重收驗證碼；建議新分頁開 |
| 入口讀訂單 | 入口網站**伺服器端**打 `GET <exec>?action=list&key=<ADMIN_KEY>` | ADMIN_KEY 只能放伺服器端 |
| 統一登入 | 四套 AUTH_SECRET 設成同一組（token 就能共用，但 localStorage key 不同，前端也要改成讀同一個 key），或改由入口網站發 token | 要改程式 |

### 其他
- **SDR 交單檔少 10 件**：「森富」訂單有一筆 `sku＝待確認`（配件、FREE SIZE、10 件、單價 3,280，零售 32,800）在 data.js 找不到商品，`hoUnits()` 會略過，交單檔總計 6,775 件／40,746,400，比 list API 少 10 件／32,800。`handoffCheck` 只比對訂單件數 vs 明細件數，抓不到這種情況。要請 Marc 確認這筆是什麼商品，改成正確 SKU；或之後在 `handoffCheck` 加「明細找不到商品」的提示。
- 同一張「森富」單有 LH0179 Presidio 球鞋 7W 2 件，但該款色只開 8W～12W（可能是客人匯入或業務改的），請確認。
- DST 客人「永璨體育登山用品社」聯絡 Email 欄有空白（`yt.sport@msa.hinet .net`），帳號 Email 正確，不影響通知。
- 有些單是業務用自己的帳號代下（帳號 Email 是 shihyao21@gmail.com、kai_weng@、vince_tian@、zero_wang@），這些單客人自己看不到。

## 9.5 交接驗證紀錄（2026-11-02，Grok Bot）

- GitHub：四個 repo 可讀（匿名 clone）。四站與 config.js 正常，四個端點健康檢查正常，錯誤 key 回 forbidden，正確 key 可讀 list。
- 測試方式：Playwright 攔截 script.google.com 回假資料，跑管理者登入、訂單彙整、刪除訂單按鈕、一鍵統整交單（含不一致時擋下）；交單檔用 LibreOffice 重算，核對總表與 APP／ACC／FTW 分頁的件數與 SRP。
- 文件和程式碼的差異已在上面各節更正（Code.gs 差異行數、tools 檔案、函式數、`--brand` 雙值、handoffCheck 原本只在 DST）。

## 10. 開新品牌（照範本複製）

1. **收資料**：品牌訂單本 Excel（款號、品名、色號、色碼 SKU、尺寸、零售價、月份／交期、主題、商品說明）、尺寸表、娃娃圖或 CAD 圖、實體圖、前季尺寸銷售佔比、主題色。缺零售價、交期年份錯、整列標黃的先列給 Marc 確認；原表反黃＝不建議下單，品名加註。
2. **Marc 建 repo**：`marcwang13/<brand>-<season>-order`，開 GitHub Pages（main／root），給 AI 的 GitHub 帳號或 App 寫入權限。
3. **複製範本**：把 `sdr-fw27-order` 全部檔案複製過去，重產 `data.js`、`imgs.js`、`big/`；改第 3 節「字串差異」表的每一項、CSS `--brand` 色、`SHEETS`、`MONTH_ORDER`、`SIZE_COLS`、`SHARE`、訂單編號前綴；`NOTIFY_TO` 用固定名單。
4. **後端**：公司帳號新建試算表「<品牌> <季> 線上訂單」→ Apps Script 貼 `Code.gs` → 指令碼屬性加 `ADMIN_KEY`（與其他套相同）→ 部署成網頁應用程式（執行身分：我，存取：任何人）→ Marc 按授權 → 網址寫進 `config.js`。
5. **測試全流程**（第 8 節），測完刪測試資料。
6. **交付**：客戶網址、試算表連結給 Marc；做客戶版快速上手文件。管理密碼不寫進任何給客戶的東西。

## 11. 變更紀錄

| 日期 | AI | 系統 | 內容 | commit |
|---|---|---|---|---|
| 2026-11-19 | Grok | WAAC | 數量上限改為只限單張訂單（LIMIT_ACROSS_ORDERS=false、USE_AVAIL=false，拿掉「可訂」字樣）；材質與產地直接顯示在卡片上，拿掉展開按鈕 | （本次） |
| 2026-11-19 | Grok | WAAC | 新增 WAAC FW26 現貨訂貨站：每尺寸顯示現有庫存、前後台都擋超過可訂量、現貨標籤、性別／品類篩選、無前台後台入口（只走內部站票券） | （本次） |
| 2026-11-19 | Claude | DSTC | 同款多色列款式圖改固定 160px 正方形、上下置中（不再跟列高變大變小） | （本次） |
| 2026-11-19 | Claude | DSTC | 同款多色列的款式圖改成跟該列高度一樣（正方形、最小 120px），跟尺寸段對齊 | （本次） |
| 2026-11-19 | Claude | DSTC | 卡片標籤「Early Buy 已開訂」改顯示「Early Buy 已訂購款」（`ebLabel`，data.js 與 Excel 不動） | （本次） |
| 2026-11-19 | Claude | DSTC | 網頁分頁順序 NEO-ARCHIVE 移到 ACC 配件之後、鞋類之前（新增 `TAB_ORDER`，預設分頁改 TRAINING）；`SHEETS` 不動，Excel 訂單本與交單彙整順序不變 | （本次） |
| 2026-11-19 | Claude | DSTC | 原價售出比門檻改 9 折以上（build_ref.py 重跑 ref.js） | （本次） |
| 2026-11-19 | Claude | DSTC | 尺寸佔比數字改一般字重、內文字體 11.5px（不用粗體與等寬字） | （本次） |
| 2026-11-19 | Claude | DSTC | 按鈕平衡：商品細節改中深藍實心、過往參考加淡藍底＋粗框（CSS 變數 `--btn-pri`／`--btn-sec-*`）；尺寸佔比改整格深淺色塊（`--heat`，越高越深，拿掉長條） | （本次） |
| 2026-11-19 | Claude | DSTC | 版面：螢幕 ≥1100px 改左側欄（篩選、過往數據區域、搜尋、顯示選項、Excel、資料待更新說明），較窄維持原上方收合列；經銷資料填好後收成一行摘要（`renderDsum`，可再編輯）。過往參考改成跟商品細節同款按鈕、全價銷售比改名「原價售出比」；同款多色列的款式圖恢復 132px；對照款沒有的顏色標「此系列新色」；尺寸佔比加粗，最高的一格反白（`pctHTML`） | （本次） |
| 2026-11-19 | Claude | DSTC | 過往尺寸佔比放到每個尺寸格下方、對照款同色佔比放在色號旁（跟著北中南綜合切換）；過往參考面板保留 | （本次） |
| 2026-11-19 | Claude | DSTC | 同款不同色合併成一個外框（`groupHTML`／`rowHTML`）：外框上方一次顯示款名、說明、過往參考、「同款 N 色」，下面每色一列各自填數量；只有一色維持原卡片。只動畫面，訂單資料、Excel 訂單本、交單彙整都沒改 | （本次） |
| 2026-11-19 | Claude | DSTC | 過往參考拿掉中部／南部「資料期間較短」提醒，ref.js 不再放體系名稱與期間 | （本次） |
| 2026-11-19 | Claude | DSTC | 商品卡加「過往參考」：27FW 每款自動對照 25FW／26FW 舊款（同款延續／同系列同品類／同品類同價格帶／無對照），北部／中部／南部／綜合切換，顯示店均月銷、售罄率、全價銷售比、參考店數、尺寸分布、熱賣色（直營＋雷根＋動力，只給區域合計，不放店名與金額，排除 OUTLET／特賣／倉庫）。列表加「過往熱賣優先」排序、卡片加「去年熱賣」「新款無對照」標籤。資料由 `tools/build_ref.py --whl ../emers-whl-system` 產生 `ref.js`；人工改對照填 `tools/ref_override.json`。只同步這份文件，其他三個 repo 的副本待同步 | （本次） |
| 2026-11-02 | Grok | DST | 訂單彙整加下單分析：依大類（上衣／外套／背心／長褲）、分頁、系列（產品線｜主題）、經銷商統計款色數／尺寸數／件數／金額與佔比，可切換單一經銷商，展開訂單看該單。作廢排除，對不到商品標「找不到商品」。Excel 訂單本總表用公式同步。Apps Script 不用重新部署 | （本次） |
| 2026-11-02 | Grok | SDR | 訂單彙整加下單分析（範本，已併入 main）：依大類（服裝／配件／鞋款）、分頁、系列、經銷商。Excel 總表用公式 | fe901f0 |
| 2026-11-02 | Grok Bot | SDR、BY27SS、BY27FW | 一鍵統整交單：先重抓最新訂單並跑 handoffCheck，件數對不上就警告、不匯出 | b43842b／d0a4f4b／f791e22 |
| 2026-11-02 | Grok Bot | 四套 | 本文件放進四個 repo，新增同步規則（0.5 節）與變更紀錄 | （本次） |
| 2026-11-18 | Claude | DSTC | 新建 DESCENTE 27FW 正式訂貨（27Q3Q4）：APP／ACC／FTW 1,114 款色、詳細中文商品說明、FTW 分色圖、韓幣參考價、Early Buy 重複款標示 | （本次） |
| 2026-11-18 | Grok | DSTC | 原廠日期拿掉（data.js 刪 eta／launch、mon +1 月，只顯示「ETA X月」）；新增大類（上身／下身／配件／鞋類）與性別篩選；桌機分頁列換行；網頁不顯示韓國參考價與金額（Excel／CSV 保留）；掛進 WHL 內部站（dst-27fw-main，權限 pre.dstc） | （本次） |
| 2026-11-18 | Grok | DSTC | 單色款式圖 pc.js 擴充到 897／926（人工目視 479，工具在 emers-whl-system tools/dstc_percolor） | fa2d052 |
| 2026-11-18 | Grok | DSTC | ETA 全拿掉（卡片、篩選、分組、CSV／Excel）；上方三排篩選 性別／大類／系列（交集、0 筆變淡、自動跳分頁）；「全部配色」改「實體圖」按鈕（無圖灰掉＋實體圖待更新）；卡片「台灣定價待定」；頁首與 Excel 總表「資料待更新說明」條列；Excel 欄名「韓幣 MSRP(₩)」「韓幣金額(₩)」 | c01980d＋（本次） |
| 2026-11-19 | Claude | DSTC | 篩選列改四層四種樣式（性別分段／大類圖示分頁／系列標籤／小類文字，ACC、FTW 歸小類）、加「目前篩選」麵包屑；手機版篩選列可收合（頂端摘要列＋明顯「收合／展開篩選」按鈕，選系列後自動收合） | （本次） |
