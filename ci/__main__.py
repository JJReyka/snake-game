import argparse
import os
import subprocess

PACKAGE_FOLDER = os.path.join(os.path.dirname(__file__), '../snakegame')


def flake8():
    subprocess.run(['python', '-m', 'flake8', PACKAGE_FOLDER])


def test():
    subprocess.run(['python', '-m', 'unittest', 'discover', PACKAGE_FOLDER])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--flake8', action='store_true')
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()
    if args.flake8:
        flake8()
    if args.test:
        test()
