from __future__ import annotations

import os


def get_cpu_usage() -> float:
    """Calculate the current CPU usage percentage from /proc/stat."""
    try:
        with open("/proc/stat", "r", encoding="utf-8") as f:
            line = f.readline()
        parts = line.split()
        if len(parts) >= 5:
            # cpu user nice system idle iowait irq softirq steal guest guest_nice
            # Sum up active times vs idle times
            user, nice, system, idle = (
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
                float(parts[4]),
            )
            total = user + nice + system + idle
            # Use state delta if we poll dynamically, but for a simple calculation:
            active = user + nice + system
            if total > 0:
                return (active / total) * 100
    except Exception:
        pass
    return 0.0


def get_mem_usage() -> float:
    """Calculate the current memory usage percentage from /proc/meminfo."""
    try:
        mem_info: dict[str, float] = {}
        with open("/proc/meminfo", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    key = parts[0].replace(":", "")
                    mem_info[key] = float(parts[1])

        total = mem_info.get("MemTotal", 0.0)
        free = mem_info.get("MemFree", 0.0)
        buffers = mem_info.get("Buffers", 0.0)
        cached = mem_info.get("Cached", 0.0)

        # Actual used memory is Total - Free - Buffers - Cached
        used = total - free - buffers - cached
        if total > 0:
            return (used / total) * 100
    except Exception:
        pass
    return 0.0


def get_system_usage() -> dict[str, float]:
    """Retrieve all monitored system metrics as a dictionary."""
    return {
        "cpu": get_cpu_usage(),
        "memory": get_mem_usage(),
    }
