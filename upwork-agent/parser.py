try:
    from pydantic import BaseModel  # type: ignore
except ImportError:
    # Minimal fallback if pydantic is unavailable
    class BaseModel:  # type: ignore
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
import json, os
try:
    from openai import OpenAI  # type: ignore
except ImportError:
    # Provide a stub when the openai package isn't available
    class OpenAI:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass

        class chat:
            class completions:
                @staticmethod
                def create(*args, **kwargs):
                    raise RuntimeError("OpenAI library not available.")

        class embeddings:
            @staticmethod
            def create(*args, **kwargs):
                raise RuntimeError("OpenAI library not available.")
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    # Fallback if python-dotenv is unavailable
    def load_dotenv(*args, **kwargs):
        return None

load_dotenv()


class ParsedJob(BaseModel):
    title: str
    summary: str
    deliverables: list[str]
    must_have: list[str]
    nice_to_have: list[str]
    budget: str | None = None
    timeline: str | None = None
    domain: list[str] = []
    risks: list[str] = []


def heuristic_parse(text: str) -> ParsedJob:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    title = lines[0][:120] if lines else "Upwork Project"
    budget = next((l for l in lines if "$" in l or "Budget" in l), None)
    timeline = next((l for l in lines if any(w in l.lower() for w in ["day","week","hour","deadline"])), None)
    kws = ["python","fastapi","langchain","openai","rag","automation","streamlit","api","etl","sql"]
    must = [k for k in kws if any(k in l.lower() for l in lines)]
    return ParsedJob(
        title=title,
        summary=" ".join(lines)[:1500],
        deliverables=["Initial analysis","MVP","Documentation","Handover"],
        must_have=sorted(set(must)),
        nice_to_have=[],
        budget=budget,
        timeline=timeline,
        domain=[],
        risks=[]
    )


def llm_parse(text: str) -> ParsedJob:
    """Structured JSON extraction via LLM; falls back to heuristic on error."""
    client = OpenAI()
    # Resolve prompt path relative to this file
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(base_dir, "prompts", "extract_requirements.md")
    prompt = open(prompt_path).read()
    try:
        completion = client.chat.completions.create(
            model=os.getenv("MODEL","gpt-5"),
            messages=[
                {"role":"system","content":prompt},
                {"role":"user","content":text}
            ],
            temperature=0
        )
        raw = completion.choices[0].message.content.strip()
        data = json.loads(raw)
        return ParsedJob(**data)
    except Exception:
        return heuristic_parse(text)