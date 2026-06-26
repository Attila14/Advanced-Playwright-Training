"""
test_visual.py — Exercise 05: Visual Testing

Uses page.screenshot() + Pillow pixel comparison.
No Node.js plugins required.

See Exercises/05_VisualTesting.md for full instructions.
Run: pytest src/tests/test_visual.py -v
"""

import io
import os
import pytest
from PIL import Image, ImageChops, ImageDraw
from playwright.sync_api import Page, Browser

SPA_URL = "https://testauto.app/task-manager-spa"
os.makedirs("screenshots/baselines", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers — implement these as part of the exercise
# ---------------------------------------------------------------------------

def compare_screenshots(current_bytes: bytes, baseline_path: str, tolerance: float = 0.01) -> float:
    """
    Compare current screenshot against a saved baseline.
    Returns ratio of differing pixels (0.0 = identical).
    On first call (no baseline file): saves the baseline and returns 0.0.

    TODO: implement this helper for Task 2.
    Hint:
        current = Image.open(io.BytesIO(current_bytes)).convert("RGB")
        if not os.path.exists(baseline_path): save and return 0.0
        diff = ImageChops.difference(current, baseline)
        changed = sum(1 for p in diff.convert("L").getdata() if p > 10)
        return changed / total_pixels
    """
    raise NotImplementedError


def mask_regions(screenshot_bytes: bytes, regions: list) -> bytes:
    """
    Fill the given bounding-box regions with magenta before comparison.
    regions: list of dicts with keys x, y, width, height (from locator.bounding_box())

    TODO: implement this helper for Task 3.
    Hint:
        img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
        draw = ImageDraw.Draw(img)
        for r in regions: draw.rectangle([r["x"], r["y"], r["x"]+r["width"], r["y"]+r["height"]], fill=(255,0,255))
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Task 1 — Save full-page screenshots of key states
# ---------------------------------------------------------------------------

def test_save_list_view_screenshot(page: Page):
    """Navigate to SPA list view and save a full-page screenshot."""
    # TODO:
    # 1. page.goto(SPA_URL) and wait_for_load_state("networkidle")
    # 2. img_bytes = page.screenshot(full_page=True)
    # 3. open("screenshots/list-view.png", "wb").write(img_bytes)
    # 4. assert os.path.exists("screenshots/list-view.png")
    # 5. assert os.path.getsize("screenshots/list-view.png") > 5000
    pass


def test_save_board_view_screenshot(page: Page):
    """Navigate to board view and save a full-page screenshot."""
    # TODO: goto SPA_URL + "?view=board", screenshot -> screenshots/board-view.png
    pass


def test_save_login_modal_screenshot(page: Page):
    """Open the Login modal and capture it."""
    # TODO:
    # 1. goto SPA_URL
    # 2. Click the Login button to open the login modal
    # 3. Wait for the modal to be visible
    # 4. screenshot -> screenshots/login-modal.png
    pass


# ---------------------------------------------------------------------------
# Task 2 — Baseline comparison
# ---------------------------------------------------------------------------

def test_baseline_comparison(page: Page):
    """
    First run: saves the baseline.
    Subsequent runs: compares against it — ratio must be < 0.15.
    """
    # TODO:
    # 1. goto SPA_URL, wait_for_load_state("networkidle")
    # 2. current_bytes = page.screenshot(full_page=True)
    # 3. ratio = compare_screenshots(current_bytes, "screenshots/baselines/list-view-baseline.png")
    # 4. assert ratio < 0.15, f"Visual diff too large: {ratio:.2%}"
    pass


# ---------------------------------------------------------------------------
# Task 3 — Mask dynamic columns before comparison
# ---------------------------------------------------------------------------

def test_masked_baseline_comparison(page: Page):
    """
    Capture screenshot, mask the Due Date and Updated At columns,
    then compare against a masked baseline. Ratio must be < 0.05.
    """
    # TODO:
    # 1. goto SPA_URL, wait_for_load_state("networkidle")
    # 2. current_bytes = page.screenshot(full_page=True)
    # 3. Get bounding_box() for Due Date column: page.locator("table tbody td:nth-child(5)").first.bounding_box()
    # 4. Get bounding_box() for Updated column: page.locator("table tbody td:nth-child(6)").first.bounding_box()
    # 5. masked_bytes = mask_regions(current_bytes, [box1, box2])
    # 6. ratio = compare_screenshots(masked_bytes, "screenshots/baselines/list-masked-baseline.png")
    # 7. assert ratio < 0.05
    pass


# ---------------------------------------------------------------------------
# Task 4 — Element-level screenshot
# ---------------------------------------------------------------------------

def test_pagination_element_screenshot(page: Page):
    """Take a screenshot of just the pagination component."""
    # TODO:
    # 1. goto SPA_URL, wait_for_load_state("networkidle")
    # 2. Find pagination: page.locator("nav, .pagination, [class*='paginat']").first
    # 3. img_bytes = pagination_locator.screenshot()
    # 4. write to screenshots/pagination.png
    # 5. assert file exists and size > 1024
    pass


# ---------------------------------------------------------------------------
# Task 5 — Mobile vs desktop visual diff
# ---------------------------------------------------------------------------

def test_mobile_vs_desktop_visual_diff(browser: Browser):
    """
    Capture the same page on desktop and mobile.
    Assert the layouts differ meaningfully (ratio > 0.05).
    """
    # TODO:
    # 1. desktop_ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    # 2. mobile_ctx  = browser.new_context(viewport={"width": 390,  "height": 844})
    # 3. Navigate both to SPA_URL, capture screenshots
    # 4. Save screenshots/desktop-view.png and screenshots/mobile-view.png
    # 5. ratio = compare_screenshots(mobile_bytes, "screenshots/desktop-view.png")
    # 6. assert ratio > 0.05  -- layouts are different
    # 7. Close both contexts
    pass
