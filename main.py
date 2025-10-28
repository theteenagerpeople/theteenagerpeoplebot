import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("MTQyOTUwNjI3NzU5OTQ4MTkzOQ.Gzy0GT.6gZKyZuq8CDkjxgcQV8G_TnOR8XO_T_CG2R3mo")

# Enable all intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot with command tree (for slash commands)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    try:
        synced = await bot.tree.sync()
        print(f"🔧 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

# Load extensions (cogs)
async def load_extensions():
    for ext in ["cogs.general", "cogs.moderation"]:
        try:
            await bot.load_extension(ext)
            print(f"Loaded {ext}")
        except Exception as e:
            print(f"Failed to load {ext}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())
