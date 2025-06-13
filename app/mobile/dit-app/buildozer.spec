[app]
title = DIT APP
package.name = dit_app
package.domain = org.dit_app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = *.py,*.kv,assets/*,images/*.png,fonts/*,data/*
source.exclude_patterns = Dockerfile,.dockerignore,.git/*
version = 0.1
requirements =
    python3,

    # KivyMD's direct dependencies (from uv tree)
    pillow==11.1.0,
    materialyoucolor==2.0.10,
    asynckivy==0.6.4,
    asyncgui==0.6.3,
    
    # Your app's direct dependencies
    https://github.com/kivy/plyer/archive/master.zip
    requests==2.32.3,
    
    # Kivy's dependencies (from uv tree)
    docutils==0.21.2,
    filetype==1.2.0,
    kivy-garden==0.1.5,
    pygments==2.19.1,
    
    # requests' sub-dependencies
    certifi==2025.1.31,
    charset-normalizer==3.4.1,
    idna==3.10,
    urllib3==2.3.0,
    
    # Build system
    setuptools==75.8.0,
    pip==25.0.1,
    cython==0.29.36,
    wheel,

    kivy==2.3.1,
    https://github.com/kivymd/KivyMD/archive/master.zip

orientation = portrait
android.kivy_version = master
author = © Copyright Info akotronis
fullscreen = 0

# android.permissions = android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.WRITE_EXTERNAL_STORAGE
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION

android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.entrypoint = org.kivy.android.PythonActivity
android.enable_androidx = True

# android.archs = x86_64, arm64-v8a
android.archs = arm64-v8a

android.allow_backup = True

# p4a.branch = master
p4a.branch = develop

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1