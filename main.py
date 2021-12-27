import commandDefinitions
import discord
import os
from dotenv import load_dotenv

load_dotenv("C:/Users/drewh/Documents/aibot/keys.env")
class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = {voice.guild.id: voice for voice in self.voice_clients}
        self.playlists = {}

        self.commands = {
            'ai.ping': self.ping,
            'ai.help': commandDefinitions.help,
            'ai.status': commandDefinitions.status,
            'ai.request': commandDefinitions.request,
            'ai.explaincode:': commandDefinitions.explaincode,
            'ai.writecode:': commandDefinitions.writecode,
            'ai.translatecode:': commandDefinitions.translatecode,
            'ai.ask:': commandDefinitions.ask,
            'ai.paragraph_completion:': commandDefinitions.paragraph_completion,
            'ai.summarize:': commandDefinitions.summarize,
        }

    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.latency * 1000)}ms')
    
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

bot=Client()
bot.run(os.getenv('DISCORD_TOKEN'))