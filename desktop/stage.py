# Copies the toolkit's pages into desktop/dist for the app to load. Nothing is changed or built:
# the app shows the same files as the website. Run from the desktop folder (Tauri does this before each build).
import os, shutil
here = os.path.dirname(os.path.abspath(__file__))
repo = os.path.dirname(here)
dist = os.path.join(here, 'dist')
KEEP = ['index.html', 'manifest.webmanifest', 'sw.js', 'tools', 'docs', 'samples', 'templates', 'schemas']
shutil.rmtree(dist, ignore_errors=True)
os.makedirs(dist)
for name in KEEP:
    src = os.path.join(repo, name)
    if os.path.isdir(src):
        shutil.copytree(src, os.path.join(dist, name))
    elif os.path.exists(src):
        shutil.copy2(src, dist)
print('Staged the toolkit in', dist)
