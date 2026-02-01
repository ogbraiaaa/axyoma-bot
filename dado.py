import random
import re
from dataclasses import dataclass

DICE_RE = re.compile(r"^\s*(\d*)\s*d\s*(\d+)\s*([+-]\s*\d+)?\s*$", re.I)

@dataclass
class RollResult:
    expr: str
    rolls: list[int]
    modifier: int
    total: int

def roll(expr: str, *, max_dice: int = 100, max_sides: int = 1000) -> RollResult:
    m = DICE_RE.match(expr)
    if not m:
        raise ValueError("Expressão inválida. Use: 2d6+3, d20, 4d8-2")

    n_str, sides_str, mod_str = m.groups()
    n = int(n_str) if n_str else 1
    sides = int(sides_str)
    modifier = int(mod_str.replace(" ", "")) if mod_str else 0

    if n < 1 or n > max_dice:
        raise ValueError(f"Número de dados deve ser 1..{max_dice}")
    if sides < 2 or sides > max_sides:
        raise ValueError(f"Lados do dado deve ser 2..{max_sides}")

    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + modifier
    return RollResult(expr=expr.strip(), rolls=rolls, modifier=modifier, total=total)
