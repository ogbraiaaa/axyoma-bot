import os
import re
import random
import discord

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Faltou DISCORD_TOKEN")

DICE_RE = re.compile(r"^\s*(\d*)\s*d\s*(\d+)\s*([+-]\s*\d+)?\s*$", re.I)
MULTI_RE = re.compile(r"^\s*(\d+)\s*#\s*(.+?)\s*$", re.I)

MAX_REPEATS = 50
MAX_DICE = 200
MAX_SIDES = 10000

def parse(expr: str):
    m = DICE_RE.match(expr)
    if not m:
        raise ValueError("Expressão inválida. Ex: 2d6+3, d20, 1d200+20, 30#d20")

    n_str, sides_str, mod_str = m.groups()
    n = int(n_str) if n_str else 1
    sides = int(sides_str)
    mod = int(mod_str.replace(" ", "")) if mod_str else 0

    if not (1 <= n <= MAX_DICE):
        raise ValueError(f"Qtd de dados deve ser 1..{MAX_DICE}")
    if not (2 <= sides <= MAX_SIDES):
        raise ValueError(f"Lados deve ser 2..{MAX_SIDES}")

    return n, sides, mod

def format_expr(n: int, sides: int, mod: int):
    base = f"{n}d{sides}"
    if mod > 0:
        return f"{base} + {mod}"
    if mod < 0:
        return f"{base} - {abs(mod)}"
    return base

def do_roll(expr: str):
    n, sides, mod = parse(expr)
    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + mod
    return total, rolls, format_expr(n, sides, mod)

def render_line(total: int, rolls: list[int], expr_fmt: str):
    return f"{total}  ⟵ {rolls} {expr_fmt}"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"ONLINE: {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    content = message.content.strip()

    try:
        mm = MULTI_RE.match(content)
        if mm:
            times = int(mm.group(1))
            expr = mm.group(2)

            if times < 1 or times > MAX_REPEATS:
                raise ValueError(f"Máximo {MAX_REPEATS} repetições")

            lines = []
            for _ in range(times):
                total, rolls, expr_fmt = do_roll(expr)
                lines.append(render_line(total, rolls, expr_fmt))

            out = "\n".join(lines)

            if len(out) > 1800:
                raise ValueError("Resposta ficou grande demais. Use menos repetições.")

            await message.reply(out, mention_author=False)
            return

        if DICE_RE.match(content):
            total, rolls, expr_fmt = do_roll(content)
            await message.reply(render_line(total, rolls, expr_fmt), mention_author=False)
            return

    except Exception as e:
        await message.reply(f"❌ {e}", mention_author=False)

client.run(TOKEN)
