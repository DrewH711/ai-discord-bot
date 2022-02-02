import discord
from discord.ext.commands import Bot, Cog
from discord_ui import SlashOption, create_choice
from discord_ui.cogs import slash_command
import openai
from dotenv import load_dotenv
import os
import messageClassification
import asyncio

from pandas import options
load_dotenv("keys.env")
openai.api_key=os.getenv("OPENAI_KEY")

class codeSlashCommands(Cog):
    def __init__(self, bot: Bot, cooldown:list):
        self.bot=bot
        self.cooldown=cooldown
        print("Code slash commands loaded")
    
    #writecode command
    @slash_command(name="writecode", description="Writes a code snippet using a prompt", options=[SlashOption(
        str, name="language", description="The language of the code snippet", choices=[
        create_choice("Python", "python"), create_choice("Javascript", "javascript"), create_choice("Java","java"), create_choice("C#","csharp"), create_choice("SQL","sql"), create_choice("Ruby","ruby"), create_choice("Rust","rust"), create_choice("Typescript","typescript"), create_choice("Go","golang"), create_choice("Bash","bash")
        ], required=True
        ), SlashOption(
            str, name="prompt", description="What you want the code to do", required=True
            )
        ])
    async def writecode(self, ctx, language: str, prompt: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(prompt)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(prompt)>400:
            await ctx.send(f'{ctx.author.mention} Sorry, that prompt is too long. Please keep your prompts under 300 characters.')
            return
        try:
            response=openai.Completion.create(
            engine="code-cushman-001",
            prompt=f"write the following {language} code: \n{prompt}:\n",
            max_tokens=400,
            temperature=0,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0,
            stop=["\n\n\n", "# ","// why","'''"],
            user=f"{ctx.author.id}"
            )
            response=response.choices[0].text
            print(response)
            response=response.replace('       ',' ').replace('!!!','')
            if(language=="python" or language=="ruby" or language=="bash"):
                commentchar='#' 
            elif(language=="sql"):
                commentchar='--'
            else:
                commentchar='//'
            
            await ctx.send(f"{ctx.author.mention}\n ```{language}\n{commentchar}{prompt} in {language}\n{response}```")
        except discord.errors.NotFound:
            await ctx.send("Sorry, something went wrong. Your request likely timed out")
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(45);self.cooldown.remove(ctx.author.id)

    #explaincode command
    @slash_command(name="explaincode", description="Explains a code snippet in regular words", options=[SlashOption(str, name="language", description="The language of the code snippet", choices=[create_choice("Python", "python"), create_choice("Javascript", "javascript"), create_choice("Java","java"), create_choice("C#","c#"), create_choice("SQL","sql"), create_choice("Ruby","ruby"),create_choice("Rust","rust"), create_choice("Typescript","typescript"), create_choice("Go","golang"), create_choice("Bash","bash")], required=True), SlashOption(str, name="code", description="The code you want explained", required=True)
    ])
    async def explaincode(self, ctx, language: str, code: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(code)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(code)>700:
            await ctx.send(f'{ctx.author.mention} Sorry, that code is too long. Please keep your code under 700 characters.')
            return
        code=code.replace('```','')
        code=code.replace('`','')
        response=openai.Completion.create(
        engine="code-cushman-001",
        prompt=f"explain the following {language} code: \n{code}",
        max_tokens=500,
        temperature=0,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        stop=["\n\n\n"],
        user=f"{ctx.author.id}"
        )
        print(response)
        if(language!="python"):
            response.choices[0].text=response.choices[0].text.replace('#','//')
        await ctx.send(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(45);self.cooldown.remove(ctx.author.id)

    #translatecode command
    @slash_command(name="translatecode", description="Translates a code snippet to another language", options=[SlashOption(str, name="language1", description="The starting language of your code", choices=[create_choice("Python", "python"), create_choice("Javascript", "javascript"), create_choice("Java","java"), create_choice("C#","c#"), create_choice("SQL","sql"), create_choice("Ruby","ruby"),create_choice("Rust","rust"), create_choice("Typescript","typescript"), create_choice("Go","golang"), create_choice("Bash","bash")], required=True), SlashOption(str, name="language2", description="The language you want your code translated to",choices=[create_choice("Python", "python"), create_choice("Javascript", "javascript"), create_choice("Java","java"), create_choice("C#","c#"), create_choice("SQL","sql"), create_choice("Ruby","ruby"),create_choice("Rust","rust"), create_choice("Typescript","typescript"), create_choice("Go","golang"), create_choice("Bash","bash")],required=True), SlashOption(str, name="code", description="The code you want translated", required=True)])
    async def translatecode(self, ctx, language1: str, language2: str, code: str):
        if self.cooldown.count(ctx.author.id)==0:A='p'
        else:await ctx.send('Please wait. You are on a cooldown.');return
        contentScore = messageClassification.checkMessageContent(code)
        if contentScore=="2":
            await ctx.send("Our content filter has detected that your question may contain offensive content. If you know this is not the case, please try again.")
            return
        if len(code)>700:
            await ctx.send(f'{ctx.author.mention} Sorry, that code is too long. Please keep your code under 700 characters.')
            return
        code=code.replace('```','')
        code=code.replace('`','')    
        response = openai.Completion.create(
        engine="code-cushman-001",
        prompt=f"translate this {language1} code into equivalent {language2}:\n\n{code}\n\n{language2} code goes here:\n",
        temperature=0,
        max_tokens=500,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        stop=['"""','\n\n\n'],
        user=f"{ctx.author.id}"
        )
        print(response)
        response.choices[0].text=response.choices[0].text.replace('\n\n\n','\n')
        await ctx.send(f'{ctx.author.mention}```{language2}\n{response.choices[0].text}```')
        if self.cooldown.count(ctx.author.id)==0:self.cooldown.append(ctx.author.id);await asyncio.sleep(45);self.cooldown.remove(ctx.author.id)