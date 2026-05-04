def section(title: str, body: str) -> str:
    return f"## {title}\n{body.strip()}"


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)
