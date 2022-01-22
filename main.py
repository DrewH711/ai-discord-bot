from discord import Intents
from discord.ext import commands
from discord_ui import UI
from dotenv import load_dotenv
import os

load_dotenv("keys.env")
intents=Intents.default()
intents.members=True

bot=commands.Bot(command_prefix="ai.", intents=intents)
bot.remove_command("help")
ui=UI(bot)

import codeSlashCommands
bot.add_cog(codeSlashCommands.codeSlashCommands(bot))

import regularSlashCommands
bot.add_cog(regularSlashCommands.regularSlash(bot))

import codeCommands
bot.add_cog(codeCommands.codeCommands(bot))

import regularCommands
bot.add_cog(regularCommands.regularCommands(bot))

bot.run(os.getenv("DISCORD_TOKEN"))