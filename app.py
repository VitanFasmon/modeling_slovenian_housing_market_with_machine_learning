from pathlib import Path
import os
from typing import List, Optional

import pandas as pd
from flask import Flask, render_template, send_from_directory, abort


BASE_DIR = Path(__file__).resolve().parent

# Check both top-level and src folders for figures and results
FIGURES_DIR = BASE_DIR / "src" / "figures" if (BASE_DIR / "src" / "figures").exists() else BASE_DIR / "figures"
RESULTS_DIR = BASE_DIR / "src" / "results" if (BASE_DIR / "src" / "results").exists() else BASE_DIR / "results"

app = Flask(__name__)


def safe_read_csv(path: Path, nrows: int = 10) -> Optional[pd.DataFrame]:
    """Read a CSV if it exists and return a short preview."""
    if path.exists():
        try:
            df = pd.read_csv(path)
            return df.head(nrows)
        except Exception:
            return None
    return None


def list_images(folder: Path) -> List[str]:
    """List image file names in a folder."""
    if not folder.exists():
        return []
    images = []
    for f in sorted(folder.glob("*")):
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp"}:
            images.append(f.name)
    return images


@app.route("/")
def index():
    """Main dashboard page with all analysis sections."""
    
    # Section 1: Original data
    original_fig_dir = FIGURES_DIR / "original_data"
    original_images = list_images(original_fig_dir)

    # Section 2: Bootstrap analysis
    bootstrap_fig_dir = FIGURES_DIR / "bootstrap"
    bootstrap_images = list_images(bootstrap_fig_dir)
    bootstrap_table = safe_read_csv(RESULTS_DIR / "bootstrap" / "bootstrap_summary.csv")

    # Section 3: Monte Carlo
    montecarlo_fig_dir = FIGURES_DIR / "montecarlo"
    montecarlo_images = list_images(montecarlo_fig_dir)
    montecarlo_table = safe_read_csv(RESULTS_DIR / "montecarlo" / "montecarlo_summary.csv")

    # Section 4: ML prediction
    ml_fig_dir = FIGURES_DIR / "ml_prediction"
    ml_images = list_images(ml_fig_dir)
    ml_model_table = safe_read_csv(RESULTS_DIR / "ml_prediction" / "ml_model_comparison.csv")
    fi_rf = safe_read_csv(RESULTS_DIR / "ml_prediction" / "feature_importance_rf.csv")
    fi_gb = safe_read_csv(RESULTS_DIR / "ml_prediction" / "feature_importance_gb.csv")
    ml_forecast = safe_read_csv(RESULTS_DIR / "ml_prediction" / "price_forecast.csv", nrows=8)

    context = {
        "original_images": original_images,
        "bootstrap_images": bootstrap_images,
        "bootstrap_table": bootstrap_table,
        "montecarlo_images": montecarlo_images,
        "montecarlo_table": montecarlo_table,
        "ml_images": ml_images,
        "ml_model_table": ml_model_table,
        "fi_rf": fi_rf,
        "fi_gb": fi_gb,
        "ml_forecast": ml_forecast,
    }

    return render_template("index.html", **context)


@app.route("/figures/<section>/<filename>")
def serve_figure(section: str, filename: str):
    """Serve images from figures directory."""
    file_path = FIGURES_DIR / section / filename
    if not file_path.exists():
        abort(404)
    return send_from_directory(str(FIGURES_DIR / section), filename)


@app.route("/results/<section>/<filename>")
def serve_result(section: str, filename: str):
    """Serve CSV files from results directory."""
    file_path = RESULTS_DIR / section / filename
    if not file_path.exists():
        abort(404)
    return send_from_directory(str(RESULTS_DIR / section), filename)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    print(f"\n🚀 Starting Flask server...")
    print(f"📁 Figures directory: {FIGURES_DIR}")
    print(f"📁 Results directory: {RESULTS_DIR}")
    print(f"🌐 Open http://127.0.0.1:5000 in your browser\n")
    app.run(host="0.0.0.0", port=5000, debug=debug)
