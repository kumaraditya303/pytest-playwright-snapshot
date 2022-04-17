import sys
import os
import shutil
from io import BytesIO
from pathlib import Path
from typing import Any, Callable
import pytest
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


@pytest.fixture
def assert_snapshot(pytestconfig: Any, request: Any, browser_name: str) -> Callable:
    test_name = f"{str(request.node.name)}[{str(sys.platform)}]"

    def compare(img: bytes, *, threshold: float = 0.1, name=f'{test_name}.png') -> None:
        update_snapshot = pytestconfig.getoption("--update-snapshots")
        test_file_name = str(os.path.basename(request.node.fspath)).strip('.py')
        filepath = (
            Path(request.node.fspath).parent.resolve()
            / 'snapshots'
            / test_file_name
        )
        filepath.mkdir(parents=True, exist_ok=True)
        file = filepath / name

        results_dir_name = (Path(request.node.fspath).parent.resolve()
                / "snapshots_tests_failures"
        )
        test_results_dir = (
                results_dir_name
                /test_file_name/test_name
        )

        if test_results_dir.exists():
            shutil.rmtree(test_results_dir)
        if update_snapshot:
            file.write_bytes(img)
            return
        if not file.exists():
            file.write_bytes(img)
            pytest.fail("Snapshot not found, created new one. To update, use --update-snapshots")
        img_a = Image.open(BytesIO(img))
        img_b = Image.open(file)
        img_diff = Image.new("RGBA", img_a.size)

        mismatch = pixelmatch(img_a, img_b, img_diff, includeAA=True, threshold=threshold)

        if mismatch == 0:
            "Snapshots match!"
        else:

            test_results_dir.mkdir(parents=True, exist_ok=True)
            img_diff.save(f'{test_results_dir}/Diff_{name}')
            img_a.save(f'{test_results_dir}/Actual_{name}')
            img_b.save(f'{test_results_dir}/Expected_{name}')
            pytest.fail("Snapshots DO NOT match!")

    return compare


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("playwright-snapshot", "Playwright Snapshot")
    group.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Update snapshots.",
    )
