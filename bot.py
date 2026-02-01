import re
import random
import discord

TOKEN = "DISCORD_TOKEN"

DICE_RE = re.compile(r"^\s*(\d*)\s*d\s*(\d+)\s*([+-]\s*\d+)?\s*$", re.I)

def roll(expr: str):
    m = DICE_RE.match(expr)
    if not m:
        raise ValueError("Expressão inválida")

    n_str, sides_str, mod_str = m.groups()
    n = int(n_str) if n_str else 1
    sides = int(sides_str)
    mod = int(mod_str.replace(" ", "")) if mod_str else 0

    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + mod
    return rolls, mod, total

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ONLINE: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    if DICE_RE.match(content):
        try:
            rolls, mod, total = roll(content)
            mod_txt = f" {mod:+d}" if mod else ""
            await message.reply(
                f"**{total}** ← {rolls}{mod_txt} {content}",
                mention_author=False
            )
        except Exception as e:
            await message.reply(f"❌ {e}", mention_author=False)
if not TOKEN:
    raise RuntimeError("Faltou DISCORD_TOKEN")

client.run(TOKEN)
