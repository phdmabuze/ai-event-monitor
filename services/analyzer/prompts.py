SYSTEM_PROMPT = """
You are an assistant that classifies incoming messages against a numbered list
of criteria.

Return:
- criterion_id = the id of the single criterion the message matches, or null
  if the message doesn't match any of them. If the message could reasonably
  match more than one criterion, pick only the single most fitting one.

The reason should be concise (1-2 sentences).
"""

ANALYSIS_PROMPT = """
Criteria:
{criteria}

Message:
{text}
"""

CRITERION_LINE = "- id={id}: {name} - {description}"
