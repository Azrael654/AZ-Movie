# 🎬 AZ Movie

A Discord bot to **decide movie nights without the drama**! Create movie lists, pick randomly, and get detailed info - all in one bot.  

## 🌟 Cool Features

- **/add [title]** - Add movies to the list (auto-fixes typos 🦸♂️)

- **/random** - Pick a random movie (no more arguments)

- **/search [title]** - Get detailed movie info + poster 🎞️

- **/list** - See all movies in your list

- **/delete** - Clear the entire list (for the indecisive)

- **Fuzzy Matching** - Auto-detects typos in movie titles

  

## 🛠️ Installation

### Prerequisites

- Python 3.10+

- A [TMDB](https://www.themoviedb.org/) account (for API key)

- A Discord bot (get the token from [Developer Portal](https://discord.com/developers))

  

### Setup

1. Clone this repo:

```bash

git clone https://github.com/Azrael654/AZ-Movie.git

cd movie-pals-bot

```

2. Install dependencies:

```bash

pip install -r requirements.txt

```

3. Put your Token and API key in `.env` file:

```env

DISCORD_TOKEN=your_discord_bot_token

TMDB_API_KEY=your_tmdb_api_key

```

  

4. Run the bot:

```bash

python bot.py

```

  

## 📜 Command List

| Command        | Example        | Description                         |
| -------------- | -------------- | ----------------------------------- |
| `/add [title]` | `/add [title]` | Auto-fixes title + adds to list     |
| `/search`      | `/search dune` | Show poster & movie info            |
| `/random`      | `/random`      | Pick a random movie from the list   |
| `/list`        | `/list`        | Show all movies in the list         |
| `/delete`      | `/delete`      | Clear the entire list (be careful!) |


  

## 🤝 Contributing

Open an issue or pull request if you want to:

- Add a new feature

- Fix typos

- Make embed themes cooler

  

**How to contribute:**

1. Fork this repo

2. Create a new branch (`git checkout -b feature/yourfeature`)

3. Commit your changes (`git commit -m 'feat: add your feature'`)

4. Push to the branch (`git push origin feature/yourfeature`)

5. Open a Pull Request

  

## 📄 License

This project is licensed under [MIT License](LICENSE) - feel free to modify/use it, just don't forget to give credit 😇

  

---

  

**Made with ❤️ by Azrael**

[![GitHub](https://img.shields.io/badge/GitHub-Azrael-blue?logo=github)](https://github.com/Azrael654)
