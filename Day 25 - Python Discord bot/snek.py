# bot.py

import asyncio
import os
import random
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

import chan
import hackernews
import insultAPI
import jokeAPI
import magic8ball
import xkcd as xk

random.seed(int(time.time() * 100))

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

ext = "N"
bot = commands.Bot(command_prefix=ext)
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


def chan4(board: str, choice: str, n: int):
    choices = ["lt", "re", "r"]
    print(f"Thread choice commands: {choices=}")

    if choice == choices[0]:
        print(f"> Getting {n} latest threads")
        return chan.get_latest(board, n=n)

    elif choice == choices[1]:
        print(f"> Getting {n} threads with most replies")
        return chan.get_most_popular(board, n=n)

    elif choice == choices[2] and n:
        print(f"> Getting {n} random threads")
        return chan.get_random_threads(board, n=n)

    else:
        print(f"Choose from {choices=}")
        return False


def format_thread_info(i, sub, com, url, replies):
    return f"**{i}) {sub}**\n{com}\n\n{url}\n{replies=}\n"


def short_comsub(com: str, sub: str, message: str, padding: int, total):
    """Short comment, subcategory substitution"""
    next_len = len(message)

    while next_len > padding + 3:
        print(next_len, padding)

        next_len = padding + 3
        com = com[:padding] + "..."

        if len(sub) > 64:
            sub = sub[:64]
        if len(com) > 64:
            com = com[:100] + "..."

    return com, sub


def format_threads(board: str, threads):
    """Format threads for Discord messages, to be multiple messages in case of
    the max characted limit of 2000"""
    print(format_threads.__name__)
    n = len(threads)
    header = f"# {n} threads fetched\n"
    total = 1997 - len(header)
    padding = total // n
    payload = []

    for i, thread in enumerate(threads):
        i += 1
        # time = thread['time']
        # no = thread['no']
        sub = thread["sub"]
        com = thread["com"]
        replies = thread["replies"]
        url = thread["url"]

        message = format_thread_info(i, sub, com, url, replies)
        com, sub = short_comsub(com, sub, message, padding, total)
        message = format_thread_info(i, sub, com, url, replies)
        print(f"{len(message)}")
        # com, sub = short_comsub(com, sub, message, padding, total)
        # message = format_thread_info(i, sub, com, url, replies)

        payload.append(message)

    return header + "".join(payload)


@bot.command(name="ch", help=chan.help_text)
async def chan_threads(ctx, board, choice, n=3):
    """Command for 4chan"""
    print(f"> Getting {n} threads from /{board}/")
    threads = chan4(board, choice, n)
    print("Threads fetched.")
    message = format_threads(board, threads)
    print("Threads formatted.")
    print(f"{message=}")

    msg_len = len(message)
    print(f"{msg_len=}")

    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name="j", help=jokeAPI.help_text)
async def get_joke(ctx):
    """Command for jokeAPI"""
    message = jokeAPI.get_joke()
    print(message)

    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name="i", help=insultAPI.help_text)
async def insult(ctx, user):
    """Command for insult API"""
    message = f"{user}\n{insultAPI.get_insult()}"

    if "gvido" in user.lower() or "590102988757139476" in user:
        message = "Not allowed to insult the master, know your place, trash."

    print(message, user)

    await ctx.message.delete()
    await ctx.send(message)


@bot.command(name="8", help=magic8ball.help_text)
async def ball8(ctx, q):
    """Command for magic 8ball"""
    message = magic8ball.ask_8ball(q)

    print(message)

    await ctx.send(message)


def hn(n: int = 10) -> str:
    """Hacker news function for getting formatted top stories"""
    print(f"Getting top {n} stories")
    newspaper = hackernews.get_top_stories(n=n)
    newspaper = format_news(newspaper, n)
    print("[+] DONE")
    return newspaper


def format_news(newspaper: list[dict], n: int) -> str:
    """Formatter for formatting the request from hacker news API"""
    message = [
        f"{i+1}) {news['title']}\n- {news['url']}\n"
        for i, news in enumerate(newspaper)
    ]
    message = f"**# Top {n} news as of {time.time()}s**\n" + "".join(
        message
    )
    print(f"{message=}")
    return message


