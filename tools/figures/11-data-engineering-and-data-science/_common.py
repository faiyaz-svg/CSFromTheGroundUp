"""Shared paths and colours for the data science figures."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

OUT_DIR = Path(__file__).resolve().parents[3] / "docs/assets/figures/11-data-engineering-and-data-science"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#2a6fb3"
ORANGE = "#d98a1f"
GREEN = "#3a7d44"
RED = "#b3402a"
GREY = "#555555"
