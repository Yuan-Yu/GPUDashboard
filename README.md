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
1. Create a Firebase **Realtime** database
2. Set rule to 
```json 
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```  
3. Go to Project overview click "web application" and copy following part.  
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
4. On server which is installed NVIDIA GPU
```
pip install GPUDashboard
GPUDashboard -n your_server_name -i 20 -u your_databaseURL_URL > GPUDashboard.log # -i is the interval of GPU information updating.
```  
Now, the server GPU information is post to the firebase.  
5. Download [ViewStatus.html]('#') and replace the "config".  
6. Double click the modified ViewStatus.html
