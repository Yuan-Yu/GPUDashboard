import subprocess as sp
import time,re
import json
import __future__
import requests
from datetime import datetime 

nvmlClocksThrottleReasonUserDefinedClocks         = 0x0000000000000002
nvmlClocksThrottleReasonGpuIdle                   = 0x0000000000000001
nvmlClocksThrottleReasonSwPowerCap                = 0x0000000000000004
nvmlClocksThrottleReasonHwSlowdown                = 0x0000000000000008
nvmlClocksThrottleReasonUnknown                   = 0x8000000000000000
nvmlClocksThrottleReasonSyncBoost                 = 0x0000000000000010
nvmlClocksThrottleReasonSwThermalSlowdown         = 0x0000000000000020
nvmlClocksThrottleReasonHwThermalSlowdown         = 0x0000000000000040
nvmlClocksThrottleReasonHwPowerBrakeSlowdown      = 0x0000000000000080
nvmlClocksThrottleReasonDisplayClockSetting       = 0x0000000000000100

throttleByThermalOrPowerBrakeSlowdown = nvmlClocksThrottleReasonHwSlowdown | \
                                         nvmlClocksThrottleReasonSwThermalSlowdown | \
                                         nvmlClocksThrottleReasonHwPowerBrakeSlowdown| \
                                         nvmlClocksThrottleReasonHwThermalSlowdown
def getGPUInfo():
    propertyNames = ['power.draw','utilization.gpu','fan.speed','temperature.gpu','name','index','memory.total','memory.used','throttled','uuid']
    GPUInfoTEXT = sp.check_output('nvidia-smi  --format=csv,noheader --query-gpu=power.draw,utilization.gpu,fan.speed,temperature.gpu,name,index,memory.total,memory.used,clocks_throttle_reasons.active,uuid',shell=True).decode()
    GPUInfos = {}
    for info in GPUInfoTEXT.split('\n'):
        if info:
            info = map(lambda x: x.strip(),info.split(','))
            info = dict(zip(propertyNames,info))
            info['throttled'] = True if int(info['throttled'],16) & throttleByThermalOrPowerBrakeSlowdown else False
            GPUInfos[info['uuid']] = info 
    return GPUInfos
def getGPUTasksInfo():
    taskPropertyNames = ['Pid','Process','uuid']
    appInfoTEXT = sp.check_output('nvidia-smi  --format=csv,noheader --query-compute-apps=pid,process_name,gpu_uuid',shell=True).decode()
    tasks = []
    for task in appInfoTEXT.split('\n'):
        if task:
            taskInfo = dict (zip(taskPropertyNames,map(lambda x: x.strip(),task.split(','))))
            tasks.append(taskInfo)  
    tasks = tasksAssignUser(tasks)
    return tasks
def getPidsUserInfo(pids):
    pid2user = {}
    if pids:
        try:
            psTEXT = sp.check_output(" ps -p {pids} -o pid,user:20".format(pids=str.join(',',pids)),shell=True).decode()
            psPattern = re.compile(r'\n\s*([\d]{1,})\s*([\w\d]{1,})')
            pid2user = dict(psPattern.findall(psTEXT))
        except sp.CalledProcessError as e:
            print(repr(e))
    return pid2user
def tasksAssignUser(tasks):
    pids = [task['Pid'] for task in tasks]
    pid2user = getPidsUserInfo(pids)
    for task in tasks:
        if task['Pid'] in pid2user:
            task['User']=pid2user[task['Pid']]    
    return tasks
def tasksGroupbyGPU(tasks):
    groupedTasks = {}
    for task in tasks:
        if task['uuid'] in groupedTasks:
            groupedTasks[task['uuid']].append(task)
        else:
            groupedTasks[task['uuid']] = [task]
    return groupedTasks

