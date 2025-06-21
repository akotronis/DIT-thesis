# DIT-thesis

This thesis presents the design and implementation of a self-hosted platform for secure geolocation sharing within closed user groups, using open-source tools and virtualized infrastructure.  
The primary objective is to develop a system that enables users to share their real-time location securely with group members, define geofenced zones, and trigger smart IoT actions based on geolocation events.

## Dockerized Services

The system is deployed inside a **Linux** virtual machine launched with **Vagrant** and **VirtualBox** where **Docker Compose** orchestrates the following services:
- A **Django** backend
- A **PostgreSQL/PostGIS** database for data storage,
- A **Streamlit** dashboard for monitoring,
- **Home Assistant** for IoT integration,
- A **WireGuard VPN server** with a management interface.

To ensure secure remote access, the setup employs as reverse proxy tools:
- **Localtonet** 
- **Ngrok**

## Mobile Application
The mobile component is developed using the **Kivy framework** and **KivyMD**.  
Users establish a VPN tunnel using the **WireGuard mobile app** using client configurations generated from the WireGuard UI.  
Once connected, the Kivy-based app communicates with the Django backend over the tunnel, sending location updates to be stored in PostgreSQL.

Through the Streamlit dashboard, users can form **private groups**, **invite others**, and **define geofenced zones**.  

Real-time user location monitoring is achieved through periodic polling of backend endpoints.  
When users enter or exit a defined zone, notification events are triggered and pushed to the frontend, and also forwarded to Home Assistant.  

A **TP-Link Tapo smart plug** is integrated to demonstrate geolocation-triggered automation by toggling its power state upon specific zone transitions.

## System Architecture

<p align="center"><img src="./resources/System-architecture.png" width="500"/></p>


## Demos
### Mobile Application
[](https://github.com/user-attachments/assets/d3c163b6-2e17-4a9b-8a4c-655506bc17ba)
<p align="center"><video width="400" controls><source src="./resources/Mobile-app-demo.mp4" type="video/mp4"></video></p>

### Dashboard Application
[](https://github.com/user-attachments/assets/a29f293c-e4d9-4bd1-b52d-92e0d65d514b)
<p align="center"><video width="800" controls><source src="./resources/Group-management.mp4" type="video/mp4"></video></p>

[](https://github.com/user-attachments/assets/f92cb4f4-ada5-484b-bfdd-e001e1d074b5)
<p align="center"><video width="800" controls><source src="./resources/Group-invitations.mp4" type="video/mp4"></video></p>

[](https://github.com/user-attachments/assets/01e562be-ac97-4bd2-ac1d-222a7ddf21f0)
<p align="center"><video width="800" controls><source src="./resources/Zone-definition" type="video/mp4"></video></p>

[](https://github.com/user-attachments/assets/6e228aae-f9bd-45c7-81d7-4aa5f8c13386)
<p align="center"><video width="800" controls><source src="./resources/Location-monitoring.mp4" type="video/mp4"></video></p>
