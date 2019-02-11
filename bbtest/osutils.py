
import os
import psutil
import time


PROCESS_TIMEOUT_RETRIES = os.environ.get('BBTEST_PROCESS_TIMEOUT_RETRIES', 1)


def is_process_running(id, timeout=PROCESS_TIMEOUT_RETRIES):
    """ Returns True is process is running (listed in the process list).

    :param id: process ID - currently supports only name.
    :param timeout: time in seconds to wait for the process to get to running state.
    :return: True - process running, Flase - process not running.
    """
    for _ in range(0, timeout):
        if find_process_by_name(id):
            return True
        time.sleep(1)
    return False


def find_process_by_name(name):
    """ Find all processes that contains 'name' in the processes' name(), cmdline() or exe().

    :param name: process name.
    :return: list of processes matching 'name'."
    """
    assert name, f'Process name is {name}'
    processes = []
    for process in psutil.process_iter():
        name_, exe, cmdline = "", "", []
        try:
            name_ = process.name()
            cmdline = process.cmdline()
            exe = process.exe()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except psutil.NoSuchProcess:
            continue
        if name == name_ or (cmdline and cmdline[0]) == name or os.path.basename(exe) == name:
            processes.append(name)
    return processes
