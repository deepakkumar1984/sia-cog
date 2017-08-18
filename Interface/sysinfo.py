import platform
import psutil
import pynvml
import jsonpickle
import math
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
    try:
        pynvml.nvmlInit()
        count = pynvml.nvmlDeviceGetCount()
        if count == 0:
            return None

        result = {"driver": pynvml.nvmlSystemGetDriverVersion(),
                  "gpu_count": int(count)
                  }
        i = 0
        gpuData = []
        while i<count:
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            gpuData.append({"device_num": i, "total": round(float(mem.total)/1000000000, 2), "used": round(float(mem.used)/1000000000, 2)})
            i = i+1

        result["devices"] = jsonpickle.encode(gpuData, unpicklable=False)
    except Exception as e:
        result = None

    return result
