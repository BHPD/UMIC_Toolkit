# UMIC_Toolkit
Common custom Python scripts used for UMIC-related workflows. These workflows have been translated to a GUI for accessibility. Note this is still work-in-progress.

## Usage
The GUI can be launched from the command line or packaged into an .exe. First the appropriate environment will have to be created and the repository has to be cloned.

### Create environment
A requirements.txt will follow in later versions. 

### Clone the repository
Navigate to your directory, and: 
```bash
git clone https://github.com/BHPD/UMIC_Toolkit.git
cd UMIC_Toolkit
```

### (Optional) package the GUI into a .exe for convenience
Change the build.spec file such that the absolute paths are correct for your computer.
Using PyInstaller:
```bash
pyinstaller build.spec --clean
```

### Launch GUI
Activate the appropriate environment.
Navigate to the directory where the repository is cloned.
```bash
python main.py
```
