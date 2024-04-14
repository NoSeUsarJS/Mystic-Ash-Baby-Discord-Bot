from discord import Intents, FFmpegPCMAudio, ClientException
from discord.ext import commands
from discord.ext.commands import Context
from os import getenv
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

intents = Intents.default()
intents.voice_states = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='WAOS', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready')

@bot.command()
async def play(ctx: Context, url: str):
    print('play command recognized')
    voice_channel = ctx.author.voice
    if voice_channel is None:
        return await ctx.send('Debes estar en un canal de voz para reproducir música.')
    
    try:
        await voice_channel.channel.connect()
    except ClientException:
        print('Bot was already connected.')
    except Exception as e:
        print(e)

    voice_client = ctx.guild.voice_client

    ytdl_opts = {'format': 'bestaudio/best'}
    try:
        with YoutubeDL(ytdl_opts) as ytdl:
            info = ytdl.extract_info(url, download=False)
            url = info['url']
            voice_client.play(FFmpegPCMAudio(source=url))
            print("Song started...")
            return await ctx.send(f'Reproduciendo "{info["title"]}"')
    except Exception as e:
        print(f'An error has occured!: {e}')

@bot.command()
async def stop(ctx: Context):
    print('stop command recognized')
    voice_channel = ctx.author.voice
    if voice_channel is None:
        return await ctx.send('No puedes detener canciones si no estás en un canal de voz.')
    
    voice_client = ctx.guild.voice_client

    await voice_client.disconnect()
    print('Succesfully disconnected.')
    return await ctx.send('Chaito')

bot.run(TOKEN)