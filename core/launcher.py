import os
import uuid
import subprocess
import time
import socket
from core.java_helper import ensure_java8
import minecraft_launcher_lib

authlib_jar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "libs", "authlib-injector.jar"))
authlib_url = "https://auth-demo.yushi.moe"


mc_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "minecraft_data"))
authlib_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "server_config", "config.json"))
version_id = "1.16.5"
version_json_path = os.path.join(mc_dir, "versions", version_id, version_id + ".json")

def get_offline_uuid(pseudo):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, pseudo)).replace("-", "")

def get_free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def start_authlib_server(port):
    print(f"[*] Authlib is starting...")
    return subprocess.Popen([
        "java", "-jar", authlib_jar_path,
        f"--config={authlib_config_path}",
        f"--port={port}"
    ])

def start_minecraft(pseudo, ram):
    os.makedirs(mc_dir, exist_ok=True)

    if not os.path.exists(version_json_path):
        print("[*] Installing Minecraft...")
        minecraft_launcher_lib.install.install_minecraft_version(version_id, mc_dir)

    java_path = ensure_java8()

    # port pas utilisé -> serveur demo pour maintenant -> mais il marche alors a voir si on reste dessus
    port = get_free_port()
    authlib_url = f"https://auth-demo.yushi.moe"

    # authlib start
    authlib_proc = start_authlib_server(port)
    time.sleep(3)  # laisser le temps au serveur de démarrer

    try:
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

        print("[*] Starting MC with Authlib Injector")
        process = subprocess.Popen(minecraft_launcher_lib.command.get_minecraft_command(version_id, mc_dir, options))

        process.wait()  # MC crash / quit
        print("[*] MC Closed. If you crashed, try searching for errors in the logs.")

    finally:
        authlib_proc.terminate()
