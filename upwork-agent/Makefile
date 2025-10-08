.PHONY: venv install build-index run test api ui log-demo api-test
venv:
	python3 -m venv .venv && . .venv/bin/activate && pip install -U pip
install:
	. .venv/bin/activate && pip install -r requirements.txt
build-index:
	. .venv/bin/activate && python build_index.py
run:
	. .venv/bin/activate && python app.py tests/test_job_post.txt
test:
	. .venv/bin/activate && pip install -r requirements-dev.txt && pytest -q
api:
	. .venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8000
ui:
	. .venv/bin/activate && streamlit run streamlit_ui.py

# Demo logging locally by running the CLI on a test job post and showing the CSV
log-demo:
	. .venv/bin/activate && python app.py tests/test_job_post.txt && ls -l logs/proposals.csv

# Run API smoke tests using pytest and httpx TestClient
api-test:
	. .venv/bin/activate && pip install -r requirements-dev.txt && pytest -q tests/test_api_smoke.py