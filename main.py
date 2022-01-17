from discord import Intents
from discord.ext import commands
from discord_ui import UI
from dotenv import load_dotenv
import os

load_dotenv("C:/Users/drewh/Documents/aibot/keys.env")
intents=Intents.default()
intents.members=True

bot=commands.Bot(command_prefix="ai.", intents=intents)
bot.remove_command("help")
ui=UI(bot)

class Ping(commands.Cog):
    from discord_ui.cogs import slash_command
    def __init__(self, bot):
        
        self.bot=bot
        print("Ping loaded")
    
    @commands.command(name="ping", description="Pong")
    async def ping(self, ctx):
        await ctx.send("Pong! Responded in {}ms".format(bot.latency*1000))
    
    @slash_command(name="ping", description="Pong")
    async def ping_(self, ctx):
        await ctx.send("Pong! Responded in {}ms".format(int(bot.latency*1000)))
    
bot.add_cog(Ping(bot))

import codeSlashCommands
bot.add_cog(codeSlashCommands.codeSlashCommands(bot))

import regularSlashCommands
bot.add_cog(regularSlashCommands.regularSlash(bot))

import codeCommands
bot.add_cog(codeCommands.codeCommands(bot))

import regularCommands
bot.add_cog(regularCommands.regularCommands(bot))

bot.run(os.getenv("DISCORD_TOKEN"))