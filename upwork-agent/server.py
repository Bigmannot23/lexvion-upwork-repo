import os
try:
    from fastapi import FastAPI
except ImportError:
    # Provide a minimal stub if FastAPI is unavailable
    class FastAPI:
        def __init__(self, *args, **kwargs):
            pass

        def get(self, *args, **kwargs):
            def decorator(f): return f
            return decorator

        def post(self, *args, **kwargs):
            def decorator(f): return f
            return decorator

    class Response:
        pass

try:
    from pydantic import BaseModel
except ImportError:
    # Fallback for BaseModel when pydantic is unavailable
    class BaseModel:  # type: ignore
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

from parser import llm_parse
from retriever import search
from generator import draft_proposal
from scoring import fit_score
from logger import log_event


app = FastAPI(title="Upwork Proposal Agent API", version="2.2")


class GenerateIn(BaseModel):
    job_text: str


class GenerateOut(BaseModel):
    proposal_md: str
    fit_score: int


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/generate", response_model=GenerateOut)
def generate(payload: GenerateIn):
    job = llm_parse(payload.job_text)
    query = f"{job.title} {' '.join(job.must_have)} {job.summary[:500]}"
    matches = search(query, k=5)
    proposal_md, tags = draft_proposal(job, matches)
    score = fit_score(job.must_have, tags)
    # Log event for API invocation
    log_event({
        "fit_score": score,
        "title": getattr(job, "title", ""),
        "must_have": getattr(job, "must_have", []),
        "response_chars": len(proposal_md),
        "source": "api",
    })
    return {"proposal_md": proposal_md, "fit_score": score}