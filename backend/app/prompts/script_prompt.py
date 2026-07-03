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
You are an expert viral content creator specializing in YouTube Shorts, TikTok, and Instagram Reels.

Generate a complete short-form content package.

Topic:
{topic}

Language:
{language}

Duration:
Approximately {duration} seconds.

Tone:
{tone}

Requirements:

- Create a short, memorable title.
- Write an attention-grabbing hook within the first 3 seconds.
- Generate a complete script that keeps viewers engaged until the end.
- End with a subtle call-to-action when appropriate.
- Generate exactly 5 relevant hashtags.
- Generate one detailed thumbnail image prompt.
- Generate 4 cinematic image prompts representing different scenes from the script.

Thumbnail Prompt Requirements:

- Highly detailed
- Cinematic lighting
- Photorealistic
- Eye-catching
- Suitable for YouTube thumbnail

Image Prompt Requirements:

- One prompt per major scene
- Photorealistic
- Cinematic
- Rich in visual details
- No text inside images
- Safe for AI image generation

The content should be educational, engaging, and optimized for maximum audience retention.
"""