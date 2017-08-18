import platform
import psutil
import pynvml
import jsonpickle
def getSystemInfo():
    result = {"machine": platform.machine(),
              "platform": platform.platform(),
              "processor": platform.processor(),
              "cpu_count": psutil.cpu_count(),
              "os": platform.system(),
              "python_compiler": platform.python_compiler(),
              "python_version": platform.python_version()}
    return result

def getCPUUsage():
    result = {"cpu_usage": psutil.cpu_percent(True),
              "mem_usage": psutil.virtual_memory().percent}

    pynvml.nvmlInit()
    pynvml.nvmlSystemGetDriverVersion()
    return result

def getGPUUsage():
    pynvml.nvmlInit()
    count = pynvml.nvmlDeviceGetCount()
    if count == 0:
        return None

    result = {"driver": pynvml.nvmlSystemGetDriverVersion(),
              "gpu_count": count
              }
    i = 0
    gpuData = []
    while i<count:
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
        gpuData.append({"device_num": i, "mem_usage": mem})
        i = i+1

    result["devices"] = jsonpickle.encode(gpuData, unpicklable=False)
    return result
