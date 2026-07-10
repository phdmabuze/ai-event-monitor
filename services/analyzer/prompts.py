SYSTEM_PROMPT = """
You are an assistant that classifies incoming messages.

Return:
- matched = true if the message satisfies the user's criteria.
- matched = false otherwise.

The reason should be concise (1-2 sentences).
"""

ANALYSIS_PROMPT = """
Criteria:
{criteria}

Message:
{text}
"""
