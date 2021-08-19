import sys
from pathlib import Path

import pytest
import requests


@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_snapshot_create(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://example.com")
            assert_snapshot(page.screenshot(), "test-snapshot.png")
    """
    )
    filepath = (
        Path(testdir.tmpdir)
        / "__snapshots__"
        / browser_name
        / sys.platform
        / "test-snapshot.png"
    ).resolve()

    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "Snapshot not found, use --update-snapshots to update it." in "".join(
        result.outlines
    )
    assert not filepath.exists()

    result = testdir.runpytest("--browser", browser_name, "--update-snapshots")
    result.assert_outcomes(passed=1)
    assert filepath.exists()


@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_snapshot_fail(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://via.placeholder.com/250/000000")
            element = page.query_selector('img')
            assert_snapshot(element.screenshot(), "test-snapshot.png")
    """
    )
    filepath = (
        Path(testdir.tmpdir)
        / "__snapshots__"
        / browser_name
        / sys.platform
        / "test-snapshot.png"
    ).resolve()

    result = testdir.runpytest("--browser", browser_name, "--update-snapshots")
    result.assert_outcomes(passed=1)
    assert filepath.exists()
    img = requests.get("https://via.placeholder.com/250/FFFFFF").content
    filepath.write_bytes(img)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "Snapshots does not match" in "".join(result.outlines)
