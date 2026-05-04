def keyword_pack(prompt: str) -> list[str]:
    words = [word.strip(".,!?;:").lower() for word in prompt.split() if len(word) > 3]
    unique = []
    for word in words:
        if word not in unique:
            unique.append(word)
    return unique[:8] or ["content", "strategy", "assistant"]


def meta_description(prompt: str) -> str:
    return f"A practical guide to {prompt.strip()[:120]} with clear positioning, messaging, and execution steps."
