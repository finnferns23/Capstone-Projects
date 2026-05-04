def shot_list(prompt: str) -> list[str]:
    return [
        f"Opening hook that frames the problem: {prompt}",
        "Screen or product demonstration showing the solution in action",
        "Proof point or benefit scene with measurable impact",
        "Closing scene with clear call to action",
    ]


def image_prompt(prompt: str, tone: str) -> str:
    return f"Create a polished {tone} visual concept for: {prompt}. Use clean composition, premium lighting, and modern brand styling."
