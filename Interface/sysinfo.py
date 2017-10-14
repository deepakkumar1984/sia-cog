import platform
import psutil
import pynvml
import jsonpickle
import subprocess

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
            gpuData.append({"device_num": i, "name": pynvml.nvmlDeviceGetName(handle), "total": round(float(mem.total)/1000000000, 2), "used": round(float(mem.used)/1000000000, 2)})
            i = i+1

        result["devices"] = jsonpickle.encode(gpuData, unpicklable=False)
    except Exception as e:
        result = {"driver": "No GPU!", "gpu_count": 0, "devices": []}

    return result

def getModuleInfo():
    result = []

    pkglist = ["Flask", "Cython", "Keras", "mxnet", "tensorflow", "cntk", "scikit-learn", "pandas", "matplotlib",
               "opencv-python", "pytesseract", "nltk", "ChatterBot", "padatious", "seaborn", "mpld3", "psutil",
               "nvidia-ml-py"]

    for p in pkglist:
        try:
            pkg = subprocess.check_output(["pip", "show", p])
            params = pkg.split('\n')
            modinfo = {}
            for p in params:
                kv = p.split(':')
                if len(kv) > 1:
                    if kv[0] != "Home-page":
                        modinfo[kv[0]] = kv[1].strip()
            result.append(modinfo)
        except Exception as e:
            result.append({"Name": p, "Error": str(e)})

    return result