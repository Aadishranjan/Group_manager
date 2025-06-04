# **Group Manager**

![Bot](./welcome3.webp) <!-- Replace with your actual image URL -->

A powerful Telegram group management bot built using Python and `python-telegram-bot`. Manage your groups with ease using commands like mute, ban, welcome messages, and more.

---

## Features

- **/start** – Start the bot and verify it’s working.
- **/mute @user** – Mute a user from sending messages.
- **/unmute @user** – Unmute a previously muted user.
- **/warn @user** – Issue a warning. After 3 warnings, user gets auto-banned.
- **/ban @user** – Permanently ban a user from the group.
- **/unban user_id** – Unban a previously banned user by their ID.
- **Custom Welcome Messages** – Send a welcome message when a new user joins.
- **Custom Goodbye Messages** – Send a farewell message when a user leaves.
- **/broadcast <message>** – Send a message to all groups where the bot is present.

---

## How to Use

1. Add the bot to your group and promote it as admin.
2. Use any of the commands listed above.
3. Modify the welcome/goodbye messages in the database or through commands (if supported).

---

## Requirements

- Python 3.12+
- `python-telegram-bot`
- `pymongo`
- Other dependencies listed in `requirements.txt`

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## License

This project is licensed under the MIT License.
