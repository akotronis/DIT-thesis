## UV
### Installation
- Install `uv` (Linux/Git Bash): `$ curl -LsSf https://astral.sh/uv/install.sh | sh`
- Add `$HOME/.local/bin to PATH` (sh): `$ source $HOME/.local/bin/env`
- Enable shell autocompletion for uv commands (sh): `$ echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc`
- Check that uv is available: `$ uv`

### Project setup / Manage dependencies
- Initialize a project with uv: `../app/mobile$ uv init --python 3.12 --vcs none --no-readme`
- Create the virtual environment: `../app/mobile$ uv venv`
- Install python dependencies on virtual environment from requirements: `../app/mobile$ uv add -r requirements.txt`

### If project and `pyproject.toml` exists
- sync dependencies: `../app/mobile$ uv sync`

To change python version:
- Change _"requires-python"_ inside _pyproject.toml_
- Change contents of _.python-version_
- Run `../app/mobile$ uv sync`
- Verify with `../app/mobile$ uv pip list`

<!-- ### Run with *HotReload*
`../app/mobile/dit-app$ DEBUG=1 uv run -m main` -->


## KIVY
- [Kivy School](https://kivyschool.com/)
- [Youtube - KivyMD Tutorial - Setup Hot Reload With Kaki](https://www.youtube.com/watch?v=68vDrMpm5Vw)

### Hot Reloader/Build

- [KivySchool Guide](https://www.canva.com/design/DAGM8aS-fkw/CuY4HsxEK99frupa7pCnuQ/view?utm_content=DAGM8aS-fkw&utm_campaign=designshare&utm_medium=link&utm_source=editor#1) or [here](https://kivyschool.com/kivy-reloader/windows/wsl2-setup-targeting-android/)


1. Update NVIDIA drivers (?)

On Windows through windows admin Powershell:

2. `Chocolatey` installation on Windows
    - `C:\Windows\system32> Get-ExecutionPolicy`
    - If the above returns *Restricted*: `C:\Windows\system32> Set-ExecutionPolicy Bypass -Scope Process`
    - `C:\Windows\system32> Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))`
    - `C:\Windows\system32> choco` to verify installation
3. `scrcpy` installation on Windows through windows admin Powershell
    - `C:\Windows\system32> choco install scrcpy`
    - `C:\Windows\system32> adb` to verify installation
    - `C:\Windows\system32> scrcpy` on a new admin Command Prompt to verify installation

On WSL shell:

4. Update WSL `$ sudo apt-get update`
5. Install Buildozer/Buildozer dependencies
    - `$ sudo apt install zip unzip openjdk-17-jdk python3-pip cmake autoconf libtool pkg-config build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev libncurses5-dev libmtdev1 xclip xsel`
    - `$ sudo apt install libtinfo5` (For Ubuntu 20, 22)
    - `$ pip3 install --user --upgrade buildozer`
    - `$ pip3 install --upgrade Cython==0.29.33 virtualenv`
6. Install `scrcpy`
    - System: `$ sudo apt install ffmpeg libsdl2-2.0-0 adb wget gcc git pkg-config meson ninja-build libsdl2-dev libavcodec-dev libavdevice-dev libavformat-dev libavutil-dev libswresample-dev libusb-1.0-0 libusb-1.0-0-dev`
    - Clone and run installer: `cd ~ && git clone https://github.com/Genymobile/scrcpy && cd scrcpy && ./install_release.sh`

7. Setup and use Hot Reloader
    - `../app/mobile/dit-app$ uv run kivy-reloader init`

### Mobile
#### On mobile
- [Developer Options](https://developer.android.com/studio/debug/dev-options#enable)
    - Settings > About Phone > Sofware Information > Touch 7 times the Build Number
    - Go to Settings > System > Developer Options > Enable USB debugging
- Connect mobile to laptop with USB device

#### On windows
- Create a Firewall inbound rule on Control Panel > System and Security > Windows Defender Firewall > Advanced Settings to allow pinging windows host from wsl
    - Verify by pinging the ip from windows `ipconfig` from wsl (If doesnt work disable firewall temporarily, see below)
- Verify if adb versions on Windows and wsl are the same (`adb version`)
    - If not easier to modify windows installation. On admin shell:
        - `choco uninstall scrcpy`
        - Verify adb version: `C:\ProgramData\chocolatey\lib\adb\tools\platform-tools\adb.exe version`
        - Download `scrcpy` appropriate version from [here](https://github.com/Genymobile/scrcpy/releases/tag/v3.1)
        - Extract in on `C:\scrcpy` and 
        - Add `C:\scrcpy` on system env variables
        - `choco install adb --version=1.0.39`

#### On windows (Run adb/scrcpy)
- `C:\Users\akotr> adb kill-server`
- Check connected devices: `C:\Users\akotr> adb devices`
- `C:\Users\akotr> adb -a -P 5037 nodaemon server`
#### On WSL
- ***ADB***: `$ adb -P 5037 -H 192.168.1.37 devices` (Change ip with the output of `C:\Users\akotr> ipconfig` on _Wireless LAN adapter Wi-Fi => IPv4 Address_)
    - If this doesnt work, temporary disable firewall: On `C:\Windows\system32> netsh advfirewall set allprofiles state off` (Turn it on again with `C:\Windows\system32> .... on`)
- ***SCRCPY***: (To be exported again on restart since ip may be different):
    - `$ export ANDROID_ADB_SERVER_PORT=5037`
    - `$ export ADB_SERVER_SOCKET=tcp:<WINDOWS-IP>:5037`
    - `$ export ANDROID_ADB_SERVER_ADDRESS=<WINDOWS-IP>`
- `$ scrcpy` to see the mobile screen
- (***NOT REQUIRED***: `../app/mobile/dit-app$ kivy-reloader run` > Debug and Livestream)



### Development workflow
Build with
- `$ docker run --rm -it --entrypoint /bin/sh -v "$HOME/.gradle":/home/user/.gradle -v "$HOME/.buildozer":/home/user/.buildozer -v "$(pwd)":/home/user/hostcwd img-dit-buildozer -c "buildozer -v android debug"`
    - If **.buidozer** and **bin** folders are NOT deleted rebuild time reduces from **45-50 min** to **20 min**
    - Mounting **`$HOME/.gradle":/home/user/.gradle`** reduces rebuilds from **20-50 min** to **1-2 min**
    - Rebuild creates new apk and overwrites old
    - Code changes are reflected on mobile
- Delete app from mobile
- Install app to mobile: `$ adb -P 5037 -H 192.168.1.37 install bin/*.apk`
- Clear and follow logs `$ adb -P 5037 -H 192.168.1.37 logcat -c && adb -P 5037 -H 192.168.1.37 logcat *:S python:D`
- Run app from mobile