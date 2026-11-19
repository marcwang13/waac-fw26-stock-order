# WAAC FW26 現貨訂貨（經銷線上訂貨）

WAAC FW26 帽款與桿頭套現貨，19 款色／11 款，25 個尺寸 SKU，現有庫存合計 168 件。資料來源：原廠 FW26 訂貨 Excel（款號、色號、品號、建議售價、商品圖）＋ WHL 每日倉庫庫存（2026-11-19）。

- `index.html`：下單頁（商品資料在 `data.js`，縮圖在 `imgs.js`，大圖在 `big/`，LOGO 與 favicon 在 `brand/`）
- `config.js`：收單網址設定（`SUBMIT_URL`）。留空時為「傳單模式」，經銷商下載 Excel 後用 LINE / Email 傳給業務。
- `apps-script/Code.gs`：貼到 Google 試算表的 Apps Script，部署成網頁應用程式後即可收單。指令碼屬性要設 `ADMIN_KEY`、`PREORDER_SSO_SECRET`（不要寫進 repo）。

## 庫存
- 每張卡每個尺寸顯示「庫存 N」。每張訂單各尺寸不能超過現有庫存（不扣其他訂單，Code.gs `LIMIT_ACROSS_ORDERS = false`）；多張訂單合計超過庫存時，由業務在訂單彙整的款色彙總（有「現有庫存」欄）分配。
- 前台輸入時擋、Excel 訂單本的儲存格驗證擋、Code.gs 送單時再擋一次。連鎖分店下單時，各分店合計不能超過庫存。
- 要改成跨單扣量（先送出先占）：Code.gs `LIMIT_ACROSS_ORDERS` 和 index.html `USE_AVAIL` 都改 true。
- 更新庫存：改 `tools/build_data.py` 重產 `data.js`，並同步改 `apps-script/Code.gs` 的 `STOCK`、`STOCK_DATE`，再部署新版本。

## 價格
卡片、CSV、Excel 顯示建議售價（NT$）。

## 卡片
品名、顏色、現貨／庫存標籤、款號／色碼 SKU／品號，下面直接列材質與產地（不用點開）。

## 篩選
上方兩排：性別 → 品類（棒球帽／遮陽帽／漁夫帽／護耳帽／桿頭套），交集。沒有 ETA 或交期。

## 後台
前台沒有後台入口。訂單彙整（款色彙總、刪除訂單、一鍵統整交單）從 WHL 內部站「03 預訂單收單」的 WAAC 卡片按「訂單彙整」開啟。

## 其他
- 訂單編號前綴 `WAAC26S-`，localStorage 前綴 `waac-`。
- 品名、中文顏色暫定；商品圖為原廠 Excel 內的圖，多色合圖已裁成單色。
- 詳細交接見 `ORDER_SYSTEMS_HANDOFF.md`。
