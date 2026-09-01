"""
test_visual.py — Exercise 05: Visual Testing

See Exercises/05_VisualTesting.md for full instructions.
Run: pytest src/tests/test_visual.py -v --headed

Requires: pip install Pillow
"""
import os
import struct
import zlib
from pathlib import Path
from playwright.sync_api import Page, expect

TASK_MANAGER = "https://testauto.app/task-manager-spa"
BASELINE_DIR = Path("visual_baselines")
BASELINE_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers — implement these (Tasks 2 and 3)
# ---------------------------------------------------------------------------

def compare_screenshots(baseline_path: str, current_path: str) -> float:
    """
    Compare two PNG screenshots pixel by pixel using Pillow.
    Return a float 0.0 (identical) to 1.0 (completely different).
    Save the current screenshot as the baseline if it does not exist yet.
    """
    # TODO Task 2 — implement Pillow pixel comparison
    # 1. from PIL import Image; import numpy as np
    # 2. If baseline does not exist: shutil.copy(current_path, baseline_path); return 0.0
    # 3. img1 = Image.open(baseline_path).convert("RGB")
    # 4. img2 = Image.open(current_path).convert("RGB").resize(img1.size)
    # 5. diff = np.abs(np.array(img1, dtype=int) - np.array(img2, dtype=int))
    # 6. return float(diff.mean() / 255.0)
    raise NotImplementedError("compare_screenshots not implemented — see Task 2")  # wrong


def mask_regions(img_path: str, regions: list[dict]) -> str:
    """
    Draw grey rectangles over dynamic regions in a screenshot before comparison.
    regions: list of {"x": int, "y": int, "width": int, "height": int}
    Returns path to the masked image (overwrites in place or saves as *_masked.png).
    """
    # TODO Task 3 — implement masking with Pillow
    # 1. from PIL import Image, ImageDraw
    # 2. img = Image.open(img_path)
    # 3. draw = ImageDraw.Draw(img)
    # 4. for r in regions: draw.rectangle([r["x"], r["y"], r["x"]+r["width"], r["y"]+r["height"]], fill="grey")
    # 5. masked_path = img_path.replace(".png", "_masked.png"); img.save(masked_path); return masked_path
    raise NotImplementedError("mask_regions not implemented — see Task 3")  # wrong


# ---------------------------------------------------------------------------
# Task 1 — Full-page screenshots and file-size validation
# ---------------------------------------------------------------------------

def test_screenshot_each_view(page: Page, tmp_path):
    """
    Take screenshots of:
    - List view (default URL)
    - Board view (?view=board)
    - Login modal (click the login button to open it)
    Each screenshot must be saved and its file size > 5 KB.
    """
    # TODO:
    # for name, url_or_action in views:
    #     page.screenshot(path=str(tmp_path / f"{name}.png"), full_page=True)
    #     assert os.path.getsize(str(tmp_path / f"{name}.png")) > 5000

    # Developer attempt: one screenshot saved but size never asserted; other views missing
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()
    path = str(tmp_path / "list_view.png")
    page.screenshot(path=path)
    # missing: assert os.path.getsize(path) > 5000
    # missing: board view and login modal screenshots


# ---------------------------------------------------------------------------
# Task 2 — Baseline comparison with compare_screenshots
# ---------------------------------------------------------------------------

def test_compare_list_view_baseline(page: Page, tmp_path):
    """
    Navigate to list view. Take a screenshot.
    Call compare_screenshots(baseline_path, current_path).
    On first run it saves the baseline and returns 0.0.
    On subsequent runs it returns a diff ratio < 0.15.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER); expect(rows.first).to_be_visible()
    # 2. current = str(tmp_path / "list_current.png"); page.screenshot(path=current)
    # 3. baseline = str(BASELINE_DIR / "list_baseline.png")
    # 4. diff = compare_screenshots(baseline, current)
    # 5. assert diff < 0.15, f"Visual regression: diff={diff:.3f}"

    # Developer attempt: calls the unimplemented helper — will raise NotImplementedError
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()
    current = str(tmp_path / "list_current.png")
    page.screenshot(path=current)
    baseline = str(BASELINE_DIR / "list_baseline.png")
    diff = compare_screenshots(baseline, current)   # wrong: raises NotImplementedError
    assert diff < 0.15


# ---------------------------------------------------------------------------
# Task 3 — Screenshot masking for dynamic columns
# ---------------------------------------------------------------------------

def test_masked_comparison(page: Page, tmp_path):
    """
    Navigate to list view. Take screenshot.
    Mask "Due Date" and "Updated At" column areas (inspect coordinates).
    Compare masked version to masked baseline. Assert diff < 0.05.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER); expect(rows.first).to_be_visible()
    # 2. current = take screenshot to tmp_path
    # 3. regions = [{"x": ..., "y": 0, "width": ..., "height": 9999}, ...]  — inspect columns
    # 4. masked = mask_regions(current, regions)
    # 5. baseline = str(BASELINE_DIR / "masked_baseline.png")
    # 6. diff = compare_screenshots(baseline, masked); assert diff < 0.05
    pass


# ---------------------------------------------------------------------------
# Task 4 — Element-scoped screenshot (pagination widget)
# ---------------------------------------------------------------------------

def test_pagination_element_screenshot(page: Page, tmp_path):
    """
    Navigate to list view. Locate the pagination widget using a resilient selector:
    "nav[aria-label*='page'], .pagination, [class*='pagination']"
    Take an element screenshot and assert file size > 1 KB.
    """
    # TODO:
    # 1. page.goto(TASK_MANAGER); expect(rows.first).to_be_visible()
    # 2. pagination = page.locator("nav[aria-label*='page'], .pagination, [class*='pagination']").first
    # 3. expect(pagination).to_be_visible()
    # 4. path = str(tmp_path / "pagination.png"); pagination.screenshot(path=path)
    # 5. assert os.path.getsize(path) > 1000

    # Developer attempt: CSS class selector used — may not match actual DOM class
    page.goto(TASK_MANAGER)
    expect(page.locator("table tbody tr").first).to_be_visible()
    pagination = page.locator(".pagination").first  # wrong: brittle CSS class — may not exist
    path = str(tmp_path / "pagination.png")
    pagination.screenshot(path=path)
    # missing: assert os.path.getsize(path) > 1000


# ---------------------------------------------------------------------------
# Task 5 — Responsive layout diff (desktop vs mobile)
# ---------------------------------------------------------------------------

def test_responsive_layout_diff(browser, tmp_path):
    """
    Capture the list view at desktop (1440x900) and mobile (390x844).
    Assert the pixel diff between them is > 0.05 (layouts are meaningfully different).
    """
    # TODO:
    # 1. desktop_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    # 2. desktop_page = desktop_ctx.new_page(); navigate; screenshot
    # 3. mobile_ctx = browser.new_context(viewport={"width": 390, "height": 844})
    # 4. mobile_page = mobile_ctx.new_page(); navigate; screenshot
    # 5. diff = compare_screenshots(desktop_path, mobile_path); assert diff > 0.05
    # 6. close both contexts
    pass