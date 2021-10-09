import sys, os
INTERP = os.path.join(os.environ['HOME'], 'mwt.sh', 'venv', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from fhost import app as application