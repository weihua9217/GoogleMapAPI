# GoogleMapAPI
call googleAPI to calculate distance and duration

主要分成兩種模式，**使用時須輸入GoogleMapAPI的Key**

**模式一**

	固定一個地點查詢其到其他各點的位址。
	輸入：起始地方名稱、起始地方地址，目的地檔案(xlsx檔)。
	輸出：起始地方至各個地方的行車距離、時間(xlsx檔)

**模式二:**

	輸入一檔案，從其中取兩兩組合，計算兩點距離及時間。
	輸入：包含地方名稱及地址之檔案(xlsx檔)
  	輸出：組合後的距離及行車時間結果
