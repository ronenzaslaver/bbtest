
import os
import re
import platform
import time
import psutil
from psutil import NoSuchProcess
try:
    from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, QueryValueEx
except Exception:
    pass

from bbtest.target import subprocess_run


PROCESS_TIMEOUT_RETRIES = os.environ.get('BBTEST_PROCESS_TIMEOUT_RETRIES', 1)


def is_windows():
    return 'windows' in platform.system().lower()


def is_linux():
    return 'linux' in platform.system().lower()


def is_mac():
    return 'darwin' in platform.system().lower()


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
        except (psutil.AccessDenied, psutil.ZombieProcess, OSError) as e:
            pass
        except psutil.NoSuchProcess:
            continue
        if name == name_ or (cmdline and cmdline[0]) == name or os.path.basename(exe) == name:
            processes.append(name)
    return processes


def is_service_running(name):
    if is_windows():
        try:
            return psutil.win_service_get(name).status() == 'running'
        except NoSuchProcess:
            return False
    elif is_linux():
        return subprocess_run(['systemctl', 'is-active', name]).stdout.strip() == b'active'
    elif is_mac():
        command = f'sudo launchctl list | awk \'$3=="{name}" {{ print $2 }}\''
        return True if subprocess_run.target.run(command, shell=True)[0] == '0' else False
    else:
        raise NotImplementedError('Sorry, operating system is not suuported')


try:
    regedit_products = [OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')]
    regedit_products.append(OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\WOW6432Node\CurrentVersion\Uninstall'))
except Exception:
    pass


def get_package_version(name):
    name_re = re.compile(name)
    for products in regedit_products:
        i = 0
        while True:
            try:
                product_key_name = EnumKey(products, i)
            except OSError as e:
                break
            product_values = OpenKey(products, product_key_name)
            try:
                display_name = QueryValueEx(product_values, 'DisplayName')[0]
                if name_re.findall(display_name):
                    return QueryValueEx(product_values, 'DisplayVersion')[0]
            except FileNotFoundError:
                # product has no 'DisplayName' attribute
                pass
            i += 1
    raise RuntimeError(f'Package {name} version not found')


def open_key(parent_key, key):
    parent = OpenKey(HKEY_LOCAL_MACHINE, parent_key)[0]
    return QueryValueEx(parent, key)[0]
