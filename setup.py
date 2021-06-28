from pathlib import Path

from setuptools import setup

setup(
    name="pytest-playwright-snapshot",
    author="Kumar Aditya",
    author_email="",
    description="A pytest wrapper for snapshot testing with playwright",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/kumaraditya303/pytest-playwright-snapshot",
    packages=["pytest_playwright_snapshot"],
    include_package_data=True,
    install_requires=[
        "pytest_playwright>=0.1.2",
        "Pillow>=8.2.0",
        "pixelmatch==0.2.3",
    ],
    entry_points={
        "pytest11": ["playwright_snapshot = pytest_playwright_snapshot.plugin"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    python_requires=">=3.7",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
)
