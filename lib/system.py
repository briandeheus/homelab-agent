import subprocess

import psutil


# Function to get the current temperature
def get_temperature():
    try:
        temp = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        return float(temp.split("=")[1].split("'")[0])  # Extract temperature
    except Exception as e:
        return {"temp": 0}


# Function to get CPU usage percentage
def get_cpu_usage():
    try:
        return {
            "percent": psutil.cpu_percent(interval=1)
        }  # Returns CPU usage in percentage
    except Exception as e:
        return f"Error getting CPU usage: {e}"


# Function to get memory usage
def get_memory_usage():
    try:
        mem = psutil.virtual_memory()
        return {
            "total": mem.total / (1024**2),  # Convert to MB
            "used": mem.used / (1024**2),  # Convert to MB
            "percent": mem.percent,  # Percentage used
        }
    except Exception as e:
        return f"Error getting memory usage: {e}"


# Function to get network usage (bytes sent and received)
def get_network_usage():
    try:
        net = psutil.net_io_counters()
        return {"bytes_sent": net.bytes_sent, "bytes_recv": net.bytes_recv}
    except Exception as e:
        return f"Error getting network usage: {e}"
