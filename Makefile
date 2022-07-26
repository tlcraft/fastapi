run_app:
	python3 -m uvicorn src.main:app --reload

run_tests:
	python3 -m pytest -v -s

install:
	pip3 install -r requirements.txt