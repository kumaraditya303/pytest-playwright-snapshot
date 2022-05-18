import sys
from pathlib import Path
import pytest
import requests
import os


@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_filepath_exists(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://example.com")
            assert_snapshot(page.screenshot())
    """
    )
    filepath = (
            Path(testdir.tmpdir)
            / "snapshots"
            / "test_filepath_exists"
            / "test_snapshot"
            / f"test_snapshot[{browser_name}][{sys.platform}].png"
    ).resolve()
    result = testdir.runpytest("--browser", browser_name)
    file_path_actual, file_name = "", ""
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames
                         if f.endswith(".png")]:
            file_path_actual = dirpath
            file_name = filename
    result.assert_outcomes(failed=1)
    if not filepath.exists():
        pytest.fail(f"Filepath does not exist, but found this dir {file_path_actual} "
                    f"and filename :{file_name})")


@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_compare_pass(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://example.com")
            assert_snapshot(page.screenshot())
    """
    )
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "--> New snapshot(s) created. Please review images" in "".join(result.outlines)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_custom_image_name_generated(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://example.com")
            assert_snapshot(page.screenshot(), name="test.png")
    """
    )
    filepath = (
            Path(testdir.tmpdir)
            / "snapshots"
            / "test_custom_image_name_generated"
            / "test_snapshot"
            / f"test.png"
    ).resolve()
    result = testdir.runpytest("--browser", browser_name)
    file_path_actual, file_name = "", ""
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames
                         if f.endswith(".png")]:
            file_path_actual = dirpath
            file_name = filename
    result.assert_outcomes(failed=1)
    if not filepath.exists():
        pytest.fail(f"Filepath does not exist, but found this dir {file_path_actual} "
                    f"and filename :{file_name})")
    result.assert_outcomes(failed=1)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    "browser_name",
    ["chromium"],
)
def test_compare_fail(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://via.placeholder.com/250/000000")
            element = page.query_selector('img')
            assert_snapshot(element.screenshot())
    """
    )
    # test_name = f"{str(Path(request.node.name))}[{str(sys.platform)}]"
    filepath = (
            Path(testdir.tmpdir)
            / "snapshots"
            / "test_compare_fail"
            / "test_snapshot"
            / f"test_snapshot[{browser_name}][{sys.platform}].png"
    ).resolve()
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "--> New snapshot(s) created. Please review images" in "".join(result.outlines)
    result = testdir.runpytest("--browser", browser_name, "--update-snapshots")
    result.assert_outcomes(failed=1)
    assert "--> Snapshots updated. Please review images" in "".join(result.outlines)
    img = requests.get("https://via.placeholder.com/250/FFFFFF").content
    filepath.write_bytes(img)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "--> Snapshots DO NOT match!" in "".join(result.outlines)


@pytest.mark.parametrize(
    "browser_name",
    ["firefox", "webkit"],
)
def test_compare_with_fail_fast(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://via.placeholder.com/250/000000")
            element = page.query_selector('img')
            assert_snapshot(element.screenshot(), fail_fast=True)
    """
    )
    # test_name = f"{str(Path(request.node.name))}[{str(sys.platform)}]"
    filepath = (
            Path(testdir.tmpdir)
            / "snapshots"
            / "test_compare_with_fail_fast"
            / "test_snapshot"
            / f"test_snapshot[{browser_name}][{sys.platform}].png"
    ).resolve()
    result = testdir.runpytest("--browser", browser_name, "--update-snapshots")
    result.assert_outcomes(failed=1)
    assert "--> Snapshots updated. Please review images" in "".join(result.outlines)
    img = requests.get("https://via.placeholder.com/250/FFFFFF").content
    filepath.write_bytes(img)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    assert "--> Snapshots DO NOT match!" in "".join(result.outlines)



@pytest.mark.parametrize(
    "browser_name",
    ["chromium", "firefox", "webkit"],
)
def test_actual_expected_diff_images_generated(browser_name: str, testdir: pytest.Testdir) -> None:
    testdir.makepyfile(
        """
        def test_snapshot(page, assert_snapshot):
            page.goto("https://via.placeholder.com/250/000000")
            element = page.query_selector('img')
            assert_snapshot(element.screenshot())
    """
    )
    # test_name = f"{str(Path(request.node.name))}[{str(sys.platform)}]"
    filepath = (
            Path(testdir.tmpdir)
            / "snapshots"
            / "test_actual_expected_diff_images_generated"
            / "test_snapshot"
            / f"test_snapshot[{browser_name}][{sys.platform}].png"
    ).resolve()
    result = testdir.runpytest("--browser", browser_name, "--update-snapshots")
    result.assert_outcomes(failed=1)
    assert "--> Snapshots updated. Please review images" in "".join(
        result.outlines
    )
    img = requests.get("https://via.placeholder.com/250/FFFFFF").content
    filepath.write_bytes(img)
    result = testdir.runpytest("--browser", browser_name)
    result.assert_outcomes(failed=1)
    results_dir_name = (Path(testdir.tmpdir)
                        / "snapshot_tests_failures")
    test_results_dir = (results_dir_name
                        / "test_actual_expected_diff_images_generated"
                        / f"test_snapshot[{browser_name}][{sys.platform}]")
    actual_img = (test_results_dir / f"Actual_test_snapshot[{browser_name}][{sys.platform}].png")
    expected_img = (test_results_dir / f"Expected_test_snapshot[{browser_name}][{sys.platform}].png")
    diff_img = (test_results_dir / f"Diff_test_snapshot[{browser_name}][{sys.platform}].png")

    # Validate the actual image exists in results folder
    file_path_actual, file_name_actual = "", ""
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames
                         if f.startswith("Actual_")]:
            file_path_actual = dirpath
            file_name_actual = filename
    if not actual_img.exists():
        pytest.fail(f"Filepath does not exist, but found this dir {file_path_actual} "
                    f"and filename :{file_name_actual})")

    # Validate the expected image exists in results folder
    file_path_expected, file_name_expected = "", ""
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames
                         if f.startswith("Expected_")]:
            file_path_expected = dirpath
            file_name_expected = filename
    if not expected_img.exists():
        pytest.fail(f"Filepath does not exist, but found this dir {file_path_expected} "
                    f"and filename :{file_name_expected})")

    # Validate the difference image exists in results folder
    file_path_diff, file_name_diff = "", ""
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames
                         if f.startswith("Diff_")]:
            file_path_diff = dirpath
            file_name_diff = filename
    if not diff_img.exists():
        pytest.fail(f"Filepath does not exist, but found this dir {file_path_diff} "
                    f"and filename :{file_name_diff})")
