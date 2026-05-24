"""User-friendly API error messages for teaching demos."""


def format_provider_error(provider: str, exc: Exception) -> str:
    provider = provider.lower()
    text = str(exc).lower()

    if provider == "groq" and ("403" in text or "access denied" in text):
        return (
            "**Groq returned 403 Access Denied** — this is usually **not** a wrong prompt.\n\n"
            "Common causes:\n"
            "1. **Network / firewall / VPN** blocking `api.groq.com` (Groq uses Cloudflare)\n"
            "2. **Corporate or campus Wi‑Fi** blocking the API\n"
            "3. **Invalid or revoked API key** — create a new key at https://console.groq.com/keys\n\n"
            "Try:\n"
            "- Different network (mobile hotspot)\n"
            "- Disable VPN/proxy temporarily\n"
            "- Put `GROQ_API_KEY=gsk_...` in `.env` and restart Streamlit\n"
            "- Use **OpenRouter** with a Groq model if Groq direct API is blocked\n\n"
            f"Technical detail: `{exc}`"
        )

    if "401" in text or "invalid api key" in text or "authentication" in text:
        return (
            f"**{provider} authentication failed.** Check your API key in BYOK or `.env` "
            f"(no extra spaces). Regenerate the key on the provider console.\n\n"
            f"Detail: `{exc}`"
        )

    if "429" in text or "rate limit" in text:
        return (
            f"**{provider} rate limit reached.** Wait a minute or switch provider.\n\n"
            f"Detail: `{exc}`"
        )

    return f"**{provider} error:** `{exc}`"
