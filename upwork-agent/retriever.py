import json, os
from typing import List, Tuple

try:
    import numpy as np  # type: ignore
except ImportError:
    class np:  # minimal shim
        @staticmethod
        def array(x, dtype=None): return x

try:
    import faiss  # type: ignore
except ImportError:
    faiss = None

try:
    from openai import OpenAI  # type: ignore
except ImportError:
    OpenAI = None

def _hash_embed(text: str, dim: int = 256) -> list[float]:
    vec = [0.0] * dim
    for i, ch in enumerate(text.encode("utf-8")):
        vec[i % dim] += (ch % 13) / 13.0
    norm = (sum(v*v for v in vec) ** 0.5) or 1.0
    return [v / norm for v in vec]

def _base_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def embed(texts: List[str]):
    if OpenAI is None:
        return np.array([_hash_embed(t) for t in texts], dtype="float32")
    try:
        client = OpenAI()
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
        em = client.embeddings.create(model=model, input=texts)
        return np.array([e.embedding for e in em.data], dtype="float32")
    except Exception:
        return np.array([_hash_embed(t) for t in texts], dtype="float32")

def build(portfolio_path="memory/portfolio.jsonl", index_path="memory/index.faiss"):
    base = _base_dir()
    portfolio_path = os.path.join(base, portfolio_path)
    index_path = os.path.join(base, index_path)
    meta_path = os.path.join(base, "memory", "portfolio.meta.json")

    records, texts = [], []
    with open(portfolio_path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            records.append(rec)
            texts.append(rec.get("blurb", ""))

    os.makedirs(os.path.join(base, "memory"), exist_ok=True)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(records, f)

    if faiss is None:
        return
    X = embed(texts)
    try:
        X = X.astype("float32")  # if numpy available
    except Exception:
        pass
    faiss.normalize_L2(X)
    idx = faiss.IndexFlatIP(len(X[0]))
    idx.add(X)
    faiss.write_index(idx, index_path)

def search(query: str, k=5, index_path="memory/index.faiss") -> List[Tuple[dict, float]]:
    base = _base_dir()
    index_path = os.path.join(base, index_path)
    meta_path = os.path.join(base, "memory", "portfolio.meta.json")

    if faiss is not None and os.path.exists(index_path):
        try:
            idx = faiss.read_index(index_path)
            q = embed([query])
            try:
                q = q.astype("float32")
            except Exception:
                pass
            faiss.normalize_L2(q)
            D, I = idx.search(q, k)
            meta = json.load(open(meta_path, "r", encoding="utf-8"))
            return [(meta[i], float(D[0][j])) for j, i in enumerate(I[0])]
        except Exception:
            pass

    if os.path.exists(meta_path):
        meta = json.load(open(meta_path, "r", encoding="utf-8"))
        return [(m, 0.0) for m in meta[:max(1, k)]]
    return []
