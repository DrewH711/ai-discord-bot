import openai
from openai import error as aierror

import discord
import os
from dotenv import load_dotenv
from discord_ui import Components, UI, create_choice
import urllib

from pandas import options
import WebServer
load_dotenv("C:/Users/drewh/Documents/aibot/keys.env")

bot = commands.Bot(command_prefix='ai.')
ui=UI(bot)
bot.remove_command('help')
openai.api_key = os.getenv('OPENAI_KEY')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/help'), status=discord.Status.online)

@bot.event
async def on_guild_join(guild):
    embed=discord.Embed(title="Thanks For Adding Me!", description=f"Thanks for adding me to {guild.name}! You can use the `/help` command to get started!", color=0x779ee4)
    await guild.text_channels[0].send(embed=embed)
    
@bot.event
async def on_command_error(ctx, error:commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, that command does not exist")
    if isinstance(error, discord.HTTPException):
        await ctx.send(f"{ctx.author.mention}, something went wrong")
    if isinstance(error,commands.errors.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, you are on cooldown")

@ui.slash.command(name='ping',description='latency test')
async def ping(ctx):
    await ctx.send(f'Pong! Responded in {bot.latency * 1000:.0f}ms')
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Responded in {bot.latency * 1000:.0f}ms')

@ui.slash.command(name='help',description='shows help menu')
async def help(ctx):
    embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
    embed.add_field(name='help', value='Shows this message', inline=False)
    embed.add_field(name='status', value='Shows the status of the bot', inline=False)
    embed.add_field(name='ping', value='Shows the latency of the bot', inline=False)
    embed.add_field(name='request [engine name]', value='Requests a response from the API', inline=False)
    embed.add_field(name='explaincode [language] [code]', value='Explains a code snippet', inline=False)
    embed.add_field(name='writecode [language] [description]', value='Writes a code snippet--works best with python', inline=False)
    embed.add_field(name='translatecode [starting language] [ending language] [code]', value='Translates a code snippet', inline=False)
    embed.add_field(name='ask [question]', value='Ask the bot a question', inline=False)
    embed.add_field(name='paragraph_completion [paragraph]', value='Offers sentence suggestions to continue a paragraph', inline=False)
    embed.add_field(name='summarize [text]', value='Summarizes a text in a way that anyone can understand', inline=False)
    await ctx.send(embed=embed)
@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Help', description='List of commands', color=0x00ff00)
    embed.add_field(name='help', value='Shows this message', inline=False)
    embed.add_field(name='status', value='Shows the status of the bot', inline=False)
    embed.add_field(name='ping', value='Shows the latency of the bot', inline=False)
    embed.add_field(name='request [engine name]', value='Requests a response from the API', inline=False)
    embed.add_field(name='explaincode [language] [code]', value='Explains a code snippet', inline=False)
    embed.add_field(name='writecode [language] [description]', value='Writes a code snippet--works best with python', inline=False)
    embed.add_field(name='translatecode [starting language] [ending language] [code]', value='Translates a code snippet', inline=False)
    embed.add_field(name='ask [question]', value='Ask the bot a question', inline=False)
    embed.add_field(name='paragraph_completion [paragraph]', value='Offers sentence suggestions to continue a paragraph', inline=False)
    embed.add_field(name='summarize [text]', value='Summarizes a text in a way that anyone can understand', inline=False)
    await ctx.send(embed=embed)
    
@ui.slash.command(name='status',description='shows the status of the bot')
async def status(ctx):
    try:
        x = openai.Engine.retrieve("cushman-codex")
        codex_status = x.ready
    except:
        codex_status = False
    try:
        x = openai.Engine.retrieve("babbage-instruct-beta")
        babbage_status = x.ready
    except:
        babbage_status = False
    try:
        x = openai.Engine.retrieve("curie")
        curie_status = x.ready
    except:
        curie_status = False
    try:
        site_code=urllib.request.urlopen("https://bot.themaddoxnetwork.com").getcode()
    except:
        site_code=0
    if codex_status:
        codex_status = ":white_check_mark:"
    else:
        codex_status = ":x:"
    if babbage_status:
        babbage_status = ":white_check_mark:"
    else:
        babbage_status = ":x:"
    if curie_status:
        curie_status = ":white_check_mark:"
    else:
        curie_status = ":x:"
    if site_code==200:
        site_status = ":white_check_mark:"
    else:
        site_status = ":x:"
    embedVar = discord.Embed(title="System Status", description="", color=0x779ee4)
    embedVar.add_field(name="Discord bot", value=":white_check_mark:", inline=False)
    embedVar.add_field(name="Website", value=site_status, inline=False)
    embedVar.add_field(name="Coding AI", value=codex_status, inline=False)
    embedVar.add_field(name="Chatting and Pragraph Analysis AI", value=babbage_status, inline=False)
    await ctx.send(embed=embedVar)

#request command
@ui.slash.command(name='request', description='requests a response from the API')
async def request(ctx, engine: str):

    try:
        x = openai.Engine.retrieve(f"{engine}")
        if(x.ready):
            await ctx.send(f"{x.id} is available")
        else:
            await ctx.send(f"{x.id} is not available")
    except aierror.APIError:
        await ctx.send(f"{engine} is not a valid engine")

#explaincode command
@ui.slash.command(name='explaincode',description='explains a code snippet')
async def explaincode(ctx, language: str, *, code: str):
    code=code.replace('```','')
    code=code.replace('`','')
    response=openai.Completion.create(
    engine="cushman-codex",
    prompt=f"explain the following {language} code: \n{code}",
    max_tokens=500,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["\n\n\n"]
    )
    print(response)
    if(language!="python"):
        response.choices[0].text=response.choices[0].text.replace('#','//')
    await ctx.send(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')
@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def explaincode(ctx, language: str, *, code: str):

    code=code.replace('```','')
    code=code.replace('`','')
    response=openai.Completion.create(
    engine="cushman-codex",
    prompt=f"explain the following {language} code: \n{code}",
    max_tokens=500,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["\n\n\n"]
    )
    print(response)
    if(language!="python"):
        response.choices[0].text=response.choices[0].text.replace('#','//')
    await ctx.send(f'{ctx.author.mention}```{language}\n{response.choices[0].text}```')
@explaincode.error
async def explaincode(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.0f}s.", color=0xff0000)
        await ctx.send(embed=em)

@ui.slash.command(name='writecode',description='writes a code snippet--works best with python')
@commands.cooldown(1, 45, commands.BucketType.user)
async def writecode(ctx, language: str, *, prompt: str):
    try:
        response=openai.Completion.create(
        engine="cushman-codex",
        prompt=f"write the following {language} code: \n{prompt}:\n",
        max_tokens=400,
        temperature=0,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        stop=["\n\n\n", "# ","// why","'''"]
        )
        response=response.choices[0].text
        print(response)
        response=response.replace('       ',' ').replace('!!!','')
        if language=="c#":
            language="csharp"
        if(language=="python"):
            commentchar='#'
        else:
            commentchar='//'
        
        await ctx.send(f"{ctx.author.mention}\n ```{language}\n{commentchar}{prompt} in {language}\n{response}```")
    except discord.errors.NotFound:
        await ctx.send("Sorry, something went wrong. Your request likely timed out")
@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def writecode(ctx, language: str, *, prompt: str):
    response=openai.Completion.create(
    engine="cushman-codex",
    prompt=f"write the following {language} code: \n{prompt}:\n",
    max_tokens=400,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["\n\n\n", "# ","// why","'''"]
    )
    response=response.choices[0].text
    print(response)
    response=response.replace('       ',' ').replace('!!!','')
    if language=="c#":
        language="csharp"
    if(language=="python"):
        commentchar='#'
    else:
        commentchar='//'
    try:
        await ctx.send(f"{ctx.author.mention}\n ```{language}\n{commentchar}{prompt} in {language}\n{response}```")
    except discord.errors.NotFound:
        print("well that's odd") #if anyone knows why this error seems to randomly occur, PLEASE let me know
@writecode.error
async def explaincodeError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
        await ctx.send(embed=em)

@ui.slash.command(name='translatecode',description='translates a code snippet')
@commands.cooldown(1, 45, commands.BucketType.user)
async def translatecode(ctx, language1: str, language2: str, *, code: str):
    code=code.replace('```','')
    code=code.replace('`','')    
    response = openai.Completion.create(
    engine="cushman-codex",
    prompt=f"translate this {language1} code into equivalent {language2}:\n\n{code}\n\n{language2} code goes here:\n",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=['"""','\n\n\n']
    )
    print(response)
    response.choices[0].text=response.choices[0].text.replace('\n\n\n','\n')
    await ctx.send(f'{ctx.author.mention}```{language2}\n{response.choices[0].text}```')
@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def translatecode(ctx, language1: str, language2: str, *, code: str):

    code=code.replace('```','')
    code=code.replace('`','')    
    response = openai.Completion.create(
    engine="cushman-codex",
    prompt=f"translate this {language1} code into equivalent {language2}:\n\n{code}\n\n{language2} code goes here:\n",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=['"""','\n\n\n']
    )
    print(response)
    response.choices[0].text=response.choices[0].text.replace('\n\n\n','\n')
    await ctx.send(f'{ctx.author.mention}```{language2}\n{response.choices[0].text}```')
@translatecode.error
async def translatecodError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
        await ctx.send(embed=em)

@ui.slash.command(name='ask', description='Ask the ai a question. Keep in mind that it has very limited knowledge of current events.')
@commands.cooldown(1, 10, commands.BucketType.user)
async def ask(ctx, *, question: str):
    if len(question)>400:
        await(ctx.reply(f'{ctx.author.mention} Sorry, that question is too long. Please keep your questions under 400 characters.'))
        return
    response = openai.Completion.create(
    engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
    prompt=f"Answer the question as accurately as possible while giving as much information as possible, but make it relatively easy to understand.\n question: {question} \n answer: ",
    max_tokens=80,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["question:"]
    )
    response=response.choices[0].text.replace('\n','')
    await ctx.send(f'{ctx.author.mention}\n Question: {question}\n Answer: **{response}**')
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ask(ctx, *, question: str):

    response = openai.Completion.create(
    engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
    prompt=f"Answer the question as accurately as possible while giving as much information as possible, but make it relatively easy to understand.\n question: {question} \n answer: ",
    max_tokens=80,
    temperature=0,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0,
    stop=["question:"]
    )
    response=response.choices[0].text.replace('\n','')
    await ctx.send(f'{ctx.author.mention}\n Question: {question}\n Answer: **{response}**')
@ask.error
async def askError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
        await ctx.send(embed=em)

@ui.slash.command(name='paragraph_completion', description='Suggests a sentence to continue a given paragraph')
@commands.cooldown(1, 60, commands.BucketType.user)
async def paragraph_completion(ctx, *, paragraph: str):
    with open('prompts/paragraphSuggestionPrompt.txt', 'r') as f:
        examples = f.read()
        f.close()

    response = openai.Completion.create(
    engine="curie",
    prompt=f"{examples} {paragraph}\n output:",
    max_tokens=100,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0.7,
    presence_penalty=2,
    stop=["Input:", '4.']
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}\n Your paragraph:\n{paragraph}\n\n**{response.choices[0].text}**')
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def paragraph_completion(ctx, *, paragraph: str):
    with open('prompts/paragraphSuggestionPrompt.txt', 'r') as f:
        examples = f.read()
        f.close()

    response = openai.Completion.create(
    engine="curie",
    prompt=f"{examples} {paragraph}\n output:",
    max_tokens=100,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0.7,
    presence_penalty=2,
    stop=["Input:", '4.']
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}\n Your paragraph:\n{paragraph}\n\n**{response.choices[0].text}**')
@paragraph_completion.error
async def paragraph_completionError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
        await ctx.send(embed=em)

@ui.slash.command(name='summarize', description='Summarizes a given text')
@commands.cooldown(1, 60, commands.BucketType.user)
async def summarize(ctx, *, text: str):
    with open('prompts/summarizePrompt.txt', 'r') as f:
        examples = f.read()
        f.close()


    response = openai.Completion.create(
    engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
    prompt=f"{examples} {text}\n rephrasing:",
    temperature=0.5,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0,
    stop=["Rephrase this passage in a way that a young child could understand:"]
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}\nYour text:\n{text}\nSummary: **{response.choices[0].text}**')
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def summarize(ctx, *, text: str):
    with open('prompts/summarizePrompt.txt', 'r') as f:
        examples = f.read()
        f.close()


    response = openai.Completion.create(
    engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
    prompt=f"{examples} {text}\n rephrasing:",
    temperature=0.5,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0,
    stop=["Rephrase this passage in a way that a young child could understand:"]
    )
    print(response)
    await ctx.send(f'{ctx.author.mention}\nYour text:\n{text}\nSummary: **{response.choices[0].text}**')
@summarize.error
async def summarizeError(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Cooldown!",description=f"Try again in {error.retry_after:.2f}s.", color=0xff0000)
        await ctx.send(embed=em)

WebServer.start()
bot.run(os.getenv('DISCORD_TOKEN'))