@bot.command(name="hn", help="Get x top stories from hackernews.")
async def get_news(ctx, n=10):
    """Command for getting news from Hackernews"""
    print("> Getting news from Hackernews")
    newspaper = hn(n=n)
    print("Newspaper:", newspaper)
    await ctx.message.delete()
    await ctx.send(newspaper)


def xkcd(type_, n=None):
    """Function for getting XKCD comics"""
    base_url = "https://xkcd.com/"
    choices = ["rand", "lt", "n"]

    if type_ == choices[0]:
        print("Getting random XKCD")
        path = xk.get_random_comic()
    elif type_ == choices[1]:
        print("Getting latest XKCD")
        path = xk.get_latest_comic()
    elif type_ == choices[2] and n:
        print(f"Getting XKCD by number {n=}")
        path = xk.get_by_num(n=n)
    else:
        print(f"Choose from {choices=}")
        return False

    return path


@bot.command(
    name="xk", help='Get either "rand"om, "lt"est comic, by "n"umber'
)
async def get_hackernews(ctx, choice, n=None):
    """Command for getting hackernews news"""
    comic = xkcd(choice, n=n)

    await ctx.message.delete()
    print(comic)
    await ctx.send(file=discord.File(comic))


def list_members(guild) -> None:
    """Print out the Discord server members"""
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


def gen_channel_name(ttl: int) -> str:
    """Generate a random channel name"""
    return f"{ttl}-temp-{random.randint(10000, 99999)}"


async def delete_channel(ttl, channel_name, guild):
    await asyncio.sleep(ttl)
    channel = discord.utils.get(guild.channels, name=channel_name)

    await channel.delete()


@bot.command(
    name="create-channel",
    help="Create a random channel for x amount of time."
)
# @commands.has_role('admin')
async def create_channel(
    ctx,
    ttl: int,
    channel_name=None,
    help="Create a random channel for time in seconds"
):
    """Command for creating a random Discord channel with a time limit"""
    guild = ctx.guild
    channel_name = (
        f"{channel_name}-temp-{ttl}"
        if channel_name else gen_channel_name(ttl)
    )
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if not existing_channel:
        message = (
            "<< CHANNEL ALIVE >>\n"
            f"CHANNEL: {channel_name}\n"
            f"TTL:     {ttl}s"
        )

        print(message)

        await guild.create_text_channel(channel_name)
        await ctx.message.delete()
        await ctx.send(message, delete_after=ttl)
        await delete_channel(ttl, channel_name, guild)


def get_all_channels(guild) -> list[str]:
    """Return all of the existing channels from the Discord server"""
    return [
        channel.name for channel in guild.text_channels
        if "-temp-" in channel.name
    ]


@bot.command(name="clean-temp", help="Delete all temp channels.")
async def clean_temp(ctx):
    """Command for deleting all temporary Discord channels"""
    guild = ctx.guild
    text_channel_list = get_all_channels(guild)

    for channel in text_channel_list:
        await delete_channel(0, channel, guild)

    message = f"# Deleted {len(text_channel_list)} channels.\n"
    message += "\n".join(text_channel_list)

    await ctx.message.delete()
    await ctx.send(message, delete_after=5)


@bot.event
async def on_command_error(ctx, error):
    """Error event for commands where the user has no access to"""
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(
            "You do not have the correct role for this command."
        )


@bot.event
async def on_error(event, *args, **kwargs):
    """Event for handling random errors"""
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
        else:
            raise


@bot.event
async def on_message(message):
    """Event for adding a custom emoji whenever anyone sends in a message"""
    await bot.process_commands(message)

    if message.author.id == bot.user.id:
        return

    emoji_id = 636284083294437376
    emoji = bot.get_emoji(emoji_id)

    # if len(message.attachments) > 0:
    # print("Content over 0")

    await message.add_reaction(emoji)

bot.run(TOKEN)

