from cx_Freeze import setup, Executable
import sys
import os

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

build_exe_options = {
    "packages": ["tkinter", "re", "random"],
    "include_files": [],
    "excludes": [],
    "optimize": 1
}

try:
    import numpy
    build_exe_options["packages"].append("numpy")
except ImportError:
    print("Numpy não encontrado - usando fallback simplificado")

setup(
    name="ChatbotFoguetesUFPE",
    version="2.0",
    description="Chatbot NLP para Foguetes Experimentais - UFPE",
    options={"build_exe": build_exe_options},
    executables=[Executable("chatbot_foguetes.py", base=base)]
)
