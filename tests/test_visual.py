"""Visual features, statistics and the draft scorer, on synthetic images (offline)."""

import shutil

import pytest

np = pytest.importorskip("numpy")
cv2 = pytest.importorskip("cv2")

from blueprint_engine.visual.features import extract, load_image  # noqa: E402
from blueprint_engine.visual.score import score  # noqa: E402
from blueprint_engine.visual.sheets import preview_sheet  # noqa: E402
from blueprint_engine.visual.study import outlier_ratios, spearman  # noqa: E402


def _blocks(seed=1, saturated=True, n=40, size=(720, 1280)):
    rng = np.random.default_rng(seed)
    img = np.full((*size, 3), 128, np.uint8)
    for _ in range(n):
        y, x = rng.integers(0, size[0] - 60), rng.integers(0, size[1] - 60)
        color = rng.integers(0, 256, 3) if saturated else np.full(3, rng.integers(100, 160))
        img[y:y + 60, x:x + 60] = color
    return img


def _one_subject(size=(720, 1280)):
    img = np.full((*size, 3), (40, 20, 10), np.uint8)  # dark blue-ish background (BGR)
    cv2.circle(img, (size[1] // 2, size[0] // 2), size[0] // 3, (0, 200, 255), -1)  # one big orange disc
    return img


def test_colour_features_separate_vivid_from_grey():
    vivid = extract(_blocks(saturated=True), text=False)
    grey = extract(_blocks(saturated=False), text=False)
    assert vivid.colorfulness > grey.colorfulness + 20
    assert vivid.saturation > grey.saturation


def test_clutter_vs_single_subject():
    busy = extract(_blocks(n=400), text=False)
    simple = extract(_one_subject(), text=False)
    assert busy.edge_density > simple.edge_density
    assert busy.jpeg_kb > simple.jpeg_kb
    assert simple.focal_points <= 2
    assert abs(simple.saliency_cx - 0.5) < 0.15  # attention centred on the disc


def test_squint_contrast_rewards_value_structure():
    halves = np.zeros((720, 1280, 3), np.uint8)
    halves[:, 640:] = 255
    flat = np.full((720, 1280, 3), 128, np.uint8)
    flat[::2, ::2] = 140  # fine texture only
    assert extract(halves, text=False).squint_contrast > 30 > extract(flat, text=False).squint_contrast


def test_letterboxed_youtube_fallback_is_cropped(tmp_path):
    img = np.zeros((480, 640, 3), np.uint8)
    img[60:420] = 200  # 16:9 content inside 4:3 letterbox
    p = tmp_path / "hq.jpg"
    cv2.imwrite(str(p), img)
    out = load_image(p, "thumbnail")
    assert out.shape[:2] == (360, 640) and out.mean() > 150


def test_outlier_ratio_and_spearman():
    ratios = outlier_ratios([100, 100, 300, 100, 100], window=2)
    assert ratios[2] == pytest.approx(3.0)
    rho, p = spearman(np.arange(30.0), np.arange(30.0) ** 2, permutations=500)
    assert rho == pytest.approx(1.0) and p < 0.01


def test_score_flags_wrong_formats(tmp_path):
    thumb = tmp_path / "t.png"
    cv2.imwrite(str(thumb), _one_subject(size=(900, 1280)))  # not 16:9
    res = score(thumb, "thumbnail")
    assert any(c["level"] == "fail" and "16:9" in c["message"] for c in res["checks"])

    icon = tmp_path / "i.png"
    cv2.imwrite(str(icon), _one_subject(size=(512, 600)))  # not square
    res = score(icon, "icon")
    assert any(c["level"] == "fail" and "square" in c["message"] for c in res["checks"])

    good = tmp_path / "g.png"
    cv2.imwrite(str(good), _one_subject(size=(1080, 1920)))
    res = score(good, "thumbnail", preview=tmp_path / "prev.png")
    assert not res["summary"]["fail"] and (tmp_path / "prev.png").is_file()


@pytest.mark.skipif(shutil.which("tesseract") is None, reason="tesseract not installed")
def test_score_catches_promotional_text(tmp_path):
    img = np.full((1080, 1920, 3), 30, np.uint8)
    cv2.putText(img, "FREE ROBUX", (200, 560), cv2.FONT_HERSHEY_DUPLEX, 6, (255, 255, 255), 18)
    p = tmp_path / "promo.png"
    cv2.imwrite(str(p), img)
    res = score(p, "thumbnail")
    assert any(c["level"] == "fail" and "promotional" in c["message"] for c in res["checks"])


def test_preview_sheet_sizes(tmp_path):
    out = preview_sheet(_one_subject(size=(512, 512)), "icon", tmp_path / "icon.png")
    assert out.is_file() and cv2.imread(str(out)).shape[1] >= 512
