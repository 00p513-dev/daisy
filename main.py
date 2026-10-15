import daisySecrets, discord, logging, random
from discord.ext import commands

import thecounter, davwheat, lineageos, tfl, rtt

# Initialize bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def start(ctx):
    """Send a message when the command /start is issued."""
    user = ctx.message.author
    greetings = ["Hello", "Hi", "Konnichiwagwan"]
    await ctx.send(f'{random.choice(greetings)} {user.mention}!')

# Module commands
@bot.command()
async def codename(ctx, *args):
    """Looks up a device by codename from LineageOS"""
    await lineageos.codename_command(ctx, *args)

@bot.command()
async def counter(ctx, *args):
    """Time since *The Counter* was reset"""
    await thecounter.counter_command(ctx, *args)

@bot.command()
async def resetcounter(ctx, *args):
    """Reset *The Counter*"""
    await thecounter.resetcounter_command(ctx, *args)

@bot.command()
async def crs(ctx, *args):
    """Looks up a CRS code for a requested train station"""
    await davwheat.crs_command(ctx, *args)

@bot.command()
async def hentai(ctx):
    """Sends hentai"""
    await ctx.send(f'[Enjoy your hentai](https://forum.djs3rl.com/media/hentai-s3rl-original-video.179/)', suppress_embeds=True)

@bot.command()
async def train(ctx, *args): await rtt.train_command(ctx, *args)

@bot.command()
async def tflstatus(ctx, *args):
    """Returns the status of TfL services"""
    await tfl.tflstatus_command(ctx, logger, *args)

@bot.command()
async def tflbus(ctx, *args):
    """Look up departures from a TfL bus stop with the stop SMS code"""
    await tfl.tflbus_command(ctx, *args)

# Run the bot
bot.run(daisySecrets.discordToken)
