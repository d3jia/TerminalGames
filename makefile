# makefile 
# setup venv and run the program

.PHONY: setup run

setup: main.py
	python3 -m venv venv

run: main.py
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python3 main.py