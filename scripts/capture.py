import html
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

evidence = Path("evidence")
run = json.loads((evidence / "run.json").read_text(encoding="utf-8"))
with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(f"http://127.0.0.1:5000/#/experiments/{run['experiment_id']}/runs/{run['run_id']}")
    page.get_by_text("iris-random-forest", exact=True).first.wait_for(timeout=60000)
    page.get_by_text("accuracy", exact=True).first.wait_for(timeout=60000)
    page.screenshot(path=evidence / "mlflow-run.png", full_page=True)
    transcript = html.escape((evidence / "hpa.txt").read_text(encoding="utf-8"))
    page.set_content(
        '<body style="background:#101820;color:#eee;padding:24px">'
        '<h2>Kubernetes HPA execution log (kubectl)</h2>'
        f'<pre style="font-size:17px;line-height:1.55">{transcript}</pre></body>'
    )
    page.screenshot(path=evidence / "hpa-scaling.png", full_page=True)
