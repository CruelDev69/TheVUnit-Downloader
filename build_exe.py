import PyInstaller.__main__
import os
import shutil

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
    '--hidden-import=customtkinter',
    '--hidden-import=PIL',
    '--hidden-import=yt_dlp',
    '--optimize=2',
    '--clean',
    '--noconfirm', 
])

print("✅ Build complete! Check 'dist' folder for TheVUnitDownloader.exe")