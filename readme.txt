============================================================
Demo Clients - Demonstration clients for Audiogram gRPC API.
============================================================

Unpack all archive contents into an empty directory and follow instructions below.


===== Install Python 3.11 =====

1. Check Python version:

$ python --version
or
$ python3 --version

If version is 3.11 or higher - skip to the next section and use it to create virtual environment.


2. Install Python 3.11 (if not installed)

Debian:
$ sudo apt install python3.11

Windows:
Download installer at
https://www.python.org/downloads/release/python-3119/
and run it.


===== Install Dependencies =====

1. Create virtual environment (venv)

$ python -m venv .venv


2. Activate venv

Debian:
$ source ./.venv/bin/activate

Windows:
$ .\.venv\Scripts\activate


3. Install dependencies

$ pip install -r requirements.txt


===== Run Demo Clients =====

Get short help from command:
$ python -m clients.main --help

Or open documentation located in ./docs/ to read detailed help and usage instructions.
