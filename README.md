# DiggerBot

**Welcome!** 🎶

I'm DiggerBot, a music lover always on the lookout for new sounds! I'm a chatbot that you can add to the general channel of a Discord server, ideally with friends who enjoy music and discovering new things!

## How to Use 

- 💻 **Install Discord**: Install the discord app on your phone and create an account. 
- 😼 **Create a Server**: Create a Server and send the invite link to your melomaniac friends!
- 🎷 **Invite me!**: Click on this link to add me to the server: https://discord.com/oauth2/authorize?client_id=1282786955066605680&permissions=8&integration_type=0&scope=bot


## How It Works

- 🪩 **Sessions**: In each session, DiggerBot suggests a musical theme, and group members are free to participate by sharing a Spotify, YouTube, or SoundCloud link.
- ❤️ **Reactions and Votes**: At the end of the session, everyone can react to others' submissions with various types of votes using reactions.
- 🏅 **Points and Rewards**: The most-voted songs earn points to encourage the best music lovers, and a system of streaks and badges rewards the most consistent participants.
- 📊 **Monthly Statistics**: Every month, DiggerBot publishes session statistics, creates a Spotify playlist with the top tracks, and presents the *Digger-of-the-Month* Award.
- ⚙️ **Customization**: Since every group is unique, you can customize DiggerBot's settings to match your preferences. You can change the frequency of sessions by selecting a *schedule* or adjust how often each musical genre is proposed.

## ⚙️ Settings

### 📅 Available Schedules

Here is the list of available schedules for DiggerBot sessions:

- **Everyday** (ID: 1) One full session every day.
- **Weekdays Only** (ID: 2) One full session every day except weekends.
- **1 day on, 1 day off** (ID: 3) One full session every other day.
- **2-days sessions** (ID: 4) One day to participate, one day to vote.
- **Weekly Session** (ID: 5) Theme on Monday and votes on Thursday.

### 🌍 Accessibility 

- 🇫🇷 **Language**: Two languages are currently available: French and English. 
- 🕦 **Timezon**: Change the group timezone depending on your location. The list of available timezones is available here: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568. Examples *Europe/Paris*, *America/New_York*


## 🤖 Command Line

I don't rely on artificial intelligence; I respond to a set of commands that allow you to manage my settings, sessions, and users. Here's the list of available commands to interact with me:

| Code              | Description                                      | Instructions                        |
|-------------------|--------------------------------------------------|-------------------------------------|
| `!help`           | Lists all available commands                     | `!help`                             |
| `!me`             | Adds yourself to the user list                   | `!me <username>`                    |
| `!info`           | Displays group information                       | `!info`                             |
| `!start`          | Restarts the group if it was paused              | `!start`                            |
| `!lang`           | Available languages: French (FR) / English (EN)  | `!lang <FR/EN>`                     |
| `!tz`             | Available timezones: *Europe/Paris*, *America/New_York*, *Asia/Tokyo*, *etc* | `!tz <timezone>`   |
| `!user_create`    | Creates a new user                               | `!create <username> <discord_id>`   |
| `!user_delete`    | Deletes an existing user                         | `!user_delete <username>`           |
| `!user_freeze`    | Freezes a user's streak                          | `!user_freeze <username>`           |
| `!user_unfreeze`  | Unfreezes a user's streak                        | `!user_unfreeze <username>`         |
| `!user_info`      | Displays user information                        | `!user_info <username>`             |
| `!user_list`      | Lists all users                                  | `!user_list`                        |
| `!schedule_set`   | Sets the schedule for the group                  | `!schedule_set <schedule_id>`       |
| `!schedule_list`  | Shows available schedule options                 | `!schedule_list`                    |
| `!settings_show`  | Displays current settings                        | `!settings_show`                    |
| `!settings_incognito` | Toggles incognito mode                         | `!settings_incognito <0/1>`         |
| `!settings_ger`   | Sets the genre exploration ratio                 | `!settings_ger <ratio>`             |
| `!settings_gsr`   | Sets the genre/sub-genre ratio                   | `!settings_gsr <ratio>`             |
| `!settings_gpr`   | Sets the genre proportions                       | `!settings_gpr <genre> <weight>`    |
| `!settings_sgprop`| Displays the genre proportions                   | `!settings_sgprop`                  |

---

**DiggerBot** - Discover new musical gems together!