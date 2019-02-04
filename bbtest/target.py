
import os
import platform
import subprocess
import logging
import tempfile
import socket
import shutil

logger = logging.getLogger('bblog')


def os_path_isfile(path):
    return os.path.isfile(path)


def os_path_getsize(path):
    return os.path.getsize(path)


def os_remove(path):
    try:
        os.remove(path)
    except OSError:
        pass


def os_chmod(path, mode):
    os.chmod(path, mode)


def os_walk(top, **kwargs):
    return os.walk(top, **kwargs)


def platform_platform():
    return platform.platform()


def platform_machine():
    return platform.machine()


def platform_system():
    return platform.system()


def tempfile_mkdtemp(**kwargs):
    return tempfile.mkdtemp(**kwargs)


def socket_gethostname():
    return socket.gethostname()


def shutil_rmtree(path, ignore_errors=True, onerror=None):
    return shutil.rmtree(path, ignore_errors, onerror)


def subprocess_run(args, **kwargs_in):
    """ run command on target via subprocess.run

    args and keywargs_in behave the same as args and keyvargs in subprocess.run.
    """
    kwargs = kwargs_in.copy()
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    logger.debug(f'running a subprocess {args} {kwargs}')
    output = subprocess.run(args, **kwargs)
    logger.debug(f'  returned: {output.stdout}')
    return output


def download_file(src_url, dst_path):
    """ Download file from URL to target file.

    :param src_url: source URL
    :type src_url: pathlib.Path
    :param dst_path: destination file path
    :type dts_path: str
    :return: destination path
    """
    logger.info(f'Downloading file from: {src_url}')
    with src_url.open(mode='rb') as in_file:
        with open(dst_path, 'wb') as out_file:
            out_file.write(in_file.read())
    logger.info(f'Downloaded file path on disk: {dst_path}')
    return dst_path