class GPU(object):
    def __init__(self,info):
        self.updateInfo(info)
        self._tasks = []
    def updateInfo(self,info):
        self.uuid = info['uuid'] if 'uuid' in info else self.uuid
        self.name = info['name'] if 'name' in info else self.name
        self.index = info['index'] if 'index' in info else self.index
        self.powerDraw = info['power.draw']
        self.temperature = info['temperature.gpu']
        self.fanSpeed = info['fan.speed']
        self.memoryTotal = info['memory.total']
        self.memoryUsed = info['memory.used']
        self.utilization = info['utilization.gpu']
        self.throttled = info['throttled']
    def updateTasks(self,tasks):
        self._tasks = tasks
    def _clearTask(self):
        if self._tasks:
            self._tasks = []
    @property
    def users(self):
        return [task['User'] for task in self._tasks if 'User' in task]
    @property
    def utilization(self):
        return self._utilization
    @utilization.setter
    def utilization(self,value):
        if isinstance(value,int) or isinstance(value,float):
            self._utilization = int(value)
        else:
            self._utilization = int(value.split(' ')[0])
    @property
    def processes(self):
        return [task['Process'] for task in self._tasks if 'Process' in task]
    def __str__(self):
        pass
    @property
    def powerDraw(self):
        return self._powerDraw
    @powerDraw.setter
    def powerDraw(self, value):
        if isinstance(value,int) or isinstance(value,float):
            self._powerDraw = value
        else:
            self._powerDraw = float(value.split(' ')[0])
    @property
    def fanSpeed(self):
        return self._fanSpeed
    @fanSpeed.setter
    def fanSpeed(self, value):
        if value !='[Not Supported]':
            self._fanSpeed = float(value.split(' ')[0])
        elif isinstance(value,int) or isinstance(value,float):
            self._fanSpeed = value
        else:
            self._fanSpeed = -1
    @property
    def memoryTotal(self):
        return self._memoryTotal
    @memoryTotal.setter
    def memoryTotal(self,value):
        self._memoryTotal = self.memoryValueHandler(value)
    @property
    def memoryUsed(self):
        return self._memoryUsed
    @memoryUsed.setter
    def memoryUsed(self,value):
        self._memoryUsed = self.memoryValueHandler(value)
    @property
    def memoryUsagePercentage(self):
        return self.memoryUsed*100 / self.memoryTotal
    @property
    def memoryFree(self):
        return self.memoryTotal - self.memoryUsed
    @property
    def temperature(self):
        return self._temperature
    @temperature.setter
    def temperature(self,value):
        if isinstance(value,str):
            self._temperature = float(value)
        else:
            self._temperature = value
    def memoryValueHandler(self,value):
        processedValue = None
        if isinstance(value,int) or isinstance(value,float):
            processedValue = float(value)
        else:
            processedValue = float(value.split(' ')[0])
        return processedValue
class GPUDashboard(object):
    def __init__(self):
        self._initGPUs()
        self._assignTasks()
        self._lastOutputs = {}
    def _initGPUs(self):
        self.gpus = {}
        gpuInfos = getGPUInfo()
        for uuid in gpuInfos:
            self.gpus[uuid] = GPU(gpuInfos[uuid])
    def _assignTasks(self):
        tasks = getGPUTasksInfo()
        groupedTask = tasksGroupbyGPU(tasks)
        for uuid in self.gpus:
            if uuid in groupedTask:
                self.gpus[uuid].updateTasks(groupedTask[uuid])
            else:
                self.gpus[uuid]._clearTask()
    def _checkGPU(self,gpuInfos):
        flag = False
        if len(self.gpus) == len(gpuInfos):
            flag = True
        return flag
    def _updateGPUInfo(self):
        gpuInfos = getGPUInfo()
        if self._checkGPU(gpuInfos):
            for uuid in gpuInfos:
                self.gpus[uuid].updateInfo(gpuInfos[uuid])
        else:
            self._initGPUs()
            self._updateGPUInfo()
    def __str__(self):
        formatedInfos = []
        for gpu in list(self.gpus.values()):
            formatedInfos.append('{name}: Usage={usage}\tmemory={memusage:2d}%'.format(name=gpu.name,usage=gpu.utilization,memusage=int(gpu.memoryUsagePercentage)))
        return '\n'.join(formatedInfos)
    def update(self):
        self._updateGPUInfo()
        self._assignTasks()
    def outputChangedInfo(self):
        '''
        return a json string contain updated information of GPUs comparing with last time ouput.
        '''
        currentOutputs = self.outputInfo()
        lastOutputs = self._lastOutputs
        changed = {}
        for gpuIndex in currentOutputs:
            currentGpuInfo = currentOutputs[gpuIndex]
            if gpuIndex in lastOutputs: 
                lastGpuInfo = lastOutputs[gpuIndex]
                changedGpuInfo = {}
                for propertyName in currentGpuInfo:
                    if propertyName in lastGpuInfo:
                        if currentGpuInfo[propertyName] != lastGpuInfo[propertyName]:
                            changedGpuInfo[propertyName] = currentGpuInfo[propertyName]
                    else:               
                        changedGpuInfo[propertyName] = currentGpuInfo[propertyName]
                changed[gpuIndex] = changedGpuInfo
            else:
                changed[gpuIndex] = currentGpuInfo
        self._lastOutputs = currentOutputs
        return changed
    def outputInfo(self):
        out = {}
        logDateTime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S GMT")
        for gpu in self.gpus.values():
            fanSpeed = 'N/A' if gpu.fanSpeed<0 else int(gpu.fanSpeed)
            processes= ','.join(gpu.processes) if gpu.processes else ''
            users= ','.join(gpu.users) if gpu.users else ''
            memoryUsage = int(gpu.memoryUsagePercentage)
            memoryFree = int(gpu.memoryFree)
            out[gpu.index] = {'Fan':fanSpeed,'GPUID':gpu.index,'Name':gpu.name,
              'Power':gpu.powerDraw,'Processes':processes,'Temperature':gpu.temperature,
              'Users':users,'Utilization':gpu.utilization,'MemoryUsage':memoryUsage,
              'MemoryFree':memoryFree,'throttled':gpu.throttled,
              'logDateTime':logDateTime }
        return out
        