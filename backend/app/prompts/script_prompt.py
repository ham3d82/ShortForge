"""
Prompt builder for script generation.
"""


def build_script_prompt(
    topic: str,
    language: str,
    duration: int,
    tone: str,
) -> str:
    """Build the prompt used to generate a short-form video script."""

    return f"""
You are an expert short-form content writer.

Create a high-quality YouTube Shorts / TikTok script.

Requirements:
- Topic: {topic}
- Language: {language}
- Duration: approximately {duration} seconds
- Tone: {tone}

Return the result in exactly this format:

TITLE:
...

HOOK:
...

SCRIPT:
...

HASHTAGS:
#tag1 #tag2 #tag3 #tag4 #tag5
"""