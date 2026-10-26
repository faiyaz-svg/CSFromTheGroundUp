"""Funnel page_view -> add_to_cart -> purchase on the events sample database."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
from _common import BLUE, OUT_DIR

steps = ["page_view", "add_to_cart", "purchase"]
users = [265, 199, 134]
fig, ax = plt.subplots(figsize=(6.2, 2.8), facecolor="white")
ax.barh(steps[::-1], users[::-1], color=BLUE, height=0.6)
for y, n in enumerate(users[::-1]):
    pct = 100 * n / users[0]
    ax.text(n + 4, y, f"{n} users ({pct:.0f}% of top)", va="center", fontsize=10)
ax.set_xlim(0, 400)
ax.set_xticks([])
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "funnel.svg", format="svg")
