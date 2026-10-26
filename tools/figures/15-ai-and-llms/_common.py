"""Shared paths and colours for the AI and LLM figures."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

OUT_DIR = Path(__file__).resolve().parents[3] / "docs/assets/figures/15-ai-and-llms"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#2a6fb3"
GREY = "#555555"
