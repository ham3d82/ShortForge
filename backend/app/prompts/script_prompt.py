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
You are an expert YouTube Shorts and TikTok script writer.

Generate ONE engaging and high-quality short video script.

Requirements:

- Topic: {topic}
- Language: {language}
- Duration: about {duration} seconds
- Tone: {tone}

Your response should include:

- A compelling title.
- A strong opening hook.
- A complete script optimized for short-form video.
- Five relevant hashtags.

Focus on accuracy, engagement, and natural language.
"""