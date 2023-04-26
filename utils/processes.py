"""
    Returns processes on system
"""

import psutil 
import time
# .cpu_times()
# .pids()


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
