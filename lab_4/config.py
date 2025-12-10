import subprocess

COMMANDS = [
    r"""free | awk '/^Mem:/ { printf("%.2f\n", $3/$2 * 100) }'""",
    """top -bn1 | grep "Cpu(s)" | awk '{print 100 - $8}'""",
    """iostat -d -k 1 2 | awk 'NR>7 {read+=$3} END {print read}'""",
    """iostat -d -k 1 2 | awk 'NR>7 {write+=$4} END {print write}'""",
    """ifstat -i wlp0s20f3 1 1 | awk 'NR>2 {print $1}'""",
    """ifstat -i wlp0s20f3 1 1 | awk 'NR>2 {print $2}'"""
]
METRICS = [
    "Memory Usage",
    "CPU Usage",
    "Read IO Usage",
    "Write IO Usage",
    "Network In Usage",
    "Network Out Usage",
]

DATA = []

HOST = subprocess.run("hostname -I", shell=True, capture_output=True, text=True, check=True).stdout.split(" ")[0]
INTERVAL = 5