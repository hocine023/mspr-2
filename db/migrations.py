import subprocess
import sys
import os

def execute_python_files(directory, exclude_files=None):
    """
    Exécute tous les fichiers Python dans le répertoire donné, sauf ceux exclus.
    """
    if exclude_files is None:
        exclude_files = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename not in exclude_files:
            filepath = os.path.join(directory, filename)
            print(f"Exécution de {filepath}...")
            subprocess.run([sys.executable, filepath], check=True)

if __name__ == "__main__":
    models_directory = os.path.join(os.getcwd(), "models")
    
    
    if os.path.exists(models_directory):
        execute_python_files(models_directory, exclude_files=["config_db.py", "__init__.py"])
    else:
        print(f"Le répertoire {models_directory} n'existe pas.")
    

