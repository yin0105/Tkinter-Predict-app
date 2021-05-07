import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","tkinter","numpy","tkmagicgrid","styleframe","pandas","matplotlib","csv"]}
include_files = r'E:\Workspace\Django Projects\doc\3in1_desktopapp-main_25th April 2021\desktopapp-main\my_icon.ico'

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "code",
        version = "2.0",
        description = "the python code",
        options = {"build_exe": build_exe_options},
        executables = [Executable("UserPanel.py", icon="my_icon.ico", base=base),Executable("AdminPanel.py", icon="my_icon.ico", base=base)]
)
