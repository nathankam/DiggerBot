# DiggerBot

**Welcome!** 🎶

I'm DiggerBot, a music lover always on the lookout for new sounds! I'm a chatbot that you can add to the general channel of a Discord server, ideally with friends who enjoy music and discovering new things!

## How It Works

- 🪩 **Sessions**: In each session, DiggerBot suggests a musical theme, and group members are free to participate by sharing a Spotify, YouTube, or SoundCloud link.
- ❤️ **Reactions and Votes**: At the end of the session, everyone can react to others' submissions with various types of votes using reactions.
- 🏅 **Points and Rewards**: The most-voted songs earn points to encourage the best music lovers, and a system of streaks and badges rewards the most consistent participants.
- 📊 **Monthly Statistics**: Every month, DiggerBot publishes session statistics, creates a Spotify playlist with the top tracks, and presents the *Digger-of-the-Month* Award.
- ⚙️ **Customization**: Since every group is unique, you can customize DiggerBot's settings to match your preferences. You can change the frequency of sessions by selecting a *schedule* or adjust how often each musical genre is proposed.

## Command Line / Interacting with the Bot

I don't rely on artificial intelligence; I respond to a set of commands that allow you to manage my settings, sessions, and users.

Here's the list of available commands to interact with DiggerBot:

| Command              | Code              | Description                                      | Instructions                        |
|----------------------|-------------------|--------------------------------------------------|-------------------------------------|
| **HELP**             | `!help`           | Lists all available commands                     | `!help`                             |
| **ME**               | `!me`             | Adds yourself to the user list                   | `!me <username>`                    |
| **GET INFO**         | `!info`           | Displays group information                       | `!info`                             |
| **START**            | `!start`          | Restarts the group if it was paused              | `!start`                            |
| **ADD USER**         | `!user_create`    | Creates a new user                               | `!create <username> <discord_id>`   |
| **REMOVE USER**      | `!user_delete`    | Deletes an existing user                         | `!user_delete <username>`           |
| **FREEZE USER**      | `!user_freeze`    | Freezes a user's streak                          | `!user_freeze <username>`           |
| **UNFREEZE USER**    | `!user_unfreeze`  | Unfreezes a user's streak                        | `!user_unfreeze <username>`         |
| **USER INFO**        | `!user_info`      | Displays user information                        | `!user_info <username>`             |
| **LIST USERS**       | `!user_list`      | Lists all users                                  | `!user_list`                        |
| **SET SCHEDULE**     | `!schedule_set`   | Sets the schedule for the group                  | `!schedule_set <schedule_id>`       |
| **LIST SCHEDULES**   | `!schedule_list`  | Shows available schedule options                 | `!schedule_list`                    |
| **SETTINGS**         | `!settings_show`  | Displays current settings                        | `!settings_show`                    |
| **SETTINGS INC**     | `!settings_incognito` | Toggles incognito mode                         | `!settings_incognito <0/1>`         |
| **SETTINGS GER**     | `!settings_ger`   | Sets the genre exploration ratio                 | `!settings_ger <ratio>`             |
| **SETTINGS GSR**     | `!settings_gsr`   | Sets the genre/sub-genre ratio                   | `!settings_gsr <ratio>`             |
| **SETTINGS GPR**     | `!settings_gpr`   | Sets the genre proportions                       | `!settings_gpr <genre> <weight>`    |
| **SETTINGS GPR SHOW**| `!settings_sgprop`| Displays the genre proportions                   | `!settings_sgprop`                  |

---

**DiggerBot** - Discover new musical gems together!