"""Quick script: injects dashboard_data.json into dashboard_template.html → dashboard.html"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
JSON_PATH = ROOT / "data" / "dashboard_data.json"
TEMPLATE_PATH = ROOT / "dashboard_template.html"
OUTPUT_PATH = ROOT / "dashboard.html"

data_json = JSON_PATH.read_text(encoding="utf-8")
template = TEMPLATE_PATH.read_text(encoding="utf-8")
html = template.replace("__DATA_JSON__", data_json)
OUTPUT_PATH.write_text(html, encoding="utf-8")
print(f"✓ Dashboard built: {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size:,} bytes)")
