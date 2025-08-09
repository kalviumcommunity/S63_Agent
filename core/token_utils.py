# core/token_utils.py
from typing import Any, Dict, Optional

def _get_nested(o: Any, *path):
    cur = o
    for p in path:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(p)
        else:
            cur = getattr(cur, p, None)
    return cur

def extract_tokens_from_response(response: Any) -> Dict[str, int]:
    """
    Try common provider shapes and return dict:
    { "prompt_tokens": int, "completion_tokens": int, "total_tokens": int }
    """
    # OpenAI style: response['usage'] => {'prompt_tokens','completion_tokens','total_tokens'}
    pt = _get_nested(response, "usage", "prompt_tokens") or _get_nested(response, "usage", "promptTokenCount")
    ct = _get_nested(response, "usage", "completion_tokens") or _get_nested(response, "usage", "completionTokenCount")

    # Google/generativeai style: response.usage_metadata.prompt_token_count and candidates_token_count
    if pt is None:
        pt = _get_nested(response, "usage_metadata", "prompt_token_count") or _get_nested(response, "usage_metadata", "promptTokens")
    if ct is None:
        ct = _get_nested(response, "usage_metadata", "candidates_token_count") or _get_nested(response, "usage_metadata", "completionTokens")

    # direct fields fallback
    if pt is None:
        pt = _get_nested(response, "prompt_tokens") or _get_nested(response, "promptTokenCount")
    if ct is None:
        ct = _get_nested(response, "completion_tokens") or _get_nested(response, "completionTokenCount")

    # if total provided
    total = _get_nested(response, "usage", "total_tokens") or _get_nested(response, "total_tokens") or _get_nested(response, "usage_metadata", "total_token_count")

    # coerce to int and compute total if needed
    def _as_int(x: Optional[Any]) -> Optional[int]:
        try:
            return int(x)
        except Exception:
            return None

    pt = _as_int(pt)
    ct = _as_int(ct)
    total = _as_int(total)

    if total is None and pt is not None and ct is not None:
        total = pt + ct

    return {
        "prompt_tokens": pt or 0,
        "completion_tokens": ct or 0,
        "total_tokens": total or ( (pt or 0) + (ct or 0) )
    }

def log_tokens(response: Any, prefix: str = "[Tokens]"):
    toks = extract_tokens_from_response(response)
    print(f"{prefix} Prompt: {toks['prompt_tokens']}, Completion: {toks['completion_tokens']}, Total: {toks['total_tokens']}")