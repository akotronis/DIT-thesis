# DIT-thesis
Repo for the HUA dit thesis project

## Configuration setup / Launch workflow
### Urls
- **Wireguard UI**: http://localhost:5000/global-settings
- **Front end**: http://localhost:8501
- **Back end**: http://localhost:8000
- **Localtonet**: https://localtonet.com/tunnel/tcpudp
- **Ngrok**: https://dashboard.ngrok.com/domains

### Localtonet
UDP tunnel to wireguard container
- URL: https://localtonet.com/tunnel/tcpudp
- Connects to local container **ctr-dit-wireguard** fixed IP:Port
- Start tunnel from Localtonet dashboard (May require to start local service first)
- Update port in server domain url where it is used
    - Wireguard ui global settings &rarr; Endpoint Address (see below)
    - Running **ctr-dit-localtonet** container updates automatically with server domain port changes

### Ngrok
TCP tunnel to wireguard ui container (Not required. only to access wireguard ui from mobile)
- URL: https://dashboard.ngrok.com/domains
- Connects to local container **ctr-dit-wireguard-ui** fixed IP:Port
- Tunnel is started automatically on local service launch with docker compose, no nned to start from Ngrok dashboard
- Use Ngrok domain to access wireguard ui from mobile browser

### Services
In WSL
- `../DIT-thesis/app$ docker compose up -d`
- Inspect ctr-dit-localtonet logs to make sure container is connected to localtonet server
- If back/front service launch commands are not in Dockerfiles, launch them manually
    - `../DIT-thesis/app$ docker exec -it ctr-dit-back bash -c "python manage.py runserver 0:8000"`
    - `../DIT-thesis/app$ docker exec -it ctr-dit-front bash -c "streamlit run main.py"`

### Wireguard configuration
- For potential wireguard ui invalid creds error or unresponsive login submition:
    - `../DIT-thesis/app$ sudo rm wireguard/ui/db/users/*`
    - `../DIT-thesis/app$ docker compose restart srv-dit-wireguard-ui`
    - Ctrl Shift R in browser before login
- Global Settings
    - Endpoint Address &rarr; `<localtonet-url>:<server-port>` (Check this is up to date with localtonet **server domain** setting)
    - Save
    - Global settings can be verified with `../DIT-thesis/app$ sudo cat wireguard/ui/db/server/global_settings.json`
- Wireguard Server
    - Post Up:  
`iptables -t nat -A POSTROUTING -s 10.252.1.0/24 -d 192.168.1.0/24 -j MASQUERADE; iptables -A FORWARD -i wg0 -d 192.168.1.0/24 -j ACCEPT; iptables -A FORWARD -s 192.168.1.0/24 -o wg0 -j ACCEPT; iptables -A INPUT -p udp -m udp --dport 51820 -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;`
    - Post Down:  
`iptables -t nat -D POSTROUTING -s 10.252.1.0/24 -d 192.168.1.0/24 -j MASQUERADE; iptables -D FORWARD -i wg0 -d 192.168.1.0/24 -j ACCEPT; iptables -D FORWARD -s 192.168.1.0/24 -o wg0 -j ACCEPT; iptables -D INPUT -p udp -m udp --dport 51820 -j ACCEPT; iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT;`
    - Save
    - Click **Apply Config** after updating server/client settings to reflect changes
- Wireguard Clients
    - New client
    - Enter name
    - Save
    - Click **Apply Config** after updating server/client settings to reflect changes
- Server/Client settings can be verified with `../DIT-thesis/app$ cat wireguard/ui/config/wg0.conf`

### Wireguard tunnel / client connection
- On wireguard ui select *QR code* on a created client
- On mobile side
    - Open Wireguard app
    - Click *+* button to create tunnel
    - Select *Scan from QR code*
    - Open created tunnel connection  by the toggle button
    - Inspect connection configuration by selecting it
    - Verify connection by
        - Opening *PingTools* app and ping address on Wireguard ui &rarr; Wireguard Server &rarr; Server Interface Addresses
        - Opening **192.168.1.102:8000/admin** on mobile browser
    - **Inspect accessile backend server and connect to it by opening the mobile DIT App and click on connetion top right icon**

