"""Confusion matrix for logistic regression on load_breast_cancer (lesson 5 run)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import matplotlib.pyplot as plt
import numpy as np
from _common import OUT_DIR

cm = np.array([[41, 1], [1, 71]])  # rows: actual malignant, benign; columns: predicted
labels = ["malignant", "benign"]
fig, ax = plt.subplots(figsize=(4.6, 3.8), facecolor="white")
ax.imshow(cm, cmap="Blues", vmin=0, vmax=80)
names = [["true positive", "false negative"], ["false positive", "true negative"]]
for i in range(2):
    for j in range(2):
        ax.text(j, i, f"{cm[i, j]}\n{names[i][j]}", ha="center", va="center", fontsize=11,
                color="white" if cm[i, j] > 40 else "#222222")
ax.set_xticks([0, 1], [f"predicted\n{lab}" for lab in labels])
ax.set_yticks([0, 1], [f"actual\n{lab}" for lab in labels])
ax.xaxis.tick_top()
for s in ax.spines.values():
    s.set_visible(False)
fig.tight_layout()
fig.savefig(OUT_DIR / "confusion-matrix.svg", format="svg")
