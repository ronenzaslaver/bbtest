
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
