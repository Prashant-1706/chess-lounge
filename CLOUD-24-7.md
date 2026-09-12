# CHESS LOUNGE Bot — Cloud 24/7 Setup

Your bot is ready for cloud hosting on Render as a Python Background Worker.

## What Codex prepared

- `render.yaml` tells Render how to run the bot.
- `requirements.txt` tells Render which Python packages to install.
- `.gitignore` keeps `.env` private, so your Discord token is not uploaded.

## What you do next

### 1. Upload the bot folder to GitHub

Create a GitHub repository and upload the files from this folder:

`C:\Users\Prashant Pal\Documents\Codex\2026-07-03\i\outputs\chess-discord-bot`

Do **not** upload `.env`.

### 2. Create a Render service

1. Go to <https://render.com>
2. Sign in
3. Click **New**
4. Choose **Blueprint** if Render detects `render.yaml`
5. Connect your GitHub repo
6. Deploy it

If you create it manually instead of Blueprint:

- Service type: **Background Worker**
- Language/runtime: **Python**
- Build command: `pip install -r requirements.txt`
- Start command: `python bot.py`

### 3. Add environment variables on Render

In Render, open your bot service, then go to **Environment** and add:

- `DISCORD_TOKEN` = your Discord bot token
- `GUILD_ID` = your Discord server ID

Never post these publicly.

### 4. Deploy

Click **Deploy latest commit** / **Manual Deploy**.

When logs show:

`Ready as CHESS LOUNGE#2341`

your bot is online from the cloud.

### 5. Stop the local bot

After the cloud bot is online, close your local terminal bot window.

Only run one copy of the bot at a time. If cloud and local both run together, Discord commands can act weird.

## Important

Render keeps the bot online while the Render service is running. Render Background Workers are made for always-running bots, but they are paid services. The smallest worker plan is `0.5c-512mb`.
