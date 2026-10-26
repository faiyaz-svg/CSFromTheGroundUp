"""A fitted line through noisy house-price data (matches the lesson's code)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
import numpy as np
from _common import BLUE, ORANGE, OUT_DIR, RED

rng = np.random.default_rng(0)
size = rng.uniform(40, 160, 50)
price = 3000 * size + 50_000 + rng.normal(0, 20_000, 50)
slope, intercept = np.polyfit(size, price, 1)
print(round(slope), round(intercept))

fig, ax = plt.subplots(figsize=(6.2, 3.6), facecolor="white")
ax.scatter(size, price / 1000, color=BLUE, s=22, label="houses")
xs = np.array([40, 160])
ax.plot(xs, (slope * xs + intercept) / 1000, color=ORANGE, linewidth=2.5, label=f"fitted line, slope {slope:,.0f} per m$^2$")
i = 10
ax.plot([size[i]] * 2, [price[i] / 1000, (slope * size[i] + intercept) / 1000], color=RED, linewidth=2)
ax.annotate("residual", (size[i] + 2, (price[i] + slope * size[i] + intercept) / 2000), color=RED, fontsize=10)
ax.set_xlabel("Size (m$^2$)")
ax.set_ylabel("Price (thousands of dollars)")
ax.legend(frameon=False, loc="upper left")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "regression-line.svg", format="svg")
