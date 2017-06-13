
# coding: utf-8
import subprocess as sp
import time,re,StringIO
import pandas as pd
import requests
firebase_url ='https://gpumonitor-d6f94.firebaseio.com'
ServerName = 'oldGPU'
setInterval = 20

while 1:
    try:
        GPUInfoTEXT = sp.check_output('nvidia-smi  --format=csv,noheader --query-gpu=power.draw,utilization.gpu,fan.speed,temperature.gpu,name,index,uuid',shell=True)
        GPUInfoTEXT = re.subn('\sW|%','',GPUInfoTEXT)[0]
        GPUInfoTEXT = re.subn('\[Not\sSupported\]','0',GPUInfoTEXT)[0]
        GPUData = pd.read_csv(StringIO.StringIO(GPUInfoTEXT),header=None)
        GPUData.columns = ['Power','Utilization','Fan','Temperature','Name','GPUID','uuid']
        GPUData['Name'] = GPUData['Name'].apply(lambda x: x.strip())

        appInfoTEXT = sp.check_output('nvidia-smi  --format=csv,noheader --query-compute-apps=pid,process_name,gpu_uuid',shell=True)
        if appInfoTEXT:
            appData=pd.read_csv(StringIO.StringIO(appInfoTEXT),header=None)
            appData.columns = ['Pid','Process','uuid']
            appData['Process'] = appData['Process'].apply(lambda x: x.strip())
        else:
            appData =pd.DataFrame(columns=['Pid','Process','uuid'])

        pids = appData['Pid'].astype('S').tolist()
        if pids:
            try:
                psTEXT = sp.check_output(" ps -p {pids} -o user:20,pid".format(pids=str.join(',',pids)),shell=True)
                psDATA=pd.read_csv(StringIO.StringIO(psTEXT),sep='\s+')
                psDATA.columns = ['USER','Pid']
            except:
                psDATA = pd.DataFrame([('','')],columns=['USER','Pid'])
        else:
            psDATA = pd.DataFrame([('','')],columns=['USER','Pid'])

        mergedDATA = pd.merge(psDATA,appData,on='Pid')
        uuidProcess = mergedDATA.groupby('uuid')

        process = uuidProcess['Process'].apply(lambda x: ','.join(list(set(x)))).to_dict().items()
        user = uuidProcess['USER'].apply(lambda x: ','.join(list(set(x)))).to_dict().items()
        GPUData = pd.merge(GPUData,pd.DataFrame(process,columns=['uuid','Processes']),on='uuid',how='left')
        GPUData = pd.merge(GPUData,pd.DataFrame(user,columns=['uuid','Users']),on='uuid',how='left')                             
        GPUData.drop(['uuid'],axis=1,inplace=True)
        GPUData.fillna('',inplace=True)  
        result = requests.put('{firebase_url}/Servers/{ServerName}/GPU.json'.format(firebase_url=firebase_url,ServerName=ServerName),data=GPUData.T.to_json())
        time.sleep(setInterval)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print repr(e)
        time.sleep(100)