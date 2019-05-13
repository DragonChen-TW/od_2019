函式說明:


calMedicalIndex(codebase)
計算統計區內「醫療院所數」及「每千人擁有病床數」，依值給定評分。

calculate_distance(lng1, lat1, lng2, lat2)
計算兩點距離。

calFreewayIndex(lng,lat)
計算離房屋物件(經緯度)最近的交流道，依距離線性給定評分。

calMRTIndex(lng,lat)
計算離房屋物件(經緯度)最近的捷運站，依距離線性給定評分。

calLightRailIndex(lng,lat)
計算離房屋物件(經緯度)最近的輕軌站，依距離線性給定評分，分數為捷運站之一半。

calPoliceIndex(lng,lat)
計算離房屋物件(經緯度)最近的警察局，依距離線性給定評分。

calStudentPopulationIndex(CODEBASE)
計算統計區內「5-19歲人口占所有人口比例」，依比例給定評分，共有10000分。

calStudentPopulationIndexAll()
計算高雄市所有統計區「5-19歲人口占所有人口比例」，依比例給定評分，共有10000分，得出整體分布結果。


資料集:
1. 107年12月高雄市統計區醫療院所統計_最小統計區
   來源: https://segis.moi.gov.tw/STAT/Web/Platform/QueryInterface/STAT_QueryProductView.aspx?pid=17E76871A91D8B18B3D6C995F0C996E8&spid=7ED8D58E129BC680

2. 高雄市交流道資料
   來源: 自行整理

3. 高雄紅橘線捷運車站中心座標
   來源: https://data.kcg.gov.tw/dataset/red-orange-line-station

4. 高雄輕軌車站中心座標
   來源: https://data.kcg.gov.tw/dataset/light-rail-station

5. 各縣(市)警察(分)局暨所屬分駐(派出)所地址資料
   來源: https://data.moi.gov.tw/MoiOD/Data/DataDetail.aspx?oid=DE03B06E-EED3-4B28-8A50-1E26642B9017

6. 107年6月高雄市統計區五歲年齡組人口統計_最小統計區
   來源: https://segis.moi.gov.tw/STAT/Web/Platform/QueryInterface/STAT_QueryProductView.aspx?pid=A6DD7C6A7F783388CD0E9E4F2131B90B&spid=7ED8D58E129BC680
   
