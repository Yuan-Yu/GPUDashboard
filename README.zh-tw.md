# GPUDashboard
專為NVIDIA顯示卡設計的儀表板  
![flowchart](https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/flowchart.png?raw=true)
## 範例
[Example](https://yuan-yu.github.io/GPUDashboard/)  
## 需求  
- Python 2.7 or 3.6
- NVIDIA-sim
- A Firebase realtime database
- Linux-like OS  

## 設置  
1. 創建一個 [Firebase **Realtime** database](https://console.firebase.google.com/)  
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/crateDB-zh.png?raw=true" height="150" >   

2. 設定規則 
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/chageRule-zh.png?raw=true" height="100" >    

```json 
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```  
3. 到Project overview 點擊 **將Firebase加入您的網路應用程式**, 然後複製下面訊息    
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/copyConfig-zh.png?raw=true" height="150" >   

```javascript
  var config = {
    apiKey: "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    authDomain: "XXXXX.firebaseapp.com",
    databaseURL: "https://XXXXXX.firebaseio.com",
    projectId: "XXXXXXX",
    storageBucket: "XXXXXXX.appspot.com",
    messagingSenderId: "XXXXXXXXXXX"
  };
```  
4. 在安裝有NVIDIA顯示卡的伺服器上輸入下列指令    
```bash
pip install GPUDashboard
GPUDashboard -n your_server_name -i 20 -u your_databaseURL > GPUDashboard.log 

# your_server_name 是你希望該伺服器顯示的名稱 e.g. MyFirstServer
# -i 設定幾秒更新一次顯示卡訊息
# your_databaseURL 是Firebase的網址,在上面步驟取得
```  
設定完後,伺服器已經開始傳送顯示卡資訊到資料庫中了. ***如果擁有多台伺服器時,僅需要確認每伺服器的名稱不同,方可使用同一個firebase網址**  
  
5. 下載[ViewStatus.html](https://raw.githubusercontent.com/Yuan-Yu/GPUDashboard/master/ViewStatus.html)以文字編輯器打開並修改config的部分.  
```html
<html>
    <header>
      <script>
        var config = {
            apiKey: "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            authDomain: "XXXXX.firebaseapp.com",
            databaseURL: "https://XXXXXX.firebaseio.com",
            projectId: "XXXXXXX",
            storageBucket: "XXXXXXX.appspot.com",
            messagingSenderId: "XXXXXXXXXXX"
          };
      </script>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"/>
```  
6. 是用瀏覽器打開"**已修改的** ViewStatus.html".
