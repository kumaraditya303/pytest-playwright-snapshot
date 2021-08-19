import sys
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


@pytest.fixture
def assert_snapshot(pytestconfig: Any, request: Any, browser_name: str) -> Callable:
    def compare(img: bytes, name: str, *, threshold: float = 0.1) -> None:
        update_snapshot = pytestconfig.getoption("--update-snapshots")
        filepath = (
            Path(request.node.fspath).parent.resolve()
            / "__snapshots__"
            / browser_name
            / sys.platform
        )
        filepath.mkdir(parents=True, exist_ok=True)
        file = filepath / name
        if update_snapshot:
            file.write_bytes(img)
            return
        if not file.exists():
            pytest.fail("Snapshot not found, use --update-snapshots to update it.")
        image = Image.open(BytesIO(img))
        golden = Image.open(file)
        diff_pixels = pixelmatch(image, golden, threshold=threshold)
        assert diff_pixels == 0, "Snapshots does not match"

    return compare


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright-snapshot", "Playwright Snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update snapshots.",
    )
