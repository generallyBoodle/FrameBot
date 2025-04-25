#!/usr/bin/env python3

import os
import zipfile
import subprocess
import sys

# Constants
ZIP_FILE = "discord-frame-bot-with-listframes.zip"
EXTRACT_FOLDER = "discord-frame-bot-with-listframes"
ENV_FILE = ".env"

def unzip_bot():
    print(f"📦 Extracting {ZIP_FILE}...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_FOLDER)
    print("✅ Extraction complete.")

def install_requirements():
    req_path = os.path.join(EXTRACT_FOLDER, "requirements.txt")
    print("📥 Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
    print("✅ Packages installed.")

def write_env():
    print("🔐 Please enter your Discord bot token:")
    token = input("> ").strip()
    env_path = os.path.join(EXTRACT_FOLDER, ".env")
    with open(env_path, "w") as f:
        f.write(f"DISCORD_TOKEN={token}\n")
    print(f"✅ Token written to {env_path}")

def done_message():
    print("\n🎉 Setup complete!")
    print(f"To start your bot, run:")
    print(f"cd {EXTRACT_FOLDER}")
    print(f"python bot.py")

if __name__ == "__main__":
    unzip_bot()
    install_requirements()
    write_env()
    done_message()
