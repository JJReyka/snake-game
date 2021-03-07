from setuptools import find_packages, setup

setup(
    name="SnakeGame",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "snake_game = snakegame.main:cli"
        ]
    }
)