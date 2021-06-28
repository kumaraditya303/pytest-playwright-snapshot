# Pytest Plugin for Snapshot Testing with Playwright

This plugin enables snapshot testing in playwright like snapshotting screenshots of pages, element handles etc.

## Installation 

```bash
$ pip install pytest-playwright-snapshot

```

## Usage

This plugin provides a `assert_snapshot` fixture which is used to create snapshots and compare it.

Example:

```python
def test_myapp(page, assert_snapshot):
    page.goto("https://example.com")
    assert_snapshot(page.screenshot(), "example.png")
```

Ths first time you run pytest, you will get error like 

```console
Failed: Snapshot not found, use --update-snapshots to create it.
```

As first you need to create golden snapshots to which this plugin will compare in future. 

To create snapshots run:

```bash
$ pytest --update-snapshots
```

This will create snapshots for your tests, after that you can run the tests are usual and this will compare the snapshots.

## License 

Apache 2.0 LICENSE 
