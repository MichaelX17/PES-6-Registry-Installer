# PES 6 Registry Installer

| ![image1](https://github.com/user-attachments/assets/9fdfe5be-558d-4800-89d1-c8256a0414c0) | ![image2](https://github.com/user-attachments/assets/87996aa9-445d-44bf-8f3b-16631d14ce90) |


*A lightweight utility to automate PES 6 registry configuration on Windows systems (x86/x64). No manual .reg files required!*

---

## 📥 Prerequisites

- **Windows 7/8/10/11 (Not tested in WinXP)** (32-bit or 64-bit)
- **Git Bash** (recommended for compilation)
- Files from `./assets` folder:
  - `python-3.4.0.msi`
  - `pywin32-221.win32-py3.4.exe`
  - `pefile-2017.11.5.tar.gz`
  - `PyInstaller-3.2.tar.gz`
  - UPX binaries (`upx-5.0.0-win32.zip` / `upx-5.0.0-win64.zip`)

---

## 🛠 Full Compilation Guide

### 1. Install Python 3.4

```bash
# File: "assets\python-3.4.0.msi"
msiexec /i "assets\python-3.4.0.msi"
```

### 2. Install pywin32

```bash
# File: "./assets/pywin32-221.win32-py3.4.exe"
./assets/pywin32-221.win32-py3.4.exe
```

### 3. Install pip for Python 3.4

```bash
curl -O https://bootstrap.pypa.io/pip/3.4/get-pip.py
/c/Python34/python.exe get-pip.py --trusted-host pypi.python.org
```

### 4. Install required packages

```bash
/c/Python34/Scripts/pip.exe install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org future==0.18.2
/c/Python34/Scripts/pip.exe install ./assets/pefile-2017.11.5.tar.gz
/c/Python34/Scripts/pip.exe install ./assets/PyInstaller-3.2.tar.gz
```

### 5. Compile Executable

```bash
/c/Python34/Scripts/pyinstaller.exe pes6_reg_editor.spec --clean
```

### 6. Compress with UPX (OPTIONAL)

```bash
# Extract UPX from assets to C:\upx first
/c/upx/upx.exe --best --lzma --ultra-brute --force ./dist/pes6_reg_editor.exe
```

---

## 🚀 Usage Instructions

1. Navigate to `dist` folder  
2. Right-click `pes6_reg_editor.exe` → **Run as Administrator**  
3. Select installation language (English/Spanish)  
4. Click **Install**  
   *Success message will appear when done.*

---

## ⚠️ Troubleshooting

### Common UPX Error

**Error**:  
`GUARD_CF enabled PE files are not supported`

**Solution**:

```bash
/c/upx/upx.exe --best --ultra-brute --force ./dist/pes6_reg_editor.exe
```

### Missing Registry Entries

- Ensure you ran the executable **as Administrator**
- Verify Python 3.4 is installed at `C:\Python34`
- Check error logs in the application directory

---

## 📂 Repository Structure

```
PES-6-Registry-Installer/
├── assets/                   # Local dependencies
│   ├── python-3.4.0.msi
│   ├── pywin32-221.win32-py3.4.exe
│   ├── pefile-2017.11.5.tar.gz
│   ├── PyInstaller-3.2.tar.gz
│   └── upx-*.zip
├── pes6.ico                 # Application icon
├── pes6_reg_editor.py       # Main script
├── pes6_reg_editor.spec     # PyInstaller config
└── README.md                # This file
```

---

## 👥 Credits & Legal

- Developer: [MichaelX17](https://github.com/MichaelX17)  
- Icon Designer: MichaelX17  
- Tools: PyInstaller, UPX, pefile  

*Educational/preservation project. Not affiliated with Konami.*

**⚠️ Note**: All assets in `/assets` are provided for archival purposes only. Use at your own risk.
