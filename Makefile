run_app:
	python3 -m uvicorn src.main:app --reload

run_tests:
	python3 -m pytest -v -s