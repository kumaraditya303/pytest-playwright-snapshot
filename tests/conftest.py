import os

pytest_plugins = ["pytester"]

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
