import sys
from io import BytesIO
from pathlib import Path

import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.nodes import get_fslocation_from_item
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


@pytest.fixture
def assert_snapshot(pytestconfig: Config, request: SubRequest, browser_name: str):
    def compare(img: bytes, name: str):
        update_snapshot = pytestconfig.getoption("--update-snapshots")
        filepath = (
            Path(request.node.fspath).parent
            / "__snapshots__"
            / browser_name
            / sys.platform
        )
        filepath.mkdir(parents=True, exist_ok=True)
        if update_snapshot:
            with open(filepath / name, mode="wb") as f:
                f.write(img)
            return
        if not (filepath / name).exists():
            pytest.fail("Snapshot not found, use --update-snapshots to create it.")
        image = Image.open(BytesIO(img))
        golden = Image.open(filepath / name)
        diff_pixels = pixelmatch(image, golden, includeAA=True)
        assert diff_pixels == 0, "Snapshot does not match"

    return compare


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("playwright-snapshot", "Playwright Snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update snapshots.",
    )
