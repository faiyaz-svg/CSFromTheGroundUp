"""Next-token probabilities at three temperatures (lesson 4 of how-llms-work)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
from _common import BLUE, GREY, OUT_DIR

tokens = ["Paris", "Lyon", "France", "banana"]
logits = [4.0, 2.5, 2.0, -1.0]


def softmax(xs, t):
    scaled = [x / t for x in xs]
    m = max(scaled)
    exps = [math.exp(x - m) for x in scaled]
    s = sum(exps)
    return [e / s for e in exps]


fig, axes = plt.subplots(1, 3, figsize=(9, 3.2), sharey=True, facecolor="white")
for ax, t in zip(axes, (0.2, 1.0, 2.0)):
    probs = softmax(logits, t)
    bars = ax.bar(tokens, probs, color=BLUE)
    for bar, p in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width() / 2, p + 0.02, f"{p:.2f}", ha="center", fontsize=9, color=GREY)
    ax.set_title(f"temperature {t}", fontsize=11)
    ax.set_ylim(0, 1.12)
    ax.tick_params(axis="x", labelsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel("probability of next token")
fig.suptitle('Next token after "The capital of France is"', fontsize=11, color=GREY)
fig.tight_layout()
fig.savefig(OUT_DIR / "sampling-temperature.svg", format="svg")
