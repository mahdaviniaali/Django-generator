

import subprocess
import os
import sys
from setting import *


class VirtualEnvManager:
    
    def setup_virtualenv():
        if VENV_PATH.exists(): 
            print("Virtual environment already exists")
        else: 
            subprocess.run([sys.executable, "-m", "venv", str(VENV_PATH)]) 

    