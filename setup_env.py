

import subprocess
import sys
from setting import *


class VirtualEnvManager:
    
    @staticmethod
    def get_venv_pyhton():
        '''     get the venv python path    '''

        if sys.platform == "win32":
            venv_python = VENV_PATH / "Scripts" / "python.exe"
        else:
            venv_python = VENV_PATH / "bin" / "python"
        return venv_python



    @staticmethod
    def update_requirements():
        '''     update the requirements    '''
        '''     if file not found, create it    '''
        req_path = BASE_DIR / 'requirements.txt'
        if req_path.exists():
            print('✓ requirements.txt found')
        else:
            req_path.touch()
            print('✓ requirements.txt created')
        
        print('Updating requirements.txt from virtual environment...')
        try:
            result = subprocess.run(
                [str(VirtualEnvManager.get_venv_pyhton()), "-m", "pip", "freeze"],
                check=True,
                capture_output=True,
                text=True
            )
            req_path.write_text(result.stdout)
            print("✓ requirements.txt updated successfully!")
        except FileNotFoundError:
            print(f"✗ Error: Virtual environment Python not found at {VirtualEnvManager.get_venv_pyhton()}")
            print("  Please make sure the virtual environment exists and is properly set up.")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error updating requirements: {e}")
            if e.stderr:
                print(f"  Details: {e.stderr}")
        except Exception as e:
            print(f"✗ Unexpected error updating requirements: {e}")




    
    @staticmethod
    def setup_virtualenv():

        '''     setup the virtualenv    '''

        if VENV_PATH.exists(): 
            print("✓ Virtual environment already exists")
            return True
        else: 
            print(f"Creating virtual environment at {VENV_PATH}...")
            try:
                subprocess.run([sys.executable, "-m", "venv", str(VENV_PATH)], check=True)
                print("✓ Virtual environment created successfully!")
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ Error creating virtual environment: {e}")
                return False
            except Exception as e:
                print(f"✗ Unexpected error creating virtual environment: {e}")
                return False


    @staticmethod
    def install_requirements():

        '''     install the requirements    '''
        '''  if file not found, install the default requirements   '''

        # اول مطمئن بشیم venv وجود داره
        if not VENV_PATH.exists():
            print("Virtual environment not found. Creating it first...")
            if not VirtualEnvManager.setup_virtualenv():
                print("✗ Cannot proceed with installation. Virtual environment creation failed.")
                return False

        venv_python = VirtualEnvManager.get_venv_pyhton()
        if not venv_python.exists():
            print(f"✗ Error: Python executable not found in venv at {venv_python}")
            print("  Virtual environment might be corrupted. Please delete it and try again.")
            return False

        req_path = BASE_DIR / 'requirements.txt'
        if req_path.exists():
            print(f"✓ Found requirements.txt. Installing packages...")
            try:
                result = subprocess.run(
                    [str(venv_python), "-m", "pip", "install", "-r", str(req_path)],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("✓ Requirements installed successfully!")
                VirtualEnvManager.update_requirements()
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ Error installing requirements from file: {e}")
                if e.stderr:
                    print(f"  Details: {e.stderr}")
                return False
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
                return False
        else:
            print("requirements.txt not found. Installing default requirements...")
            try:
                subprocess.run(
                    [str(venv_python), "-m", "pip", "install", *DEFAULT_REQUIREMENTS],
                    check=True
                )
                print("✓ Default requirements installed successfully!")
                VirtualEnvManager.update_requirements()
                return True
            except subprocess.CalledProcessError as e:
                print(f"✗ Error installing default requirements: {e}")
                if e.stderr:
                    print(f"  Details: {e.stderr}")
                return False
            except Exception as e:
                print(f"✗ Unexpected error: {e}")
                return False


