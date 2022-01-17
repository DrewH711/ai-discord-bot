from discord.ext import commands
import openai

class codeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot=bot
        print("Code commands loaded")
    
    #writecode command
    @commands.command(name="writecode")
    async def explaincode(self, ctx, language: str, *, code: str):
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

    #explaincode command
    @commands.command(name="explaincode")
    async def explaincode(self, ctx, language: str, *, code: str):
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

    #translatecode command
    @commands.command(name="translatecode")
    async def translatecode(self, ctx, language1: str, language2: str, *, code: str):
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


