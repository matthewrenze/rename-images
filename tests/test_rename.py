"""Tests for Rename.py (run with pytest from the repo root)."""

import importlib.util
from pathlib import Path

from PIL import Image

RENAME_PY = Path(__file__).resolve().parent.parent / "Rename.py"


def load_rename():
    spec = importlib.util.spec_from_file_location("rename_mod", RENAME_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_photo(path, timestamp="2024:05:01 10:00:00"):
    img = Image.new("RGB", (16, 16), "red")
    exif = Image.Exif()
    exif.get_ifd(0x8769)[0x9003] = timestamp
    img.save(path, exif=exif)


def test_same_second_photos_do_not_crash_or_overwrite(tmp_path, capsys):
    make_photo(tmp_path / "a_photo.jpg")
    make_photo(tmp_path / "b_photo.jpg")
    rename = load_rename()

    rename.rename_files(str(tmp_path))  # must not raise FileExistsError

    out, _ = capsys.readouterr()
    assert "Skipped" in out
    # first photo renamed, second one left untouched, nothing lost
    assert (tmp_path / "20240501-100000.jpg").exists()
    assert (tmp_path / "b_photo.jpg").exists()


def test_single_photo_still_renamed(tmp_path):
    make_photo(tmp_path / "a_photo.jpg")
    rename = load_rename()

    rename.rename_files(str(tmp_path))

    assert (tmp_path / "20240501-100000.jpg").exists()
    assert not (tmp_path / "a_photo.jpg").exists()
