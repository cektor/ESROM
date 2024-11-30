# ESROM
This application allows you to convert between text and Morse code, and also allows you to listen to Morse code by voice. It has a graphical user interface and is cross-platform.

<h1 align="center">ESROM Logo</h1>

<p align="center">
  <img src="esromlo.png" alt="ESROM Logo" width="150" height="150">
</p>


----------------------

# Linux Screenshot
![Linux(pardus)](screenshot/esrom_linux.png)  

# Windows Screenshot
![Windows(11)](screenshot/esrom_windows.png) 

--------------------
Install Git Clone and Python3

Github Package Must Be Installed On Your Device.

git
```bash
sudo apt install git -y
```

Python3
```bash
sudo apt install python3 -y 

```

pip
```bash
sudo apt install python3-pip

```

# Required Libraries

PyQt5
```bash
pip install PyQt5
```
PyQt5-sip
```bash
pip install PyQt5 PyQt5-sip
```

PyQt5-tools
```bash
pip install PyQt5-tools
```

Required Libraries for Debian/Ubuntu
```bash
sudo apt-get install python3-pyqt5
sudo apt-get install qttools5-dev-tools
```
pygame
```bash
pip install pygame
```

numpy
```bash
pip install numpy

```

----------------------------------


# Installation
Install ESROM

```bash
sudo git clone https://github.com/cektor/ESROM.git
```
```bash
cd ESROM
```

```bash
python3 esrom.py

```

# To compile

NOTE: For Compilation Process pyinstaller must be installed. To Install If Not Installed.

pip install pyinstaller 

Linux Terminal 
```bash
pytohn3 -m pyinstaller --onefile --windowed esrom.py
```

Windows VSCode Terminal 
```bash
pyinstaller --onefile --noconsole esrom.py
```

MacOS VSCode Terminal 
```bash
pyinstaller --onefile --noconsole esrom.py
```

# To install directly on Windows or Linux





Linux (based debian) Terminal: Linux (debian based distributions) To install directly from Terminal.
```bash
wget -O Setup_Linux64.deb https://github.com/cektor/ESROM/releases/download/1.00/Setup_Linux64.deb && sudo apt install ./Setup_Linux64.deb && sudo apt-get install -f -y
```

Windows Installer CMD (PowerShell): To Install from Windows CMD with Direct Connection.
```bash
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cektor/ESROM/releases/download/1.00/Setup_Win64.exe' -OutFile 'Setup_Win64.exe'" && start /wait Setup_Win64.exe
```

Release Page: https://github.com/cektor/ESROM/releases/tag/1.00

----------------------------------

