def enrich_prompt(prompt: str, audience: str, tone: str) -> str:
    return (
        f"Audience: {audience}\n"
        f"Tone: {tone}\n"
        f"Objective: {prompt.strip()}\n"
        "Deliver practical, structured, channel-ready content."
    )
