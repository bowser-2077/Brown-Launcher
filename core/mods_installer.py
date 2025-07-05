

# UPCOMING UPDATE
# THIS IS NOT WORKING


import os
import requests

MODS = {
    "Sodium": "https://cdn.modrinth.com/data/AANobbMI/versions/mc1.16.5-0.2.0/Sodium-mc1.16.5-0.2.0+build.4.jar",
    "Lithium": "https://cdn.modrinth.com/data/gvQqBUqZ/versions/mc1.16.5-0.6.4/Lithium-mc1.16.5-0.6.4.jar",
    "Phosphor": "https://cdn.modrinth.com/data/mOgUt4GM/versions/mc1.16.5-0.7.0/Phosphor-mc1.16.5-0.7.0.jar"
}

def download_mods(mods_dir):
    os.makedirs(mods_dir, exist_ok=True)
    for name, url in MODS.items():
        path = os.path.join(mods_dir, url.split("/")[-1])
        if not os.path.exists(path):
            print(f"[*] Downloading {name}...")
            with requests.get(url, stream=True) as r:
                with open(path, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
        else:
            print(f"[*] {name} already installed.")
