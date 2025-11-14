
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent
VENV_PATH = BASE_DIR / "venv"



DEFAULT_REQUIREMENTS = [
    "Django>=4.2.0",                    
    "djangorestframework>=3.14.0",      
    "django-cors-headers>=4.3.0",       
    "python-decouple>=3.8",             
    "Pillow>=10.0.0",                   
    "psycopg2-binary>=2.9.0",           
]