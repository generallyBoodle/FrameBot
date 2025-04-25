# Discord Profile Frame Bot 🎨

This bot overlays a transparent profile frame on user avatars, based on their server role!

## ✨ Features
- `!frame` or `!frame @user` – Apply a frame based on role name
- Automatically uses `frames/{role}.png` or falls back to `frames/default.png`

## 🚀 One-Click Deploy (Recommended)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

### ✅ Steps:
1. Click the **Deploy** button
2. Set your `DISCORD_TOKEN` in Railway’s environment variables
3. Once deployed, **invite your bot** using:

```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=277025508352
```

Replace `YOUR_CLIENT_ID` from your [Discord Developer Portal](https://discord.com/developers/applications).

## 🧰 Local Setup (Optional)

1. Clone the repo  
   ```bash
   git clone https://github.com/YOUR_USERNAME/discord-frame-bot.git
   cd discord-frame-bot
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` to `.env`  
   ```bash
   cp .env.example .env
   ```

4. Add your Discord bot token to `.env`

5. Run it!  
   ```bash
   python bot.py
   ```

## 🖼 Adding Frames

Add transparent `.png` files to the `frames/` folder, named after role names:

```
frames/
├── default.png
├── admin.png
└── mod.png
```

When a user uses `!frame`, their highest role name will determine which frame to use.
