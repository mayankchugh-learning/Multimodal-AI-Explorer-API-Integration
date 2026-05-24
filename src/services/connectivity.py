"""Quick provider connectivity checks for the UI."""

from groq import Groq

from src.config import ProviderKeys
from src.providers import default_model


def test_groq(keys: ProviderKeys) -> tuple[bool, str]:
    if not keys.has_groq():
        return False, "No Groq API key set."
    key = (keys.groq or "").strip()
    if not key.startswith("gsk_"):
        return False, "Groq keys usually start with `gsk_`. Check for typos or extra spaces."
    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=default_model("groq"),
            messages=[{"role": "user", "content": "Reply with exactly: ok"}],
            max_tokens=16,
            temperature=0,
        )
        reply = (response.choices[0].message.content or "").strip()
        return True, f"Connected. Model replied: {reply!r}"
    except Exception as exc:
        return False, str(exc)