### Troubleshooting
For connectivity problems make sure:
- Localtonet tunnel is running
- Local localtonet container is connected with localtonet server with up to date **server domain port** by inspecting logs.
    - If port changes from localtonet server and local container is running, the change will be updated automatically
    - Run `../DIT-thesis/app$ docker compose restart srv-dit-localtonet` if necessary
- Localtonet **server domain port** is aligned with Wireguard ui &rarr; Global Settings &rarr; Endpoint Address.  
    If port changes from localtonet server
    - Update Wireguard ui &rarr; Global Settings &rarr; Endpoint Address
    - Create new tunnel from mobile side for existing client (no need to create new client on wireguard ui side)

### Home Assistant
- [Install Home Assistant Container](https://www.home-assistant.io/installation/linux#install-home-assistant-container)
- [Troubleshooting installation problems](https://www.home-assistant.io/installation/troubleshooting/)
- Problem with accessing ui from the browser if launched with `network_mode: host` on docker compose in conjuction to docker desktop. See:
    - [HomeAssistant running on Docker Desktop for Windows but not accessible from browser](https://community.home-assistant.io/t/homeassistant-running-on-docker-desktop-for-windows-but-not-accessible-from-browser/370731)
    - [Installing HA on Docker in Windows desktop](https://community.home-assistant.io/t/installing-ha-on-docker-in-windows-desktop/529554)
    - [Help Needed: Cannot access Home Assistant via IP or http://homeassistant.local:8123 [Solved]](https://community.home-assistant.io/t/help-needed-cannot-access-home-assistant-via-ip-or-http-homeassistant-local-8123-solved/544900)
    - [Homeassisant in docker unreachable using network mode host](https://community.home-assistant.io/t/homeassisant-in-docker-unreachable-using-network-mode-host/498969)
- Access by the browser can be establishd if docker destop is updated to version `>=4.34`. See
    - [Docker Docs: Networking using the host network](https://docs.docker.com/engine/network/tutorials/host/#prerequisites) BUT
- Still devices can't be (auto)discoverd. See
    - [Home assistant on desktop docker help!](https://www.reddit.com/r/homeassistant/comments/1aq6bdb/comment/kqawzh1/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)
- Use **named volume** in the vm

#### Add Device
- Find Tapo IP from router page: _LAN settings_ &rarr; _Allocated Address (DHCP)_
- `vagrant@ubuntu2204:~/code/DIT-thesis$ curl http://192.168.1.13:80` to see if the device is accessible from the VM
- _Settings (Left Pane)_ &rarr; _Device & Settings_ &rarr; _Device Tab_ &rarr;  _Add Device (Bottom Right)_ &rarr; Search _Tp-Link_ &rarr; Select _Tapo_
- `$ sudo cat /var/lib/docker/volumes/app_dit-homeassistant-data/_data/.storage/core.config_entries` to see if the correct device IP is registered
    - If the device has not the correct id (the one from router's page) &rarr; _LAN settings_ &rarr; _Allocated Address (DHCP)_, delete the device and add it again
- [Integrations - TP-Link Smart Home](https://www.home-assistant.io/integrations/tplink)

#### Automation Creation
- [Youtube - Beginners guide to use Home Assistant’s webhooks like a pro (Technithusiast)](https://www.youtube.com/watch?v=znbdNh9wR0A&list=PLbj6wg8ZoGHkM0gVQBzA-FJlmKoRXhJu5&index=2)
- Left Pane _Settings_ &rarr; _Automations & scenes_ &rarr; _Create automation_ &rarr; _Create new automation_ &rarr; _Add a trigger_ &rarr; _Search for: Webhook (add ID)_ &rarr; _Add action_ &rarr; _Select Device_ &rarr; _Select Tapo p110_ and action _turn on_ &rarr; _Save_
- Same for _turn_off_
- `vagrant@ubuntu2204:~/code/DIT-thesis/app/ubuntu$ sudo rm -r homeassistant/config && sudo cp -r /var/lib/docker/volumes/app_dit-homeassistant-data/_data homeassistant/config` to get named volume contents to mounted folder

### VM
[Install Docker on Ubuntu](https://docs.docker.com/engine/install/ubuntu/#uninstall-old-versions)
1. Uninstall all conflicting packages
   - `$ for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done`
2. Install using the apt repository
   - `$ sudo apt-get update`
   - `$ sudo apt-get install ca-certificates curl`
   - `$ sudo install -m 0755 -d /etc/apt/keyrings`
   - `$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc`
   - `$ sudo chmod a+r /etc/apt/keyrings/docker.asc`
   - `$ sudo -i`
   - `# apt update`
   - `# apt install sudo`
   - `# exit`
   - `$ sudo --version`
   - `$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
   - `$ sudo apt-get update`
   - `$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`
   - `$ docker --version`
   - `$ sudo usermod -aG docker $USER`
   - `$ newgrp docker`

[Install Docker Compose on Ubuntu](https://docs.docker.com/compose/install/linux/#install-using-the-repository)
- `$ sudo apt-get update`
- `$ sudo apt-get install docker-compose-plugin`
- `$ docker compose version`

#### Troubleshooting

If `$ vagrant up` stucks on ssh:

***First Alternative***
- Run `$ vagrant halt`
- Open **VirtualBox** and in the settings of the vm, in **System** left pane and under **Acceleration** tab, make sure **Hardware virtualization** is **unchecked**. Click **Ok**
- `$ vagrant up` again and try to ssh

***Second Alternative***
1. On Vagrantfile folder: `$ vagrant halt`
2. Start vm from VirtualBox
3. If I am on a `(initramfs)` prompt
   - `(initramfs) $ fsck -y /dev/mapper/ubuntu--vg-ubuntu--lv` (maybe more than once)
   - `(initramfs) $ reboot`
   - `$ exit`
4. On Vagrantfile folder: `$ vagrant up`


## Resources
### General
- [How to Show Phone Screen on Windows PC Laptop!! - Howtosolveit](https://www.youtube.com/watch?v=SvpUtT3lZaE)
- [ExcaliDraw](https://excalidraw.com/)

### Wireguard/VPN/Hosting
- [Github - linuxserver.io](https://github.com/linuxserver/docker-wireguard?tab=readme-ov-file#usage)
- [Github - wg-easy](https://github.com/wg-easy/wg-easy)
- [Github - wg-easy/compose](https://github.com/wg-easy/wg-easy/blob/master/docker-compose.yml)
- [Github - wg-easy/config](https://github.com/wg-easy/wg-easy/blob/master/src/config.js#L19)
- [Techdox - Docker Compose Configuration for Wireguard and Wireguard UI](https://docs.techdox.nz/wireguard/#docker-compose-configuration-for-wireguard-and-wireguard-ui)
- [Youtube - Access Your Local Servers From Anywhere // Self Hosted VPN (Wireguard + Docker)](https://www.youtube.com/watch?v=AkKz7Vza1rw)
- [Youtube - Let's Install PiVPN On A Raspberry Pi](https://www.youtube.com/watch?v=zsN47t2r_WU&pp=ygUkbGV0cyBpbnN0YWxsIHBpdnBuIG9uIGEgcmFzcGJlcnJ5IHBp)
- [Youtube - Effortless Wireguard Installation with Docker and Portainer | Zimaboard Server Series](https://www.youtube.com/watch?v=QLL5lT0SDoQ)
- [Youtube - Access Your HOME NETWORK From ANYWHERE IN THE WORLD | Wireguard VPN](https://www.youtube.com/watch?v=AYQtlezVW2c)
- [Youtube - Cloudflare Zero Trust Tunnel Guide: Exposing Self-Hosted Services Safely](https://www.youtube.com/watch?v=gpWo94XXrhU)
- [Youtube - How To VPN Without Port Forwarding Using Headscale & Tailscale - Complete Tutorial](https://www.youtube.com/watch?v=u_6Zd7Bo6J4)
- [Youtube - Create your own VPN server with WireGuard in Docker](https://www.youtube.com/watch?v=GZRTnP4lyuo)
- [Youtube - Self Hosting your OWN VPN is EASY and FREE using Wireguard in Docker](https://www.youtube.com/watch?v=RktXcwwaYr0)

#### Cloudflare
- [Github - cloudflare tunnel](https://github.com/jonas-merkle/container-cloudflare-tunnel)
- [Codegito - How to host a webpage locally using Cloudflare Tunnels, Apache, and Docker](https://codegito.xyz/2024/12/01/cloudflare-apache-docker/)

#### Ngrok
- [ngrok - tunnel configuration - Version 2](https://ngrok.com/docs/agent/config/v2/#tunnel-configurations)
- [ngrok - Agent Config - Version 3](https://ngrok.com/docs/agent/config/v3/#endpoint-definitions)

#### Localtonet
- [How To Use Localtonet](https://localtonet.com/blog/how-to-use-localtonet)
- [Localtonet: An Ideal Solution for Systems Behind CGNAT](https://localtonet.com/documents/using-localtonet-with-cgnat)
- [Localtonet API](https://documenter.getpostman.com/view/17350314/2s9Y5YShx5#7b5da9fb-a1e6-4b7c-bdcb-dbf181069630)

#### Port Forwarding
- [OTE Speedport W 724V Router Port Forwarding Instructions](https://portforward.com/ote/speedport-w-724v/)
- [How to Forward Ports in a ZTE ZXHN H108N Router](https://portforward.com/zte/zxhn-h108n/)
- [How To Set Up a Static IP Address on Windows 11](https://portforward.com/static-ip-address-windows-11/)
- [DHCP Reservations - 5 Reasons You Need to Assign a Permanent Address to Devices on Your Network](https://portforward.com/dhcp-reservation/)
- [CanYouSeeMe.org - Open Port Check Tool](https://canyouseeme.org/)

#### Kivy/Kivymd
- [kivy official Docs](https://kivy.org/doc/stable/gettingstarted/intro.html)
- [kivymd Pypi](https://pypi.org/project/kivymd/)
- [kivymd Docs](https://kivymd.readthedocs.io/en/latest/)
- [kivymd Github (official examples)](https://github.com/kivymd/KivyMD/blob/master/examples/common_app.py)
- [kivymd Basics Github (attreyadhatt)](https://github.com/attreyabhatt/KivyMD-Basics/blob/master/4%20-%20Themes/main.py)
- [kaki Github](https://github.com/tito/kaki)
- [Kivy School - Hot Reloader - 1](https://kivyschool.com/kivy-reloader/windows/wsl2-setup-targeting-android/)
- [Kivy School - Hot Reloader - 2](https://kivyschool.com/kivy-reloader/windows/setup-and-how-to-use/#connect-windows-adb-to-wsl-adb-through-usb-cable)
- [Kivy School - Hot Reloader - PPTX Guides](https://www.canva.com/design/DAGM8aS-fkw/CuY4HsxEK99frupa7pCnuQ/view?utm_content=DAGM8aS-fkw&utm_campaign=designshare&utm_medium=link&utm_source=editor#49)
- [Erik Sandberg - Farmers' Market Finder App - Github](https://github.com/Dirk-Sandberg/FarmersMarketFinderTutorial/blob/master/part6/gpshelper.py)
- [Youtube - Farmers' Market Finder App - (Erik Sandberg)](https://www.youtube.com/playlist?list=PLy5hjmUzdc0mY-nC-Djhv_wJjQuWVmPV8)
- [Youtube - Learn to Make Beautiful Mobile Apps in Python | KivyMD Tutorial - MDChip(s) (Erik Sandberg)](https://www.youtube.com/watch?v=jJNyVQdPAeQ)
- [Youtube - Python KivyMD Building Mobile & Desktop Apps | KivyMD Emulator & HotReloadViewer | Live Design View (Spinn TV)](https://www.youtube.com/watch?v=gJ-E30uhWD0)
- [Youtube - MeditationApp (KivyMD)](https://www.youtube.com/watch?v=puNtm7Xa2tE)
- [Youtube - Designing LOGIN page using KIVYMD || Mobile App Development (The Club of Python Developers)](https://www.youtube.com/watch?v=2ImbdfgY0Gg)
- [Youtube - Python KivyMD Building Mobile & Desktop Apps | KivyMD Emulator & HotReloadViewer | Live Design View (Spinn TV)](https://www.youtube.com/watch?v=gJ-E30uhWD0&list=PLJ8t3BKaQLhNtZH_lVTI4Q1Qf9bCeuiAs)
- [Youtube - KivyMD Add Bottom And Top Navigation Toolbars | Multiple Screens | Python Tutorial | Live Design View (Spinn TV)](https://www.youtube.com/watch?v=-q14ljnO2cQ)
- [Youtube - Kivy Tutorial - Building Mobile Apps with Python | KivyMD (buildwithpython)](https://www.youtube.com/playlist?list=PLhTjy8cBISEpobkPwLm71p5YNBzPH9m9V)
- [Youtube - Kivy Tutorial - Building Games and Mobile Apps with Python (buildwithpython)](https://www.youtube.com/watch?v=RYF73CKGV6c&list=PLhTjy8cBISEpobkPwLm71p5YNBzPH9m9V)
- [Youtube - Beginner Kivy Android: Do THIS and AVOID Startup Crashes! (OSSnext)](https://www.youtube.com/watch?v=tWUkPflqA64)
- [Youtube - How to Download KIVY Buildozer For Zero PAIN APK | 2025 ANDROID (OSSnext)](https://www.youtube.com/watch?v=D79BtZQSH2A)
- [buildozer Pypi](https://pypi.org/project/buildozer/)
- [buildozer Docs](https://buildozer.readthedocs.io/en/latest/installation.html)
- [Github - buildozer image](https://github.com/kivy/buildozer/blob/master/Dockerfile)
- [Github - Android for Python Users](https://github.com/Android-for-Python/Android-for-Python-Users?tab=readme-ov-file#install-app-on-android)
- [plyer bug - 1](https://github.com/kivy/plyer/issues/505)
- [plyer bug - 2](https://github.com/kivy/plyer/pull/665)
- [plyer Docs](https://plyer.readthedocs.io/en/latest/api.html#plyer.facades.GPS)
- [Android Developers - logcat](https://developer.android.com/tools/logcat)

#### scrcpy
- [Downloads](https://github.com/Genymobile/scrcpy/releases/tag/v3.1)

#### VM
- [Youtube - How to install Ubuntu 24.04 LTS in VirtualBox 2024 - (TopNotch Programmer)](https://www.youtube.com/watch?v=Hva8lsV2nTk)
- [Ubuntu downloads](https://ubuntu.com/download/desktop/thank-you?version=24.04.2&architecture=amd64&lts=true)



## Commands
### POSTGRES BACKUP/RESTORE
- BACKUP
    1. CHECK DATABASES: `>>> docker exec -it <db-container-name> bash -c "psql -U <user> -c '\l'"`
    2. DATABASE BACKUP (.DUMP): `>>> docker exec -it <db-container-name> bash -c 'pg_dump -U <user> -d <database-name> -Fc -f file.dump'`
    3. CHECK OUTPUT FILE: `>>> docker exec -it <db-container-name> bash -c 'ls -lha'`
    4. COPY DUMP FILE FROM CONTAINER: `>>> docker cp <db-container-name>:/file.dump /code/db_dumps/file.dump`
- RESTORE
    1. COPY DUMP FILE TO CONTAINER: `>>> docker cp /code/db_dumps/file.dump <db-container-name>:/file.dump`
    2. STOP BACKEND CONTAINER: `>>> docker stop <web-container-name>`
    3. CHECK DATABASES: `>>> docker exec -it <db-container-name> bash -c "psql -U <user> -c '\l'"`
    4. DROP DATABASE: `>>> docker exec -it <db-container-name> bash -c "psql -U <user> -c 'drop database <database-name>'"`
    5. RECREATE DATABASE: `>>> docker exec -it <db-container-name> bash -c "psql -U <user> -c 'create database <database-name> owner postgres'"`
    6. CHECK DATABASES: `>>> docker exec -it <db-container-name> bash -c "psql -U <user> -c '\l'"`
    7. DATABASE RESTORE (.DUMP): `>>> docker exec -it <db-container-name> bash -c 'pg_restore -U <user> -d <database-name> -v file.dump'`
    8. REMOVE OUTPUT FILE FROM CONTAINER: `>>> docker exec -it <db-container-name> bash -c 'rm file.dump'`
    9. START BACKEND SERVICE: `>>> docker compose up -d <web-service-name>`