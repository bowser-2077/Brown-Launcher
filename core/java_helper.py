import shutil
import subprocess
import os
import requests

def ensure_java8():
    # PATH!
    if shutil.which("java"):
        print("[*] Java is installed, GG!")
        return "java"  # Utilisera celui du système

    print("[!] Java is not installed :( = Downloading")

    # java 8 installer
    url = "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=252042_8a1589aa0fe24566b4337beee47c2d29"
    exe_path = os.path.join(os.getcwd(), "jre-8u451-windows-i586-iftw.exe")

    if not os.path.exists(exe_path):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(exe_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)

    print("[*] Starting JAVA installer...")
    subprocess.Popen(exe_path, shell=True)

    input("Restart the launcher once java is installed!")
    exit()
