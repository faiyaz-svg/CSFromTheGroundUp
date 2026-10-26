"""Retention heat table for the first six signup cohorts (numbers from the lesson's SQL)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
import numpy as np
from _common import OUT_DIR

cohorts = ["Jan 2025 (70)", "Feb 2025 (41)", "Mar 2025 (32)", "Apr 2025 (25)", "May 2025 (31)", "Jun 2025 (19)"]
pct = np.array([
    [76, 60, 23, 9],
    [76, 78, 27, 5],
    [63, 41, 13, 3],
    [76, 60, 20, 12],
    [71, 65, 19, 6],
    [68, 53, 5, 5],
])
fig, ax = plt.subplots(figsize=(6.2, 3.6), facecolor="white")
ax.imshow(pct, cmap="Blues", vmin=0, vmax=100, aspect="auto")
for i in range(pct.shape[0]):
    for j in range(pct.shape[1]):
        ax.text(j, i, f"{pct[i, j]}%", ha="center", va="center", fontsize=10,
                color="white" if pct[i, j] > 55 else "#222222")
ax.set_xticks(range(4), [f"Month {m}" for m in range(4)])
ax.set_yticks(range(len(cohorts)), cohorts)
ax.xaxis.tick_top()
ax.set_ylabel("Signup cohort (users)")
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "cohort-heat-table.svg", format="svg")
