# Chess Club Discord Bot

A Discord bot for a chess community. It can set up the server structure and run chess games directly in text channels.

## Features

- `/setup` creates chess roles, categories, and channels
- `/challenge @player` starts a challenge
- `/accept` accepts a pending challenge
- `/move e2e4` plays a legal move (SAN such as `Nf3` also works)
- `/board`, `/game`, and `/resign` manage the current game
- Only the two players can move, and turns are enforced

## 1. Create the Discord bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create **New Application**, open **Bot**, and select **Add Bot**.
3. Copy the token. Never post or share it.
4. Under **OAuth2 > URL Generator**, select `bot` and `applications.commands`.
5. Give it these permissions: Manage Roles, Manage Channels, Send Messages, Embed Links, Read Message History, and Use Application Commands.
6. Open the generated URL and add the bot to your server.

## 2. Add your private details and run

The software and libraries are already installed in the included `.venv` folder.
Open `.env` in Notepad and paste your token and Server ID after the equals signs. Then double-click `start-bot.bat`.

If moving this project to another computer, install it with Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and paste the bot token and server ID, then run:

```powershell
python bot.py
```

Enable **Developer Mode** in Discord under User Settings > Advanced, then right-click the server and choose **Copy Server ID**.

## 3. Set up the server

As the server owner or an administrator, run `/setup` once. Then use `/challenge @player` in `#find-a-game` or `#chess-games`.

The bot must have a role above the roles it creates. Keep the terminal running while you want the bot online; for 24/7 use, deploy this folder to a Python host.
