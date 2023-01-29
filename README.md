## Yahoo 電影搭配 Line Notify 通知

使用爬蟲取得 Yahoo 電影資訊，並使用 line notify 發送。

![成果範例](/image/img1.jpg)

### 環境設定
1. 安裝相關的套件
2. 設定環境變數
    * `LINE_TOKEN`: line notify 官方金鑰
    * `PLAYING_PAGE`: (非必要) 上映中的電影要爬取的頁面數量。 默認為 5
    * `COMMING_PAGE`: (非必要) 即將上映的電影要爬取的頁面數量。 默認為 6
