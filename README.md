# 🎮 Campus Chaos

**The Discord bot your college server definitely didn't need.**

Campus Chaos is a fun, Python-powered Discord bot featuring memes, interactive quizzes, college attendance tracking, a bunk calculator, mini-games, XP, achievements, leaderboards, and music playback.

Built for entertainment, friendly competition, and questionable college decisions. 😈

---

## ✨ Features

### 😂 Memes
- Get random memes using `/meme`.
- Enjoy a quick break from college assignments.

### 🧠 Interactive Quizzes
- Multiple-choice questions with Discord buttons.
- Computer Science, General Knowledge, and Chaos Mode.
- Timed questions with instant feedback.
- Earn 25 XP for a correct answer.

### 📚 Attendance Tracker
- Add subjects and record attendance.
- Mark attended or missed classes.
- View attendance percentages.
- Track minimum attendance requirements.

### 😈 Bunk Calculator
- Calculate how many future classes you can miss while maintaining your attendance threshold.
- Receive funny attendance status messages.
- Make informed decisions using your recorded attendance data.

### 🎲 Fun Commands
- Coin flipping
- Dice rolling
- Magic 8-Ball
- Friendly roasts
- Pickup-line generator
- Random decision maker

### 🏆 XP, Levels & Achievements
- Earn XP through supported commands.
- Level up automatically.
- Compare scores on the leaderboard.
- Unlock achievements for reaching milestones.

### 🎵 Music System
- Join Discord voice channels.
- Play supported audio sources.
- Pause, resume, skip, and stop playback.
- Manage a music queue.

Music playback depends on source availability, permissions, and supported media formats.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| discord.py | Discord bot framework |
| SQLite | Persistent user and attendance data |
| yt-dlp | Supported media extraction |
| FFmpeg | Audio processing |
| PyNaCl | Discord voice support |
| python-dotenv | Environment variable management |

---

## 📂 Project Structure

```text
campus-chaos-discord-bot/
├── bot.py
├── cogs/
│   ├── memes.py
│   ├── quiz.py
│   ├── attendance.py
│   ├── fun.py
│   ├── levels.py
│   └── music.py
├── database/
│   └── db.py
├── utils/
│   ├── quiz_questions.py
│   └── xp.py
├── assets/
│   └── screenshots/
├── .env.example
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or newer
- Git
- FFmpeg for music playback
- A Discord application and bot token

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/campus-chaos-discord-bot.git
cd campus-chaos-discord-bot
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Install FFmpeg

On macOS:

```bash
brew install ffmpeg
```

On other operating systems, install FFmpeg using the appropriate package manager or official distribution.

### 5. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your private bot token:

```dotenv
DISCORD_TOKEN=your_actual_token_here
```

Never share or commit this token.

### 6. Start Campus Chaos

```bash
python3 bot.py
```

The bot should connect to Discord and synchronize its slash commands.

---

## 🎮 Available Commands

| Category | Command | Description |
|---|---|---|
| General | `/ping` | Check bot latency |
| General | `/about` | Learn about Campus Chaos |
| General | `/help` | Display the help menu |
| Memes | `/meme` | Get a random meme |
| Quiz | `/quiz` | Start a trivia question |
| Attendance | `/subject` | Add a subject |
| Attendance | `/attendance` | View attendance |
| Attendance | `/attend` | Record an attended class |
| Attendance | `/bunk` | Record a missed class |
| Attendance | `/canibunk` | Calculate safe bunks |
| Fun | `/coinflip` | Flip a coin |
| Fun | `/roll` | Roll a dice |
| Fun | `/8ball` | Ask the Magic 8-Ball |
| Fun | `/roast` | Playfully roast a member |
| Fun | `/rizz` | Generate a pickup line |
| Fun | `/choose` | Choose between options |
| Levels | `/profile` | View XP and level |
| Levels | `/leaderboard` | View XP rankings |
| Levels | `/achievements` | View achievements |
| Music | `/join` | Join a voice channel |
| Music | `/play` | Play supported audio |
| Music | `/pause` | Pause playback |
| Music | `/resume` | Resume playback |
| Music | `/skip` | Skip a song |
| Music | `/queue` | View upcoming songs |
| Music | `/nowplaying` | Show current song |
| Music | `/stop` | Stop and disconnect |

---

## 📸 Screenshots

Add screenshots from your running Discord server here.

Suggested screenshots:

- `assets/screenshots/help.png`
- `assets/screenshots/quiz.png`
- `assets/screenshots/attendance.png`
- `assets/screenshots/bunk-calculator.png`
- `assets/screenshots/profile.png`
- `assets/screenshots/music.png`

For example:

```markdown
![Campus Chaos Help Menu](assets/screenshots/help.png)
```

Only add screenshot links after the corresponding images exist.

---

## 🗺️ Future Ideas

- [ ] AI-powered chatbot
- [ ] Multiplayer quiz battles
- [ ] Server-specific leaderboards
- [ ] Advanced attendance analytics
- [ ] Custom profile cards
- [ ] Weekly challenges
- [ ] Automated attendance reminders
- [ ] Music playback improvements
- [ ] Web dashboard

---

## 🔒 Security

- Never expose the Discord bot token.
- Store secrets in environment variables.
- Keep the SQLite database private.
- Validate command inputs.
- Only play audio from permitted sources.
- Avoid giving the bot unnecessary Discord permissions.

## 📜 License

This project is intended to be released under the MIT License. See `LICENSE` once added.

---

**Made with Python, Discord, and an unreasonable amount of chaos.** 🎮