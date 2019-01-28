
import subprocess
import logging

logger = logging.getLogger('bblog')


def run(args, **kwargs_in):
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
    with src_url.open() as in_file:
        with open(dst_path, 'wb') as out_file:
            out_file.write(in_file.read())
    logger.info(f'Downloaded file path on disk: {dst_path}')
    return dst_path
