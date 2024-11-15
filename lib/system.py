import os
import subprocess
import logging
import psutil

log = logging.getLogger(__name__)


# Function to get the current temperature
def get_temperature():
    try:
        temp = subprocess.check_output(["sudo", "vcgencmd", "measure_temp"]).decode()
        return float(temp.split("=")[1].split("'")[0])  # Extract temperature
    except Exception as e:
        log.error("Failed to get temperature from vcgencmd: %s", e)
        return {"temp": 0}


# Function to get CPU usage percentage
def get_cpu_usage():
    try:
        return {
            "percent": psutil.cpu_percent(interval=0.01)
        }  # Returns CPU usage in percentage
    except Exception as e:
        return f"Error getting CPU usage: {e}"


# Function to get memory usage
def get_memory_usage():
    try:
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024**2), 2),
            "used": round(mem.used / (1024**2), 2),
        }
    except Exception as e:
        return f"Error getting memory usage: {e}"


# Function to get network usage (bytes sent and received)
def get_network_usage():
    try:
        net = psutil.net_io_counters()
        return {
            "sent": round(net.bytes_sent / (1024**2), 2),
            "recv": round(net.bytes_recv / (1024**2), 2),
        }
    except Exception as e:
        return f"Error getting network usage: {e}"


def get_hostname():
    return os.uname()[1]


def get_uptime():
    try:
        # Read the system uptime from /proc/uptime
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])

        # Calculate days, hours, minutes, and seconds
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        # Return as a formatted string
        return f"{days}d {hours}h {minutes}m {seconds}s"
    except Exception as e:
        return f"Error getting uptime: {e}"
