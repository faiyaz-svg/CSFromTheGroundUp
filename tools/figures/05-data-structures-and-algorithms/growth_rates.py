"""Draw the common growth rates for n from 1 to 20 (Big O and runtime lesson)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[3]
    / "docs/assets/figures/05-data-structures-and-algorithms/growth-rates.svg"
)

OFFSETS = {"log n": 5, "1": -5}

n = np.linspace(1, 20, 400)
curves = [
    ("2^n", 2.0**n, "#b3402a"),
    ("n^2", n**2, "#d98a1f"),
    ("n log n", n * np.log2(n), "#3a7d44"),
    ("n", n, "#2a6fb3"),
    ("log n", np.log2(n), "#6b4aa0"),
    ("1", np.ones_like(n), "#555555"),
]

fig, ax = plt.subplots(figsize=(7, 4.2), facecolor="white")
ax.set_facecolor("white")
for label, y, colour in curves:
    ax.plot(n, y, color=colour, linewidth=2)
    # label each curve where it leaves the plot, or at its right end
    visible = n[y <= 100]
    x_end = visible[-1]
    y_end = y[n == x_end][0] if (n == x_end).any() else y[len(visible) - 1]
    ax.annotate(
        f"O({label})", (x_end, y_end), xytext=(5, OFFSETS.get(label, 0)), textcoords="offset points",
        color=colour, fontsize=10, va="center", fontweight="bold",
    )

ax.set_ylim(0, 100)
ax.set_xlim(1, 22.5)
ax.set_xlabel("input size n")
ax.set_ylabel("steps")
ax.set_title("Steps taken as n grows (constants dropped)", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color="#e5e5e5")
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, format="svg")
print("wrote", OUT)
