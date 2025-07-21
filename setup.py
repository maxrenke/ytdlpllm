"""Install file for ytdlpllm."""
from setuptools import setup, find_packages

setup(
    name="ytdlpllm",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Dependencies here, e.g., 'requests'
    ],
    entry_points={
        "console_scripts": [
            "ytdlpllm = ytdlpllm.main:main",
        ],
    },
)