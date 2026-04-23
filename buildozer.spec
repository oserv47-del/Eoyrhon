[app]
# App ka naam jo phone me dikhega
title = BGMI Popularity Store
package.name = bgmistore
package.domain = org.store

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# SABSE IMPORTANT: requests (Telegram ke liye) aur pyjnius (UPI ke liye) add kiya gaya hai
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,requests,pyjnius

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# PERMISSIONS: Internet ke bina Telegram message nahi jayega
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
