import discord
from discord import app_commands
import random
import requests
import os
import re
from difflib import SequenceMatcher
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class MovieClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.movies = {}
        self.TMDB_API_KEY = os.getenv('TMDB_API_KEY')
        self.TMDB_BASE_URL = "https://api.themoviedb.org/3"

    async def setup_hook(self):
        await self.tree.sync()

client = MovieClient(intents=intents)

def normalize_title(title: str) -> str:
    """Normalize title for flexible comparison"""
    return re.sub(r'\W+', '', title).lower()

def search_tmdb_movie(title: str):
    try:
        response = requests.get(
            f"{client.TMDB_BASE_URL}/search/movie",
            params={
                "api_key": client.TMDB_API_KEY,
                "query": title,
                "language": "en-US",
                "page": 1,
                "include_adult": "false"
            }
        )
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        print(f"TMDB API Error: {str(e)}")
        return None

@client.tree.command(name="add", description="Add a movie title")
async def add_movie(interaction: discord.Interaction, title: str):
    results = search_tmdb_movie(title)
    
    if results is None:
        await interaction.response.send_message("⚠️ Error connecting to database. Please try again later.")
        return
        
    if not results:
        await interaction.response.send_message("❌ Movie not found in database!")
        return
    
    normalized_input = normalize_title(title)
    best_match = None
    
    # Fuzzy matching logic
    for movie in results:
        ratio = SequenceMatcher(
            None, 
            normalized_input, 
            normalize_title(movie["title"])
        ).ratio()
        
        if ratio > 0.7:
            best_match = movie
            break
    
    if not best_match:
        best_match = results[0]
        if SequenceMatcher(None, normalized_input, normalize_title(best_match["title"])).ratio() < 0.4:
            await interaction.response.send_message("❌ No close match found!")
            return
    
    guild_id = interaction.guild.id
    client.movies.setdefault(guild_id, []).append(best_match["title"])
    
    year = best_match.get("release_date", "")[:4]
    year_info = f" ({year})" if year else ""
    
    await interaction.response.send_message(
        f"✅ Added: **{best_match['title']}**{year_info}\n"
        f"(Matched from: '{title}')"
    )

@client.tree.command(name="random", description="Pick random movie")
async def random_movie(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    movies = client.movies.get(guild_id, [])
    
    if not movies:
        await interaction.response.send_message("❌ No movies in the list!")
        return
    
    chosen = random.choice(movies)
    await interaction.response.send_message(f"🎲 Random pick: **{chosen}**")

@client.tree.command(name="list", description="Show all movies")
async def list_movies(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    movies = client.movies.get(guild_id, [])
    
    if not movies:
        await interaction.response.send_message("📜 Movie list is empty!")
        return
    
    movie_list = "\n".join([f"{i+1}. {title}" for i, title in enumerate(movies)])
    await interaction.response.send_message(f"🎬 **Movie List:**\n{movie_list}")

@client.tree.command(name="delete", description="Delete all movies")
async def delete_movies(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    if guild_id in client.movies:
        client.movies[guild_id].clear()
    await interaction.response.send_message("🔥 All movies deleted!")

@client.tree.command(name="search", description="Search movie details")
async def search_movie(interaction: discord.Interaction, title: str):
    results = search_tmdb_movie(title)
    
    if results is None:
        await interaction.response.send_message("⚠️ Error connecting to database. Please try again later.")
        return
        
    if not results:
        await interaction.response.send_message("❌ Movie not found in database!")
        return
    
    movie = results[0]
    
    # Format data
    release_year = movie.get("release_date", "")[:4] if movie.get("release_date") else "N/A"
    overview = movie.get("overview", "No overview available.")[:1000]  # Truncate long overviews
    rating = movie.get("vote_average", "N/A")
    
    # Create embed
    embed = discord.Embed(
        title=movie["title"],
        description=overview,
        color=discord.Color.blue()
    )
    embed.add_field(name="Release Year", value=release_year, inline=True)
    embed.add_field(name="Rating", value=f"{rating}/10 ⭐", inline=True)
    
    if movie.get("poster_path"):
        embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
    
    embed.set_footer(text="Data provided by The Movie Database (TMDB)")
    
    await interaction.response.send_message(embed=embed)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

client.run(os.getenv('DISCORD_TOKEN'))