import sys
from cx_Freeze import setup, Executable
from Dlls_padrao import include_files

base = None
if sys.platform == "win32":
    base = "Win32GUI"
if sys.platform == "win64":
    base = "Win64GUI"
    
setup(
    name="Fatigue Life Calculator (FLC)",
    author="David Lucas Pereira (david.pereira@acad.ufsm.br)",
    version="1.0.0",
    description="Programa educativo para cálculo de Fadiga mecânica",
    options={'build_exe': {
        'includes': ["gi"],
        'excludes': ['wx', 'email', 'pydoc_data', 'curses'],
        'packages': ["gi"],
        'include_files': include_files
    }},
    executables=[
        Executable("FLC_executable.py",
                   base=base,
                   icon="application-x-executable.png",
                   shortcut_name="Life Fatigue Calculator",
                   shortcut_dir="FLC"
                   )
    ]
)
