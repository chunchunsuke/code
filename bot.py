from discord.ext import commands
from discord.utils import get
import discord
import json
import aiohttp
import random
import praw
import os
import youtube_dl
import http.client

players = {}
client = commands.Bot(command_prefix = "~")

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server')

@client.command()
async def mey(ctx):
    await ctx.send('eww,gay!')

@client.command()
async def moshi(ctx):
    await ctx.send('BL lord!')

@client.command()
async def hinata(ctx):
    await ctx.send('BL senin!')

@client.command()
async def gechsim(ctx):
    await ctx.send('eww,gay!')

@client.command()
async def gif(ctx, *, search):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if search == '':
        response = await session.get('https://api.giphy.com/v1/gifs/random?api_key=oI17LcvYpWX5oZGu9cgDs7idJdRUdyaL')
        data = json.loads(await response.text())
        embed.set_image(url=data['data']['images']['original']['url'])
    else:
        search.replace(' ', '+')
        response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=oI17LcvYpWX5oZGu9cgDs7idJdRUdyaL&limit=10')
        data = json.loads(await response.text())
        gif_choice = random.randint(0, 9)
        embed.set_image(url=data['data'][gif_choice]['images']['original']['url'])

    await session.close()

    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_bot(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')

    await ctx.send(f'Joined {channel}')

@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients,guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')
    else:
        print("Bot left")
        await ctx.send(f'Dun think I am in th voice channel')

@client.command(pass_context=True, aliases=['p', 'pl'])
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            print('Removed old song file')
    except PermissionError:
        print('Song is being played')
        await ctx.send('Error: music playing')
        return

    await ctx.send('Getting ready')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quite':True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@client.command(pass_context=True,aliases=['pa'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")

@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


client.run('NzM2MjQ2NjYzMTg1ODI1ODYy.XxsBIw.1Ky8LN7NLzNF9WuKIt2mPEh2MGY')
