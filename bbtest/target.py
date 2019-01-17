
import subprocess
import logging

logger = logging.getLogger('bblog')


def run(args, **kwargs_in):
    kwargs = kwargs_in.copy()
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    logger.debug(f'running a subprocess {args} {kwargs}')
    output = subprocess.run(args, **kwargs)
    logger.debug(f'  returned: {output.stdout}')
    if output.returncode > 0:
        raise subprocess.SubprocessError(f'subprocess run "{args} {kwargs}" failed on target\n'
                                         f'stdout = {output.stdout}\n'
                                         f'stderr = {output.stderr}')
    return output.stdout
