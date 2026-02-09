import os
import uuid
import subprocess
import time
import minecraft_launcher_lib
import minecraft_launcher_lib.fabric as fabric_lib
from core.java_helper import ensure_java8
from minecraft_launcher_lib.utils import get_available_versions

# config
mc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "minecraft_data"))
authlib_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libs", "authlib-injector.jar"))
authlib_url = "https://auth-demo.yushi.moe"  # Authlib demo server

# utils
def get_offline_uuid(pseudo):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, pseudo)).replace("-", "")

def list_installed_profiles():
    versions_dir = os.path.join(mc_dir, "versions")
    if not os.path.exists(versions_dir):
        return []
    return [v for v in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, v))]

def is_stable_release(version_id):
    
    return version_id.count('.') == 2 and version_id.replace(".", "").isdigit()

def get_all_profiles():
    versions_dir = os.path.join(mc_dir, "versions")
    installed_versions = os.listdir(versions_dir) if os.path.exists(versions_dir) else []

    try:
        official_versions = get_available_versions(mc_dir)
        fabric_loader = fabric_lib.get_latest_loader_version()
    except Exception as e:
        print(f"[!] Erreur récupération des versions : {e}")
        return installed_versions

    profiles = []

    for version in official_versions:
        name = version["id"]

        if not is_stable_release(name):
            continue

        # vanilla
        profiles.append(name if name in installed_versions else f"{name} ⏬")

        # fabric
        fabric_profile = f"fabric-loader-{fabric_loader}-{name}"
        profiles.append(fabric_profile if fabric_profile in installed_versions else f"{fabric_profile} ⏬")

    return profiles


# install a version
def install_version(profile: str):
    
    version_dir = os.path.join(mc_dir, "versions", profile)
    version_json = os.path.join(version_dir, f"{profile}.json")

    
    profile = profile.replace(" ⏬", "").strip()

    if os.path.exists(version_json):
        print(f"[*] Version already installed : {profile}")
        return

    print(f"[*] Installing version : {profile}")

    try:
        # Détection Fabric
        if "fabric" in profile or "fabric-loader" in profile:
            print("[*] Installing fabric...")

            if profile.startswith("fabric-loader"):
                # Exemple : fabric-loader-0.16.14-1.16.5
                try:
                    parts = profile.split("-")
                    loader_version = parts[2]
                    base_version = parts[3]
                except:
                    raise Exception("Fabric error")

                fabric_lib.install_fabric(
                    minecraft_version=base_version,
                    loader_version=loader_version,
                    minecraft_directory=mc_dir
                )
            else:
                # simple fab version detection
                base_version = profile.replace("fabric-", "")
                fabric_lib.install_fabric(
                    minecraft_version=base_version,
                    minecraft_directory=mc_dir
                )

        else:
            # vanilla method
            print(f"[*] Installing mc vanilla {profile}...")
            minecraft_launcher_lib.install.install_minecraft_version(profile, mc_dir)

        print(f"[*] Version {profile} installed")

    except Exception as e:
        print(f"[!] Failed to install {profile} : {e}")

# === LANCEMENT DE MINECRAFT ===
def start_minecraft(pseudo, ram, profile="1.20.4"):
    os.makedirs(mc_dir, exist_ok=True)
    print(f"[*] Attempting to launch {profile}")

    # Nettoyage du nom si nécessaire
    profile = profile.replace(" ⏬", "").strip()

    version_dir = os.path.join(mc_dir, "versions", profile)
    version_json = os.path.join(version_dir, f"{profile}.json")

    # === Installation si nécessaire ===
    if not os.path.exists(version_json):
        try:
            if profile.startswith("fabric-") or "-fabric" in profile or "fabric-loader" in profile:
                print(f"[*] Fabric not found, installing...")

                # Déduire version de base depuis profile : ex. "fabric-loader-0.16.14-1.16.5"
                try:
                    base_version = profile.split("-")[-1]  # récupère "1.16.5"
                except:
                    base_version = "1.16.5"  # fallback

                # Liste des loaders
                all_loaders = fabric_lib.get_all_loader_versions()
                loader = next((l["loader"]["version"] for l in all_loaders if l["stable"] is True), None)

                if not loader:
                    print("[!] No stable Fabric loader found.")
                    return

                print(f"[*] Installing Fabric {loader} for {base_version}...")
                fabric_lib.install_fabric(
                    minecraft_version=base_version,
                    loader_version=loader,
                    minecraft_directory=mc_dir
                )
            else:
                print(f"[*] Installing vanilla Minecraft {profile}...")
                minecraft_launcher_lib.install.install_minecraft_version(profile, mc_dir)
        except Exception as e:
            print(f"[!] Failed to install {profile} : {e}")
            return

    # === Java détecté ===
    java_path = ensure_java8()

    # === Options de lancement ===
    options = {
        "username": pseudo,
        "uuid": get_offline_uuid(pseudo),
        "token": "fake-token",
        "executablePath": java_path,
        "jvmArguments": [
            f"-Xmx{ram}",
            f"-javaagent:{authlib_jar_path}={authlib_url}"
        ],
        "gameDirectory": mc_dir,
        "launcherName": "BrownLauncher",
        "launcherVersion": "1.0"
    }

    print(f"[*] Launching Minecraft ({profile})...")
    try:
        command = minecraft_launcher_lib.command.get_minecraft_command(profile, mc_dir, options)
        subprocess.Popen(command).wait()
        print("[*] Minecraft closed.")
    except Exception as e:
        print(f"[!] Error during Minecraft launch : {e}")
