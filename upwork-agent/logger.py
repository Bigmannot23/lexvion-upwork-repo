import os, csv, datetime
from typing import Dict, Any

# Sheets deps are optional; import guarded
try:
    import gspread  # type: ignore
    from google.oauth2.service_account import Credentials  # type: ignore
except Exception:
    gspread = None  # type: ignore
    Credentials = None  # type: ignore


def _now_iso() -> str:
    """Return current UTC time in ISO 8601 format (no microseconds) with 'Z' suffix."""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _env(name: str, default: str | None = None) -> str | None:
    """Helper to fetch environment variables with optional default."""
    return os.getenv(name, default)


def _ensure_dir(p: str) -> None:
    """Ensure the directory exists."""
    os.makedirs(p, exist_ok=True)


def _to_row(payload: Dict[str, Any]) -> list[str]:
    """Convert the event payload into a list representing a CSV/Sheets row."""
    return [
        payload.get("ts", _now_iso()),
        str(payload.get("fit_score", "")),
        payload.get("title", ""),
        ",".join(payload.get("must_have", []) or []),
        str(payload.get("response_chars", "")),
        payload.get("source", ""),
    ]


def log_event(data: Dict[str, Any]) -> None:
    """
    Dual-mode logger.
    - CSV mode (default): writes to logs/proposals.csv
    - Sheets mode: requires SHEETS_MODE=sheets, SHEETS_SA_JSON, SHEETS_SPREADSHEET, SHEETS_WORKSHEET
    Each call appends a row with timestamp, fit_score, title, comma-joined must_have, response_chars, and source.
    Fallbacks gracefully to CSV if Sheets dependencies or configuration are missing.
    """
    mode = (_env("SHEETS_MODE", "csv") or "csv").lower()
    # Attempt sheets logging if requested and dependencies are available
    if mode == "sheets":
        if gspread is not None and Credentials is not None:
            try:
                sa_path = _env("SHEETS_SA_JSON")
                spreadsheet = _env("SHEETS_SPREADSHEET")
                worksheet_name = _env("SHEETS_WORKSHEET", "proposals")
                if not (sa_path and spreadsheet):
                    raise RuntimeError("Sheets config incomplete")
                scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                creds = Credentials.from_service_account_file(sa_path, scopes=scopes)
                gc = gspread.authorize(creds)
                sh = gc.open(spreadsheet)
                # reuse or create worksheet
                worksheet_titles = [w.title for w in sh.worksheets()]
                if worksheet_name in worksheet_titles:
                    ws = sh.worksheet(worksheet_name)
                else:
                    ws = sh.add_worksheet(worksheet_name, rows=1000, cols=10)
                ws.append_row(_to_row(data))
                return
            except Exception:
                # fall back to CSV if any error occurs
                mode = "csv"
        else:
            # dependencies missing
            mode = "csv"
    # CSV mode
    logs_dir = _env("LOGS_DIR", "logs") or "logs"
    _ensure_dir(logs_dir)
    csv_path = os.path.join(logs_dir, "proposals.csv")
    header = ["timestamp", "fit_score", "title", "must_have", "response_chars", "source"]
    write_header = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(_to_row(data))
