import daisySecrets, discord, logging, random
from discord.ext import commands

import davwheat, lineageos, rtt, tfl

# Initialize bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='/', intents=intents)

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
    greetings = ["Hewwo", "Haiii", "OwO It's an", "meow meow"]
    await ctx.send(f'{random.choice(greetings)} {user.mention}!')

# Module commands
@bot.command()
async def codename(ctx, *args): await lineageos.codename_command(ctx, *args)

@bot.command()
async def crs(ctx, *args): await davwheat.crs_command(ctx, *args)

@bot.command()
async def train(ctx, *args): await rtt.train_command(ctx, *args)

@bot.command()
async def status(ctx, *args): await tfl.tflstatus_command(ctx, *args)

@bot.command()
async def tflbus(ctx, *args): await tfl.tflbus_command(ctx, *args)

# Run the bot
bot.run(daisySecrets.discordToken)
