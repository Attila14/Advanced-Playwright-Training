# Exercise 05 — Visual Testing

## 🎯 Goal

Capture screenshots of testauto.app pages and detect unintended visual regressions automatically — using raw `page.screenshot()` with Pillow-based pixel comparison and committed baseline images. No Node.js plugins required.

Before writing any code, **navigate to https://testauto.app/task-manager-spa** and notice:
- The task titles change as real users add and delete tasks
- The "Updated" column shows live timestamps
- The page layout and structure stays consistent

The goal of visual testing is to catch layout changes while ignoring content changes.

---

## 📖 Background

### How visual testing works in Python Playwright

The Node.js Playwright API has a built-in snapshot helper that is absent from the Python API. In Python we use `page.screenshot()` directly and compare images with Pillow:

```python
from PIL import Image, ImageChops
import io, os

def compare_screenshots(current_bytes: bytes, baseline_path: str, tolerance: float = 0.01) -> float:
    """
    Returns the ratio of differing pixels (0.0 = identical).
    Saves a diff PNG next to the baseline if differences exist.
    """
    current = Image.open(io.BytesIO(current_bytes)).convert("RGB")

    if not os.path.exists(baseline_path):
        # First run — save as baseline
        current.save(baseline_path)
        return 0.0

    baseline = Image.open(baseline_path).convert("RGB")
    if current.size != baseline.size:
        current = current.resize(baseline.size)

    diff = ImageChops.difference(current, baseline)
    pixels = diff.convert("L").getdata()
    changed = sum(1 for p in pixels if p > 10)   # threshold per-pixel brightness
    ratio = changed / len(pixels)
    return ratio
```

### Masking dynamic regions before comparison

Overwrite dynamic areas with a solid colour before saving or comparing:

```python
from PIL import Image, ImageDraw
import io

def mask_regions(screenshot_bytes: bytes, regions: list[dict]) -> bytes:
    """
    regions: list of {"x":int, "y":int, "width":int, "height":int}
    Fills each region with magenta so it is ignored in diffs.
    """
    img = Image.open(io.BytesIO(screenshot_bytes)).convert("RGB")
    draw = ImageDraw.Draw(img)
    for r in regions:
        draw.rectangle([r["x"], r["y"], r["x"]+r["width"], r["y"]+r["height"]], fill=(255, 0, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
```

### Capturing bounding boxes for masking

```python
# Get the bounding box of a locator to use as a mask region
box = page.locator("table tbody td:nth-child(6)").first.bounding_box()
# box = {"x": 900, "y": 140, "width": 180, "height": 400}
```

---

## 🏗️ Files to work in

| File | What to build |
|------|--------------|
| `src/tests/test_visual.py` | All tasks for this exercise |
| `screenshots/baselines/` | Committed baseline images |

---

## ✅ Task 1 — Save full-page screenshots of key states

Take and save full-page screenshots of three page states:

| State | URL | Save to |
|-------|-----|---------|
| List view | `/task-manager-spa` | `screenshots/list-view.png` |
| Board view | `/task-manager-spa?view=board` | `screenshots/board-view.png` |
| Login modal | click Login button | `screenshots/login-modal.png` |

Assert each file exists and has size `> 5 KB`.

---

## ✅ Task 2 — Baseline comparison

1. On first run, save `screenshots/baselines/list-view-baseline.png`
2. On second run, capture a new screenshot and call `compare_screenshots()`
3. Assert the ratio of differing pixels is `< 0.15` (15% tolerance for live content)

Use the helper function from the Background section above.

---

## ✅ Task 3 — Mask dynamic columns before comparison

The task table has dynamic columns (timestamps, task titles). Before comparing:

1. Capture the full-page screenshot as bytes
2. Find the bounding boxes of the "Due Date" and "Updated At" columns using `.bounding_box()`
3. Call `mask_regions()` to fill those areas with magenta
4. Save the masked image as the baseline / compare against the masked baseline

Assert the comparison ratio is `< 0.05` — much tighter, because the noisy parts are masked.

---

## ✅ Task 4 — Element-level screenshot

Locate the pagination component at the bottom of the list and take a screenshot of just that element:

```python
pagination = page.locator("nav[aria-label*='page'], .pagination, [class*='pagination']").first
img_bytes = pagination.screenshot()
```

Save to `screenshots/pagination.png`. Assert file exists and size `> 1 KB`.

---

## ✅ Task 5 — Mobile viewport visual diff

Create two contexts — desktop (1440×900) and mobile (390×844) — and capture the same page in both.

Compare them using `compare_screenshots()`. Assert the ratio of differing pixels is `> 0.05` — proving the layouts are meaningfully different.

Save both:
- `screenshots/desktop-view.png`
- `screenshots/mobile-view.png`

---

## 🏃 Run your tests

```bash
# First run — creates baselines
pytest src/tests/test_visual.py -v

# Subsequent runs — compares against baselines
pytest src/tests/test_visual.py -v

# To reset a baseline, delete the file and run again
rm screenshots/baselines/list-view-baseline.png
```

---

## 💡 Tips

- Commit your `screenshots/baselines/` folder to Git so the team shares the same baselines.
- Never run visual tests with `-n` (parallel) — screenshot timing is sensitive.
- `page.screenshot(full_page=True)` captures content below the fold; omit `full_page=True` for viewport-only.
- Pillow is already in `requirements.txt` — no additional install needed.

---

## 📌 Reference

- [Pillow — Image module](https://pillow.readthedocs.io/en/stable/reference/Image.html)
- [Playwright Python — page.screenshot()](https://playwright.dev/python/docs/api/class-page#page-screenshot)
- [Playwright Python — locator.screenshot()](https://playwright.dev/python/docs/api/class-locator#locator-screenshot)
