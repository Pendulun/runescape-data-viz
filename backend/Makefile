install:
	pwd
	python3 -m pip install -r requirements.txt

run: install
	python3 -m pip list
	fastapi dev main.py

run-from-scratch:
	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip --list
	python3 -m pip install -r requirements.txt
	python3 -m pip --list
	fastapi dev main.py

test_item_service:
	python -m unittest domain.tests.domain.test_item_service

test: test_item_service