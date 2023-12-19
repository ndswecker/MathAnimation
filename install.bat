@echo off

:: Create virtual environment
if not exist .venv\ (
	python -m venv .venv
)

:: Activate virtual environment
call .venv\Scripts\activate

:: Update virtual environment
python -m pip install pip setuptools wheel --upgrade

:: Install dependencies
pip install -r requirements.txt --upgrade

:: Create .env from example
if not exist .env (
	copy dev.env .env
)

if not exist web\static\media\dynamic (
	mkdir web\static\media\dynamic
)
