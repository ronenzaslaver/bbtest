
import subprocess
import logging

logger = logging.getLogger('bblog')


def run(*args, **kwargs_in):
    kwargs = kwargs_in.copy()
    kwargs['stdout'] = subprocess.PIPE
    kwargs['stderr'] = subprocess.PIPE
    kwargs['shell'] = True
    logger.debug(f'running a subprocess {args} {kwargs}')
    output = subprocess.run(list(args), **kwargs)
    logger.debug(f'  returned: {output.stdout}')
    return output
