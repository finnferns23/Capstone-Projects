def headline(prompt: str, audience: str) -> str:
    return f"Content Strategy for {audience}: {prompt.strip().capitalize()}"


def call_to_action(task: str) -> str:
    actions = {
        "email": "Reply to this email to book a quick consultation.",
        "social": "Share this with someone who needs better content workflows.",
        "campaign": "Start with one campaign pillar and scale the winning format.",
    }
    return actions.get(task, "Use this content as a practical starting point and refine for your channel.")
