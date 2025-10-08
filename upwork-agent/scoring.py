def fit_score(must_have: list[str], portfolio_tags: list[str]) -> int:
    if not must_have: return 50
    overlap = len(set(must_have) & set(portfolio_tags))
    return min(100, int(60 + 40 * (overlap / max(1,len(must_have)))))