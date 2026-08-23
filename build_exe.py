import PyInstaller.__main__
import os
import shutil
import customtkinter

# Find customtkinter directory to include its JSON themes and assets automatically
ctk_path = os.path.dirname(customtkinter.__file__)

if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

print("🔨 Building TheVUnit Downloader EXE...")

PyInstaller.__main__.run([
    'main.py',
    '--name=TheVUnitDownloader',
    '--onefile',
    '--windowed',
    '--icon=assets/thevunit_logo.ico',
    '--add-data=assets;assets',
    f'--add-data={ctk_path};customtkinter',
    '--collect-all=customtkinter',
    '--collect-all=yt_dlp',
    '--collect-submodules=core',
    '--collect-submodules=gui',
    '--collect-submodules=utils',
    '--optimize=2',
    '--clean',
    '--noconfirm', 
])

print("✅ Build complete! Check 'dist' folder for TheVUnitDownloader.exe")