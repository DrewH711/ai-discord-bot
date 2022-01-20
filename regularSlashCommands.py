import discord
from discord.ext.commands import Bot, Cog
from discord_ui import Slash, SlashPermission, SlashOption, create_choice
from discord_ui.cogs import slash_command, subslash_command, context_cog, listening_component
import openai
from dotenv import load_dotenv
import os
load_dotenv("keys.env")
openai.api_key=os.getenv("OPENAI_KEY")

class regularSlash(Cog):
    def __init__(self, bot: Bot):
        self.bot=bot
        print("Regular slash commands loaded")

    #help command
    @slash_command(name="help", description="Shows a list of commands")
    async def help(self, ctx):
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

    #status command
    @slash_command(name="status", description="Shows the status of different parts of the bot")
    async def status(self, ctx):
        import urllib
        from discord import Embed
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
        embedVar = Embed(title="System Status", description="", color=0x779ee4)
        embedVar.add_field(name="Discord bot", value=":white_check_mark:", inline=False)
        embedVar.add_field(name="Website", value=site_status, inline=False)
        embedVar.add_field(name="Coding AI", value=codex_status, inline=False)
        embedVar.add_field(name="Chatting and Paragraph Analysis AI", value=babbage_status, inline=False)
        await ctx.send(embed=embedVar)

    #request command
    @slash_command(name="request", description="Requests a response from the API", options=[
        SlashOption(str, name="engine", description="Engine to request", choices=[
            create_choice("Davinci","davinci"), create_choice("Curie","curie"), create_choice("Babbage","babbage"), create_choice("Ada","ada"), create_choice("Curie Instruct","curie-instruct-beta-v2"), create_choice("Babbage Instruct","babbage-instruct-beta"), create_choice("Davinci Codex","davincicodex"), create_choice("Cushman Codex","cushman-codex")
            ], required=True)
        ])
    async def request(self, ctx, engine:str="davinci"):
        try:
            x = openai.Engine.retrieve(f"{engine}")
            if(x.ready):
                await ctx.send(f"{x.id} is available")
            else:
                await ctx.send(f"{x.id} is not available")
        except openai.InvalidRequestError:
            await ctx.send(f"{engine} is not a valid engine")
        except openai.APIError:
            await ctx.send("Oops! Something went wrong. Please try again")

    #ask command
    @slash_command(name="ask", description="Ask the bot a question")
    async def ask(self, ctx, *, question: str):
        if len(question)>400:
            await ctx.send(f'{ctx.author.mention} Sorry, that question is too long. Please keep your questions under 400 characters.')
            return
        response = openai.Completion.create(
        engine="babbage-instruct-beta", #curie-instruct-beta-v2 is better if it's not too expensive
        prompt=f"Answer the question as accurately as possible while giving as much information as possible, but make it relatively easy to understand.\n question: {question} \n answer: ",
        max_tokens=80,
        temperature=0,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
        stop=["question:"],
        user=f"{ctx.author.id}"
        )
        response=response.choices[0].text.replace('\n','')
        await ctx.send(f'{ctx.author.mention}\n Question: {question}\n Answer: **{response}**')

    #paragraph completion command
    @slash_command(name="paragraph_completion", description="Offers sentence suggestions to continue a paragraph")
    async def paragraph_completion(self, ctx, *, paragraph: str):
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
        stop=["Input:", '4.'],
        user=f"{ctx.author.id}"
        )
        print(response)
        await ctx.send(f'{ctx.author.mention}\n Your paragraph:\n{paragraph}\n\n**{response.choices[0].text}**')

    #summarize command
    @slash_command(name="summarize", description="Summarizes a text in a way that anyone can understand")
    async def summarize(self, ctx, *, text: str):
        with open('prompts/paragraphSuggestionPrompt.txt', 'r') as f:
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
        stop=["Rephrase this passage in a way that a young child could understand:"],
        user=f"{ctx.author.id}"
        )
        print(response)
        await ctx.send(f'{ctx.author.mention}\nYour text:\n{text}\nSummary: **{response.choices[0].text}**')        