"""
    Returns processes on system
"""

import psutil 
import time
import datetime
import re

def formatSize(size):
    kb = 1024
    mb = 1048576
    gb = 1073741824
    if size < mb:
        size = round(size / kb, 2)
        return f'{size} KB'
    elif size < gb:
        size = round(size / mb, 2)
        return f'{size} MB'
    else:
        size = round(size / gb, 2)
        return f'{size} GB'

def diskData():
    disks = psutil.disk_partitions()
    real_disk_list = list()
    
    # remove virtual disks
    filtered = filter(lambda disk: not re.search("loop", disk.device), disks)
    real_disk_list = list(filtered)

    _data = []
    for disk in real_disk_list:
        mountpoint = disk.mountpoint
        disk_details = psutil.disk_usage(mountpoint)
        total = formatSize(disk_details.total)
        used = formatSize(disk_details.used)
        percent = disk_details.percent

        _data.append(
                {
                    "device" : disk.device,
                    "directory" : disk.mountpoint,
                    "type" : disk.fstype,
                    "total" : total,
                    "used" : used,
                    "percent" : int(percent)
                    }
                )

    return _data



def processes():
    _process_list = []
    for process in psutil.pids():
        # try except to prevent non root execution
        try:
            pid = process
            p = psutil.Process(process)
            name = p.name()
            exe = p.exe()
            user = p.username()
            createTime = p.create_time()
            now = time.time()
            uptime = (now - createTime)
            niceness = p.nice()
            status = p.status()
            cpu = p.cpu_percent()
            p_dict = {
                    "details": {
                        "name" : name,
                        "user" : user,
                        "pid" : pid,
                        "status" : status,
                        "uptime" : uptime,
                        "cpu" : cpu,
                        "niceness" : niceness
                        },
                    "process" : p
                    }

            #_list = [name, user, pid, uptime, cpu, niceness]
            _process_list.append(p_dict)
        except:
            pass
    return _process_list

def process_info(pid):
    p = psutil.Process(pid)
    proc_dict = {
            "name": p.name(),
            "pid": p.pid,
            "user": p.username(),
            "command line": ", ".join(p.cmdline()),
            "started": datetime.datetime.fromtimestamp(p.create_time()).strftime("%d-%m-%Y %H:%M:%S"),
            "uptime": time.time() - p.create_time(),
            "cpu time user": p.cpu_times().user,
            "cpu time kernel": p.cpu_times().system, 
            #"memory": p.
            "open files": len(p.open_files()),
            "connections": len(p.connections()),
            "memory - rss": p.memory_info().rss,
            "memory - vms": p.memory_info().vms,
            "memory - shared": p.memory_info().shared,
            "memory - text": p.memory_info().text,
            "memory - lib": p.memory_info().lib,
            "memory - data": p.memory_info().data,
            "memory - dirty": p.memory_info().dirty,
            "nice": p.nice(),
            }
    return proc_dict
