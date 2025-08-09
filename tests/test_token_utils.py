# tests/test_token_utils.py
from core.token_utils import extract_tokens_from_response

def test_openai_style():
    resp = {"usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}}
    toks = extract_tokens_from_response(resp)
    assert toks["prompt_tokens"] == 10
    assert toks["completion_tokens"] == 5
    assert toks["total_tokens"] == 15