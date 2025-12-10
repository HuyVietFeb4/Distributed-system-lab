import subprocess
from lab_4 import config

def generate_metric_data():
    result = {}
    for i in range(6):
        result[config.METRICS[i]] = subprocess.run(config.COMMANDS[i], shell=True, capture_output=True, text=True, check=True).stdout.strip()
    
    config.DATA.append(result)
    return result