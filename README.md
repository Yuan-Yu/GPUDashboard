# GPUDashboard
A simple dashboard for NVIDIA GPU
![flowchart](https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/flowchart.png?raw=true)
## Demo
[Example](https://yuan-yu.github.io/GPUDashboard/)  
## Requirement  
- Python 2.7 or 3.6
- NVIDIA-sim
- A Firebase realtime database
- Linux-like OS  

## Setup  
1. Create a [Firebase **Realtime** database](https://console.firebase.google.com/)  
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/crateDB.png?raw=true" height="150" >   

2. Set rules to 
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/chageRule.png?raw=true" height="100" >    

```json 
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```  
3. Go to Project overview click **Add Firebase to your web app** and copy following part.  
<img src="https://github.com/Yuan-Yu/GPUDashboard/blob/master/docs/copyConfig.png?raw=true" height="150" >   

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
4. **On servers** which are installed NVIDIA GPU
```bash
pip install GPUDashboard
GPUDashboard -n your_server_name -i 20 -u your_databaseURL > GPUDashboard.log 

# your_server_name is the name you want to give your server e.g. MyFirstServer
# -i is the interval of GPU information updating
# your_databaseURL is the databaseURL obtained froom Firebase as shown above
```  
Now, the server GPU information is post to the firebase.  
5. Download [ViewStatus.html]('https://raw.githubusercontent.com/Yuan-Yu/GPUDashboard/master/ViewStatus.html') and open with text editor then replace the "config".  
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
6. open the "**modified** ViewStatus.html" with browser.
