# FlickWiz Telegram Bot Suite

![Welcome to FlickWiz](welcome.jpg)

FlickWiz is a two-part Telegram bot system designed to **auto-filter, manage, and serve movie content** in Telegram channels or groups with **high performance** and **automation**.

---

## Bots Overview

### 1. **FlickWiz** (Movie Search & Filter Bot)

This is the user-facing bot where users can search and get movie links.

**Commands:**

| Command         | Description                                             |
| --------------- | ------------------------------------------------------- |
| `/start`        | Show welcome message and verify user access.           |
| `/help`         | Display how to use the bot.                            |
| `/about`        | Info about the bot.                                    |
| `/verify`       | Re-verify user to access content (for URL shortener).  |
| `/star_user`    | (Admin) Add or check starred users.                    |
| `/stoploop`     | Stop bot running in loop.                         |

**Features:**

- Inline movie search by name.
- Filters movies automatically from database.
- Verifies users every 24 hours.
- Restricts access to only subscribed users.
- Fast, scalable, and user-friendly.

---

### 2. **Admin Bot** (Movie Uploader Bot)

This bot runs in the background, listens to your channel, and stores movie files into MongoDB.

**Command:**

| Command       | Description                                   |
| ------------- | --------------------------------------------- |
| `/refresh`    | Refresh `file_id`s of all movies in database. |

**Features:**

- Automatically saves forwarded videos/documents.
- Parses captions to extract movie name.
- Stores `file_id`, `movie_name`, `message_id`, and `timestamp`.
- Allows manual file ID refresh.

---

## Setup Guide

### Prerequisites

- Python 3.10+
- MongoDB (local or Atlas)
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- python-telegram-bot, pymongo, aiohttp, motor, requests, python-dotenv

---

### Installation

```bash
git clone https://github.com/Aadishranjan/FlickWiz
cd FlickWiz
pip install -r requirements.txt
python bot.py
git clone https://github.com/Aadishranjan/Admin.git
cd Admin
python bot.py
