import os
import sys
import time
import logging
import socket
import win32serviceutil
import win32service
import win32event
import servicemanager
from rpyc.utils.server import ThreadedServer
from bbtest.rpyc import BBTestService
import shutil


DEFAULT_RPYC_SERVER_PORT = os.environ.get('BBTEST_DEFAULT_RPYC_SERVER_PORT', 57911)


class BBTestWinService(object):
    """A container for an RPyC server serving our bbtest RPyC logic"""
    HOSTNAME = "0.0.0.0"
    SERVER_LOG_DIR = "C:\\Users\\bbtest\\logs"
    SERVER_LOG_FILENAME = "BBTest_server_service.log"
    FALLBACK_LOG_DIR = "C:\\Temp"

    def __init__(self):
        """The server of the underlying rpyc package"""
        self._rpyc_server = None

    def start_rpyc_server(self):
        self._init_logger()
        self._rpyc_server = ThreadedServer(BBTestService, hostname=self.HOSTNAME, port=DEFAULT_RPYC_SERVER_PORT,
                                           logger=self.logger)
        self._rpyc_server.start()

    def stop_rpyc_server(self):
        self._rpyc_server.close()
        # TODO: why sleep? why 2?
        time.sleep(2)

    def _init_logger(self):
        self._init_logger_dir()
        handler = logging.FileHandler(os.path.join(self.log_dir, self.SERVER_LOG_FILENAME), mode="w+")
        handler.setFormatter(
            logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        )
        self.logger = logging.Logger("Bbtest_server", level=logging.DEBUG)
        self.logger.addHandler(handler)

    def _init_logger_dir(self):
        """Create log directory if needed.

        In case of failure, fall back to an always-present directory
        """
        if os.path.isdir(self.SERVER_LOG_DIR):
            self.log_dir = self.SERVER_LOG_DIR
        else:
            try:
                os.makedirs(self.SERVER_LOG_DIR)
                self.log_dir = self.SERVER_LOG_DIR
            except (IOError, WindowsError) as e:
                print(e)
                print("Server log dir does not exist and could not be created, falling back to %s" % self.FALLBACK_LOG_DIR)
                self.log_dir = self.FALLBACK_LOG_DIR


class BBTestWinServiceAdapter(win32serviceutil.ServiceFramework):
    """Windows service implementing the Rpyc server"""
    # standard members
    _svc_name_ = "BBTestServer"
    _svc_display_name_ = "BBTest Server"
    _svc_description = "BBTest server"

    def __init__(self, args):
        # no super - we inherit from an old-style class (yuck)
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.rpyc_server = BBTestWinService()
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        try:
            self.rpyc_server.stopRpycServer()
        except Exception as _:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                                  servicemanager.PYS_SERVICE_STOPPED,
                                  (self._svc_name_, f'Failed to stop {self._svc_name_}'))
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, f'{self._svc_name_} is started..'))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.rpyc_server.start_rpyc_server()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    @classmethod
    def service_main(cls):
        win32serviceutil.HandleCommandLine(cls)


def main():
    site_packages = os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages')
    src = os.path.join(os.path.join(site_packages, 'pywin32_system32', 'pywintypes37.dll'))
    dst = os.path.join(os.path.join(site_packages, 'win32', 'pywintypes37.dll'))
    if not os.path.isfile(dst):
        shutil.copy(src, dst)
    BBTestWinServiceAdapter.service_main()


if __name__ == '__main__':
    main()
