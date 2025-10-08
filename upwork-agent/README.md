# Upwork Proposal Agent
Paste a job post → get a tailored `proposal.md`. Human-in-the-loop, retrieval-aware.

## Quickstart
1) `./run.sh`  (or use Makefile targets)
2) Edit `.env` with your `OPENAI_API_KEY`
3) Rebuild index after editing `memory/portfolio.jsonl`: `python build_index.py`

## CLI
- `python app.py tests/test_job_post.txt` → writes `proposal.md`

## Env
- `MODEL` (default gpt-5), `EMBEDDING_MODEL` (default text-embedding-3-large)
- `API_MODE=1` to expose FastAPI (future extension)

## Tests
- `pytest -q`

## Notes
- Keep manual review before posting to Upwork.
- Track response rates & edit distance for quality.

## API
You can run the proposal agent as a web service using FastAPI.

- **Start server**: `make api`
- **Health check**: `curl -s http://localhost:8000/healthz`
- **Generate proposal**:

  ```sh
  curl -s -X POST http://localhost:8000/generate \
    -H "Content-Type: application/json" \
    -d '{"job_text":"Build a FastAPI bot..."}'
  ```

## UI
A simple Streamlit UI is provided for interactive use.

- **Start UI**: `make ui`
- Paste an Upwork job post into the textarea and click **Generate** to see the proposal and fit score.

## Dev Tests
Install development dependencies and run tests to ensure everything works:

    pip install -r requirements-dev.txt
    pytest -q

## Logging & Analytics

Every invocation of the proposal agent writes a row to a log so you can track usage and performance over time. By default this is a CSV file at `logs/proposals.csv`. Each row contains:

- **timestamp**: UTC ISO-8601 when the request was processed
- **fit_score**: the integer score returned by the scoring module
- **title**: the job title extracted from the post
- **must_have**: comma-separated list of required skills
- **response_chars**: number of characters in the generated proposal
- **source**: which interface generated the proposal (`cli`, `api` or `ui`)

To store logs in Google Sheets instead, set `SHEETS_MODE=sheets` in your `.env` and provide `SHEETS_SA_JSON` (path to your service account JSON), `SHEETS_SPREADSHEET` (target spreadsheet name) and optionally `SHEETS_WORKSHEET` (worksheet name). Install the optional dependencies via `pip install -r requirements-optional.txt`.

### Log demo

Use the Makefile to see logging in action:

    make log-demo

This runs the CLI against a sample job post and prints the resulting CSV file.

## API Tests

A FastAPI TestClient is included to smoke test the `/healthz` and `/generate` endpoints without network access. Run the tests with the Makefile:

    make api-test

Alternatively, install the dev requirements and run the test file directly:

    pip install -r requirements-dev.txt
    pytest -q tests/test_api_smoke.py