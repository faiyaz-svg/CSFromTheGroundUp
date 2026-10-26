"""A symmetric and a right-skewed distribution with mean, median and p95 marked."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
import numpy as np
from _common import GREEN, ORANGE, OUT_DIR, RED

rng = np.random.default_rng(1)
heights = rng.normal(170, 8, 5000)
latency = rng.lognormal(mean=np.log(60), sigma=0.7, size=5000)

fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), facecolor="white")
for ax, data, title, bins, unit in [
    (axes[0], heights, "Symmetric: heights (cm)", 40, "cm"),
    (axes[1], latency, "Right-skewed: request latency (ms)", np.arange(0, 420, 10), "ms"),
]:
    ax.hist(data, bins=bins, color="#c9d9ec", edgecolor="white")
    mean, med, p95 = data.mean(), np.median(data), np.percentile(data, 95)
    ax.axvline(mean, color=ORANGE, linewidth=2, label=f"mean {mean:.0f}")
    ax.axvline(med, color=GREEN, linewidth=2, linestyle="--", label=f"median {med:.0f}")
    ax.axvline(p95, color=RED, linewidth=2, linestyle=":", label=f"p95 {p95:.0f}")
    ax.set_title(title, fontsize=11)
    ax.set_yticks([])
    ax.set_xlabel(unit)
    ax.legend(frameon=False, fontsize=9)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    print(title, round(mean, 1), round(med, 1), round(p95, 1))
axes[1].set_xlim(0, 400)
fig.tight_layout()
fig.savefig(OUT_DIR / "distributions.svg", format="svg")
