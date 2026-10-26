"""Train and test error against model flexibility (polynomial degree)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
import numpy as np
from _common import BLUE, GREY, ORANGE, OUT_DIR

rng = np.random.default_rng(4)


def sample(n):
    x = np.sort(rng.uniform(0, 1, n))
    return x, np.sin(2 * np.pi * x) + rng.normal(0, 0.3, n)


x_tr, y_tr = sample(30)
x_te, y_te = sample(200)
degrees = list(range(1, 11))
tr, te = [], []
for d in degrees:
    c = np.polynomial.Polynomial.fit(x_tr, y_tr, d)
    tr.append(np.sqrt(np.mean((c(x_tr) - y_tr) ** 2)))
    te.append(np.sqrt(np.mean((c(x_te) - y_te) ** 2)))
best = degrees[int(np.argmin(te))]
print("best degree", best)
print("train", [round(v, 2) for v in tr])
print("test ", [round(v, 2) for v in te])

fig, ax = plt.subplots(figsize=(6.2, 3.6), facecolor="white")
ax.plot(degrees, tr, color=BLUE, linewidth=2, marker="o", label="train error")
ax.plot(degrees, te, color=ORANGE, linewidth=2, marker="o", label="test error")
ax.axvline(best, color=GREY, linestyle=":")
ax.annotate("underfitting", (1.2, 0.75), fontsize=10, color=GREY)
ax.annotate("overfitting", (8, 0.75), fontsize=10, color=GREY)
ax.set_xlabel("Model flexibility (polynomial degree)")
ax.set_ylabel("Error (RMSE)")
ax.set_ylim(0, 0.9)
ax.legend(frameon=False, loc="upper center")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "overfitting.svg", format="svg")
