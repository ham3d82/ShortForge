# ShortForge — AI Pipeline Architecture

> **Author**: Principal Software Architect  
> **Version**: 1.0.0  
> **Last Updated**: 2026-07-02

---

## Table of Contents

1. [Pipeline Overview](#1-pipeline-overview)
2. [Provider Abstraction Layer](#2-provider-abstraction-layer)
3. [Script Generation Pipeline](#3-script-generation-pipeline)
4. [Image Generation Pipeline](#4-image-generation-pipeline)
5. [Multi-Language Support](#5-multi-language-support)
6. [Prompt Engineering Framework](#6-prompt-engineering-framework)
7. [Quality Evaluation](#7-quality-evaluation)
8. [Error Handling & Fallbacks](#8-error-handling--fallbacks)
9. [Performance & Cost Optimization](#9-performance--cost-optimization)

---

## 1. Pipeline Overview

The AI Pipeline consists of **four sub-pipelines** that can run in parallel or sequence depending on the generation stage:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI Pipeline Orchestrator                             │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pipeline 1: Script Generation                                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐      │   │
│  │  │  Topic  │ │  Hook   │ │  Body   │ │  CTA    │ │  Scene   │      │   │
│  │  │  Analyze│─▶│  Write  │─▶│  Struct │─▶│  Write  │─▶│  Parse   │      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pipeline 2: Image Generation                                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐      │   │
│  │  │  Prompt  │ │  Style  │ │  Image  │ │  Up-    │ │  Animate │      │   │
│  │  │  Expand  │─▶│  Apply  │─▶│  Gen    │─▶│  scale  │─▶│  (opt)   │      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pipeline 3: Audio Generation (TTS)                                  │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐      │   │
│  │  │  Voice  │ │  SSML   │ │  TTS    │ │  Post-  │ │  Timing  │      │   │
│  │  │  Select │─▶│  Build  │─▶│  Gen    │─▶│  Proc   │─▶│  Extract │      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pipeline 4: Caption Generation                                      │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐      │   │
│  │  │  Audio  │ │  Word   │ │  Format │ │  Trans- │ │  Style   │      │   │
│  │  │  Trans  │─▶│  Align  │─▶│  SRT    │─▶│  late   │─▶│  Apply   │      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └──────────┘      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Provider Abstraction Layer

### 2.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Application Layer (Use Cases)                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      │
│  │GenerateScript│  │GenerateImage │  │  GenerateTTS │                      │
│  │  UseCase     │  │  UseCase     │  │  UseCase     │                      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘                      │
│         │                 │                 │                                │
│         ▼                 ▼                 ▼                                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Infrastructure Layer (Provider Adapters)                            │   │
│  │                                                                       │   │
│  │  ┌─────────────────────────────────────────────────────────────┐     │   │
│  │  │  IAIService (Port)                                           │     │   │
│  │  │  ├─ generate_script(params) → ScriptResult                   │     │   │
│  │  │  ├─ generate_image(params) → ImageResult                     │     │   │
│  │  │  ├─ generate_tts(params) → TTSResult                         │     │   │
│  │  │  ├─ transcribe_audio(params) → TranscriptionResult           │     │   │
│  │  │  ├─ translate_text(params) → TranslationResult               │     │   │
│  │  │  └─ evaluate_quality(params) → QualityScore                  │     │   │
│  │  └─────────────────────────────────────────────────────────────┘     │   │
│  │                           ▲                                           │   │
│  │          ┌────────────────┼────────────────┐                          │   │
│  │          │                │                │                          │   │
│  │  ┌───────┴──────┐ ┌──────┴───────┐ ┌──────┴───────┐                  │   │
│  │  │  LLMAdapter  │ │  ImageAdapter│ │  TTSAdapter  │                  │   │
│  │  │  (OpenAI/    │ │  (Stability/  │ │  (ElevenLabs/│                  │   │
│  │  │  Anthropic/  │ │  FLUX/        │ │  Azure/      │                  │   │
│  │  │  Ollama)     │ │  SD Local)    │ │  Local)      │                  │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Provider Registry

```python
# backend/infrastructure/external_services/provider_registry.py

class ProviderRegistry:
    """
    Central registry for AI provider adapters.
    Uses strategy pattern — providers are swappable at runtime.
    """
    
    _providers: dict[str, type[BaseAdapter]] = {}
    _health_cache: dict[str, HealthStatus] = {}
    
    def register(self, name: str, adapter_class: type[BaseAdapter]):
        self._providers[name] = adapter_class
    
    def get_llm(self, preferred: str = None) -> LLMAdapter:
        return self._select_provider('llm', preferred)
    
    def get_image(self, preferred: str = None) -> ImageAdapter:
        return self._select_provider('image', preferred)
    
    def get_tts(self, preferred: str = None) -> TTSAdapter:
        return self._select_provider('tts', preferred)
    
    def _select_provider(self, category: str, preferred: str) -> BaseAdapter:
        """
        Selection logic:
        1. If preferred provider specified and healthy → use it
        2. If preferred failed → fallback to next healthy provider
        3. Circuit breaker: skip providers with >5 failures in 60s
        4. Cost optimization: prefer cheaper provider if quality >= threshold
        """
```

### 2.3 Provider Configuration

```yaml
# backend/core/config/providers.yaml

llm:
  providers:
    - name: openai
      model: gpt-4o
      priority: 1  # Primary
      cost_per_token: 0.00001
      max_retries: 3
      timeout_sec: 30
    
    - name: anthropic
      model: claude-3.5-sonnet
      priority: 2  # Fallback
      cost_per_token: 0.000015
      max_retries: 2
      timeout_sec: 30
    
    - name: ollama
      model: llama-3.1-70b
      priority: 3  # Local fallback
      cost_per_token: 0  # Free
      max_retries: 1
      timeout_sec: 120

image:
  providers:
    - name: stability
      model: stable-diffusion-3.5
      priority: 1
      cost_per_image: 0.04
    
    - name: flux
      model: flux-pro
      priority: 2
      cost_per_image: 0.05
    
    - name: local
      model: sdxl-turbo
      priority: 3
      cost_per_image: 0  # GPU cost only
      requires_gpu: true

tts:
  providers:
    - name: elevenlabs
      priority: 1
      cost_per_char: 0.000001
    
    - name: azure
      priority: 2
      cost_per_char: 0.000015
    
    - name: local
      priority: 3
      quality: "acceptable"
      requires_gpu: false
```

---

## 3. Script Generation Pipeline

### 3.1 Pipeline Steps

#### Step 1: Topic Analysis

```
Input: User's topic string (e.g., "Benefits of intermittent fasting")
       Tone: educational
       Duration: 60 seconds
       Language: en

Process:
1. Extract key concepts and entities (NLP)
2. Identify target audience (demographic inference)
3. Suggest angle/hook direction
4. Identify trending angles in the topic space
5. Check for factual claims that need citations

Output:
{
  "core_concept": "Intermittent fasting health benefits",
  "key_points": ["autophagy", "insulin sensitivity", "weight loss"],
  "target_audience": "Health-conscious adults 25-45",
  "suggested_angle": "Myth-busting common misconceptions",
  "trending_hashtags": ["#intermittentfasting", "#healthtips"],
  "requires_citations": ["autophagy study", "weight loss stats"]
}
```

#### Step 2: Hook Generation

```
Input: Topic analysis output
       Hook count: 3

Prompt Template (v1_hook.txt):
───
You are a YouTube Shorts hook specialist. Your goal is to write
hooks that achieve >70% retention in the first 3 seconds.

Topic: {topic}
Tone: {tone}
Target Audience: {audience}
Key Points: {key_points}

Write {count} different hooks. Each hook must:
- Be under 150 characters
- Start with a pattern: question, shocking stat, bold claim, or curiosity gap
- Include 1-3 power words from: {power_words}
- Be optimized for the hook's first 2 seconds (most critical)

Format as JSON array:
[
  {
    "hook_text": "...",
    "pattern_used": "question|statistic|claim|curiosity",
    "expected_retention_score": 0.0-1.0,
    "power_words_used": ["..."]
  }
]
───

Output:
[
  {
    "hook_text": "What if I told you fasting doesn't burn muscle?",
    "pattern_used": "curiosity",
    "expected_retention_score": 0.85,
    "power_words_used": ["what if", "doesn't"]
  },
  {
    "hook_text": "3 studies prove fasting extends lifespan by 11%",
    "pattern_used": "statistic",
    "expected_retention_score": 0.82,
    "power_words_used": ["proves", "extends"]
  }
]
```

#### Step 3: Body Structure

```
Input: Selected hook (user-approved)
       Key points: 3
       Target duration: 60 seconds

Prompt Template (v1_body.txt):
───
Structure the body of a YouTube Shorts video.

Hook: {hook}
Key Points: {key_points}
Duration: {duration_sec} seconds
Tone: {tone}

The body should follow this pacing:
- Seconds 0-3: Hook
- Seconds 3-15: First key point (problem/interest)
- Seconds 15-30: Second key point (solution/value)
- Seconds 30-45: Third key point (proof/social proof)
- Seconds 45-55: Summary/transition
- Seconds 55-60: Call-to-action

Each scene must specify:
- Duration (in seconds)
- Voiceover text (what the narrator says)
- Visual style (background type, animation cues)
- Image generation prompt (for scene background)

Return as JSON.
───

Output: See SceneBreakdown schema in API spec.
```

#### Step 4: CTA Generation

```
Input: Topic, tone, body summary

Prompt Template (v1_cta.txt):
───
Write a call-to-action for a YouTube Shorts video.

Topic: {topic}
Tone: {tone}
Video Summary: {summary}

Requirements:
- 2-4 seconds in length
- Clear, specific action (like, subscribe, comment, share)
- Include a reason WHY they should take action
- Create urgency or FOMO
- Max 80 characters

Provide 3 options with different CTA types:
1. Engagement (comment)
2. Subscription (subscribe)
3. Sharing (share/tag a friend)
───
```

#### Step 5: Scene Parsing & Validation

```
Input: LLM raw JSON output

Validation rules:
1. Total duration matches target (±2 seconds)
2. Each scene has all required fields
3. Voiceover text fits within scene duration (reading speed check)
4. Image prompts are valid (not empty, < 500 chars)
5. No duplicate scene indices

Reading speed validation:
- Average speaking rate: 150 words/min (2.5 words/sec)
- For 60s video, max ~150 words total
- Each scene's voiceover must fit its duration

Output:
{
  "is_valid": true,
  "total_duration_sec": 60,
  "total_words": 142,
  "scenes": [...],
  "warnings": ["Scene 3 voiceover may be tight at 10s for 30 words"]
}
```

### 3.2 Script Generation Flow (Full)

```
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│  User Prompt  │───▶│  Step 1: Topic       │───▶│  Step 2: Hooks   │
│  + Settings    │    │  Analysis (LLM)     │    │  Generation (LLM)│
└──────────────┘    └──────────────────────┘    └────────┬─────────┘
                                                         │
                                                         ▼
                                              ┌──────────────────┐
                                              │  User Selects    │
                                              │  Best Hook       │
                                              └────────┬─────────┘
                                                         │
                                                         ▼
┌──────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│  Step 5:      │◄───│  Step 4: CTA         │◄───│  Step 3: Body   │
│  Validate &   │    │  Generation (LLM)    │    │  Structure (LLM)│
│  Parse        │    └──────────────────────┘    └──────────────────┘
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│  Quality Evaluation                                               │
│  ├─ Check Word Count: 142/150 words (PASS)                      │
│  ├─ Check Duration Match: 60s/60s (PASS)                        │
│  ├─ Check Coherence Score: 0.89 (PASS > 0.7)                    │
│  ├─ Check Tone Consistency: 0.92 (PASS > 0.8)                    │
│  └─ Overall Quality Score: 0.87 / 1.0                            │
│                                                                  │
│  If score < threshold (0.6): Auto-regenerate with feedback      │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 Character & Pacing Constraints

| Duration | Total Words | Scenes | Hook (sec) | Body (sec) | CTA (sec) |
|----------|------------|--------|------------|------------|-----------|
| 15 sec | 35-40 | 2-3 | 3 | 10 | 2 |
| 30 sec | 70-80 | 3-4 | 3 | 24 | 3 |
| 45 sec | 105-115 | 4-5 | 3 | 38 | 4 |
| 60 sec | 140-150 | 5-6 | 3 | 52 | 5 |
| 90 sec | 210-225 | 7-8 | 3 | 82 | 5 |
| 180 sec | 420-450 | 12-15 | 3 | 170 | 7 |

---

## 4. Image Generation Pipeline

### 4.1 Pipeline Steps

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Scene       │───▶│  Prompt         │───▶│  Style           │
│  Description │    │  Engineering    │    │  Application     │
└──────────────┘    └──────────────────┘    └────────┬─────────┘
                                                      │
                                                      ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Animation   │◄───│  Upscaling       │◄───│  Generation      │
│  (Deforum)   │    │  (Real-ESRGAN)   │    │  (SD/FLUX)       │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

### 4.2 Prompt Engineering for Images

```python
# backend/ai/prompts/templates/image/v1_generation.txt

PROMPT_TEMPLATE = """
Generate a text-to-image prompt for a YouTube Shorts scene.

Scene Context:
- Description: {scene_description}
- Visual Style: {visual_style}
- Tone: {tone}
- Duration: {duration_sec} seconds
- Previous Scene: {previous_scene_summary} (for continuity)

Requirements for the prompt:
1. Format: "[Subject], [action/pose], [environment], [lighting], [style], [composition]"
2. Include style keywords: {style_keywords}
3. Negative prompt must exclude: {negative_prompt_items}
4. Optimize for {resolution} aspect ratio (9:16 portrait)
5. Ensure visual consistency with adjacent scenes
6. Add quality boosters: "highly detailed, 8k, professional lighting"

Return as JSON:
{
    "positive_prompt": "...",
    "negative_prompt": "...",
    "style_preset": "...",
    "seed": null,  # null = random, int = fixed for reproducibility
    "cfg_scale": 7.0,
    "steps": 30
}
"""
```

### 4.3 Image Style Presets

| Preset | Description | Keywords | Best For |
|--------|-------------|----------|----------|
| `modern` | Clean, minimalist | flat design, clean lines, pastel | Educational |
| `cinematic` | Film-like, dramatic | cinematic lighting, depth of field, 35mm | Storytelling |
| `anime` | Japanese animation | anime style, cel shaded, vibrant | Explainers |
| `3d_render` | 3D-like quality | 3D render, octane render, blender | Tech content |
| `watercolor` | Artistic, soft | watercolor, soft edges, artistic | Inspirational |
| `cyberpunk` | Neon, futuristic | cyberpunk, neon lights, dark | Tech/coding |
| `vintage` | Retro, nostalgic | vintage, film grain, warm tones | History |
| `abstract` | Non-representational | abstract, geometric, fluid art | Motivation |

### 4.4 Animation Pipeline

Images can be animated using two techniques depending on requirements:

#### Technique A: Ken Burns Effect (Simple, Fast)

```
┌──────────────┐    ┌──────────────────┐
│  Static      │───▶│  Zoom/Pan        │   < 50ms per frame
│  Image       │    │  Parameters      │
└──────────────┘    └──────┬───────────┘
                           │
                           ▼
┌──────────────┐    ┌──────────────────┐
│  Output      │◄───│  FFmpeg Filter   │
│  Video Clip  │    │  (zoompan)       │
└──────────────┘    └──────────────────┘
```

Parameters:
- Zoom: 1.0 → 1.15 (subtle zoom in)
- Pan: vary by scene (left→right, top→bottom)
- Duration: matches scene duration
- Easing: ease-in-out for smooth motion

#### Technique B: Deforum Animation (Complex, GPU-Intensive)

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Initial     │───▶│  Frame           │───▶│  Next Frame      │
│  Image       │    │  Interpolation   │    │  Generation      │
└──────────────┘    └──────────────────┘    └──────────────────┘
                                                    │
                                                    ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Final       │◄───│  Frame           │◄───│  ... Repeat      │
│  Video       │    │  Assembly        │    │  for N frames    │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

Parameters:
- Frames: 12-24 FPS × scene duration
- Motion: 3D camera translation + rotation
- Strength: 0.6-0.8 (controls how much each frame changes)
- Steps: 20-25 per frame (lower = faster, less quality)

### 4.5 Upscaling Pipeline

```python
# backend/media/image/upscaler.py

class ImageUpscaler:
    """
    Upscales generated images using Real-ESRGAN.
    
    Pipeline:
    1. Receive base image (1080×1920 or lower)
    2. Apply Real-ESRGAN (4x upscale → 4320×7680)
    3. Downscale to target resolution (1080×1920)
       Note: This seems counterintuitive, but the AI upscaler
       produces better details even after downscaling.
    4. Apply sharpening filter
    5. Save to S3
    
    GPU requirements:
    - VRAM: 4GB minimum for 1080p, 8GB recommended
    - CUDA: Compute Capability 7.0+ (Turing+)
    """
    
    MODELS = {
        "realesr-general-x4v3": "General purpose (default)",
        "realesr-animevideov3": "Anime/cartoon optimized",
    }
```

### 4.6 Image Generation Settings by Quality Tier

| Setting | Draft | Standard | High |
|---------|-------|----------|------|
| **Provider** | SDXL Turbo | Stable Diffusion 3.5 | FLUX Pro |
| **Steps** | 4-8 | 25-30 | 40-50 |
| **CFG Scale** | 3.0 | 7.0 | 8.0 |
| **Resolution** | 768×1344 | 1080×1920 | 1080×1920 |
| **Upscale** | No | Yes (2x) | Yes (4x) |
| **Time per image** | ~1s | ~10s | ~30s |
| **Cost per image** | $0.003 | $0.04 | $0.05 |

---

## 5. Multi-Language Support

### 5.1 Language Pipeline

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Original    │───▶│  Translation     │───▶│  Voiceover       │
│  Script (en) │    │  (LLM or Google) │    │  (TTS in target) │
└──────────────┘    └──────────────────┘    └──────────────────┘
                           │                          │
                           ▼                          ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Captions    │◄───│  Word Timing     │◄───│  Audio Timing    │
│  (Translated)│    │  (Realignment)   │    │  (Target Lang)   │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

### 5.2 Supported Languages (Phase 1)

| Language | Code | TTS Support | Whisper Support | Script Quality |
|----------|------|-------------|-----------------|----------------|
| English | en | Excellent | Excellent | Native |
| Spanish | es | Excellent | Excellent | Good |
| French | fr | Excellent | Excellent | Good |
| German | de | Excellent | Excellent | Good |
| Portuguese | pt | Excellent | Good | Good |
| Italian | it | Excellent | Good | Good |
| Japanese | ja | Good | Good | Fair |
| Korean | ko | Good | Good | Fair |
| Chinese (Simplified) | zh | Good | Excellent | Good |
| Arabic | ar | Fair | Good | Fair |
| Hindi | hi | Good | Good | Fair |

### 5.3 Translation Strategy

```python
# backend/ai/pipeline/translation.py

class TranslationPipeline:
    """
    Multi-strategy translation for Shorts scripts.
    
    Strategy Selection:
    1. If source == target → bypass translation
    2. If LLM available (gpt-4o) → LLM translation (best quality)
       - Preserves tone, humor, idioms
       - Adapts cultural references
       - Maintains pacing constraints
    3. If LLM fallback needed → Google Translate API
       - Faster but loses nuance
       - Post-edit for tone preservation
    4. For caption-only translation → Direct word-level mapping
    
    Quality Checks:
    - Back-translation verification (translate back, compare similarity)
    - Duration constraint check (translated text must fit audio timing)
    - Cultural reference adaptation log
    """
    
    def translate_script(self, script: Script, target_lang: str) -> Script:
        """
        1. Translate full text preserving scene structure
        2. Check word count vs target duration
        3. If too long: summarize scenes to fit
        4. If too short: expand with transitional phrases
        5. Generate new TTS timing estimates
        6. Return translated Script object
        """
```

---

## 6. Prompt Engineering Framework

### 6.1 Prompt Registry

```python
# backend/ai/prompts/registry.py

class PromptRegistry:
    """
    Central registry for all prompt templates with versioning.
    
    Features:
    - Versioned templates (immutable after release)
    - A/B testing between versions
    - Rollback capability
    - Template inheritance (base → specialized)
    - Dynamic variable injection
    - Token usage estimation
    """
    
    def __init__(self):
        self._templates: dict[str, dict[int, PromptTemplate]] = {}
        self._active_versions: dict[str, int] = {}
        self._experiments: dict[str, ABTest] = {}
    
    def register(self, name: str, version: int, template: PromptTemplate):
        """Register a new template version."""
    
    def get(self, name: str, version: int = None) -> PromptTemplate:
        """Get template; uses active version if not specified."""
    
    def activate(self, name: str, version: int):
        """Set active version for a template."""
    
    def start_experiment(self, name: str, version_a: int, version_b: int, traffic_split: float):
        """Start A/B test between two versions."""
```

### 6.2 Template Structure

```
backend/ai/prompts/
├── __init__.py
├── registry.py                    # PromptRegistry implementation
│
├── templates/
│   ├── script_generation/
│   │   ├── base.yaml              # Base template with shared instructions
│   │   ├── v1_topic_analyze.txt   # Topic analysis prompt
│   │   ├── v1_hook.txt            # Hook generation
│   │   ├── v2_hook.txt            # A/B test: different hook strategy
│   │   ├── v1_body.txt            # Body structure
│   │   ├── v1_cta.txt             # CTA generation
│   │   └── v1_short.yaml          # Short-form (15-30s) optimized
│   │
│   ├── image_prompts/
│   │   ├── v1_generation.txt      # Image prompt construction
│   │   ├── v1_negative.txt        # Common negative prompts
│   │   └── v1_style_presets.yaml  # Style preset definitions
│   │
│   ├── evaluation/
│   │   ├── v1_quality_score.txt   # Script quality evaluation
│   │   ├── v1_coherence.txt       # Coherence scoring
│   │   └── v1_cultural_fit.txt    # Cultural appropriateness check
│   │
│   └── translation/
│       ├── v1_preserve_tone.txt   # Tone-preserving translation
│       └── v1_adapt_culture.txt   # Cultural adaptation
│
└── examples/
    ├── successful_shorts.yaml     # Few-shot examples (high engagement)
    └── failed_shorts.yaml         # Examples of what to avoid
```

### 6.3 Prompt Versioning Strategy

| Version | Date | Change | Status |
|---------|------|--------|--------|
| v1_hook | 2026-07-01 | Initial hook prompt | Active |
| v2_hook | 2026-07-15 | A/B test: more power words | Testing (25%) |
| v3_hook | 2026-08-01 | Killed: lower quality | Archived |
| v4_hook | 2026-09-01 | Emotional triggers added | Active (75%) |

### 6.4 Prompt Optimization Rules

1. **Token Budget**: Keep prompts under 4000 tokens (including few-shot examples)
2. **Structured Output**: Always request JSON with explicit schema
3. **Temperature Control**:
   - Hook generation: 0.8 (more creative)
   - Body structure: 0.5 (more consistent)
   - CTA generation: 0.7 (balanced)
   - Translation: 0.3 (more precise)
4. **Few-Shot Selection**: Dynamically select 2-3 examples based on topic similarity
5. **Self-Consistency**: Generate 3 responses, select most consistent (for critical paths)

---

## 7. Quality Evaluation

### 7.1 Script Quality Scoring

```python
class ScriptQualityEvaluator:
    """
    Multi-dimensional script quality evaluation.
    
    Dimensions:
    1. Relevance (0-1): How well does it address the topic?
    2. Engagement (0-1): Hook strength, pacing, retention potential
    3. Coherence (0-1): Logical flow between scenes
    4. Tone Consistency (0-1): Matches requested tone throughout
    5. CTA Effectiveness (0-1): Call-to-action clarity and urgency
    6. Readability (0-1): Flesch-Kincaid score appropriate for audience
    7. Duration Accuracy (0-1): Fits within target ±5%
    
    Overall Score = Weighted average of dimensions
    """
    
    WEIGHTS = {
        "relevance": 0.20,
        "engagement": 0.25,
        "coherence": 0.15,
        "tone_consistency": 0.10,
        "cta_effectiveness": 0.10,
        "readability": 0.10,
        "duration_accuracy": 0.10,
    }
    
    THRESHOLDS = {
        "auto_approve": 0.85,  # No human review needed
        "auto_regenerate": 0.50,  # Auto-trigger regeneration
        "human_review": 0.70,  # Flag for human review
    }
```

### 7.2 Image Quality Scoring

| Criterion | Method | Threshold |
|-----------|--------|-----------|
| **Aesthetic Score** | LAION aesthetic predictor | > 6.0 / 10 |
| **NSFW Detection** | CLIP-based NSFW filter | < 0.1 probability |
| **Artifact Detection** | BRISQUE no-reference | < 40 score |
| **Text Rendering** | OCR check on overlaid text | > 90% accuracy |
| **Style Match** | CLIP similarity to style preset | > 0.3 cosine sim |
| **Resolution** | Size check | >= 1080×1920 |

### 7.3 Audio Quality Scoring

| Criterion | Method | Threshold |
|-----------|--------|-----------|
| **Naturalness** | MOS prediction model | > 3.5 / 5 |
| **Silence Detection** | Voice activity detection | < 15% silence |
| **Clipping** | Peak amplitude check | < -1 dBFS |
| **Background Noise** | SNR estimation | > 25 dB |
| **Speed Accuracy** | Duration vs target | ±5% tolerance |

---

## 8. Error Handling & Fallbacks

### 8.1 Provider Failure Handling

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Error Handling Hierarchy                                                   │
│                                                                              │
│  Level 1: Transient Error (timeout, rate limit, 5xx)                       │
│  └─ Retry with exponential backoff (max 3 attempts)                        │
│     └─ Still failing? → Level 2                                            │
│                                                                              │
│  Level 2: Provider Failure (consistent errors)                             │
│  └─ Failover to next provider in priority order                            │
│     └─ Circuit breaker: skip this provider for 60s                         │
│     └─ Still failing? → Level 3                                            │
│                                                                              │
│  Level 3: All Providers Failed                                             │
│  └─ Return degraded result if possible                                     │
│     └─ Script: Use template-based fallback                                  │
│     └─ Image: Use solid color + text overlay fallback                       │
│     └─ TTS: Use pyttsx3 offline TTS                                        │
│     └─ Notify admin via Sentry + alert                                     │
│                                                                              │
│  Level 4: Critical Failure                                                 │
│  └─ Mark pipeline as failed                                                │
│  └─ Return detailed error to user                                          │
│  └─ Log full trace for debugging                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Content Safety Filters

```python
# backend/ai/pipeline/safety.py

class ContentSafetyFilter:
    """
    Multi-layer content safety filtering.
    
    Layers:
    1. Input Filter: Reject prompts containing blocked terms
    2. Output Filter: Scan generated content for violations
    3. Image Filter: NSFW detection on generated images
    4. Cultural Filter: Region-specific content appropriateness
    
    Blocked Categories:
    - Violence/gore
    - Hate speech
    - Explicit content
    - Copyrighted characters
    - Political misinformation
    - Medical claims (without disclaimer)
    """
    
    def check_script(self, script: Script) -> SafetyResult:
        """Scan script text for policy violations."""
        
    def check_image(self, image_path: str) -> SafetyResult:
        """Run NSFW detection on generated image."""
```

---

## 9. Performance & Cost Optimization

### 9.1 Cost Breakdown (per video)

| Component | Provider | Cost/Unit | Units/Video (60s) | Total |
|-----------|----------|-----------|-------------------|-------|
| Script Gen | GPT-4o | $0.01/1K tokens | ~2K tokens | $0.02 |
| Hook Gen | GPT-4o-mini | $0.002/1K tokens | ~0.5K tokens | $0.001 |
| Image Gen | SD 3.5 | $0.04/image | 5 images | $0.20 |
| Image Upscale | Real-ESRGAN | Free (GPU) | 5 images | $0.00 |
| TTS | ElevenLabs | $0.001/char | ~600 chars | $0.60 |
| Caption | Whisper | Free (GPU) | 60s audio | $0.00 |
| Video Render | FFmpeg GPU | Free | 1 video | $0.00 |
| **Total** | | | | **~$0.82/video** |

### 9.2 Optimization Strategies

| Strategy | Savings | Implementation |
|----------|---------|----------------|
| **Prompt Caching** | ~30% | Cache LLM responses for identical prompts (24h TTL) |
| **Model Tiering** | ~40% | Use GPT-4o-mini for hooks, GPT-4o only for body |
| **Batch Image Gen** | ~15% | Generate all scene images in one API call |
| **Draft Mode** | ~60% | Use SDXL Turbo (4 steps) for preview, FLUX for final |
| **Local Inference** | ~100% | Run Whisper + Real-ESRGAN locally on GPU |
| **Audio Caching** | ~50% | Cache TTS for identical text segments |

### 9.3 GPU Resource Planning

| Workload | GPU Required | VRAM | Recommended Card | Concurrent Jobs |
|----------|-------------|------|------------------|-----------------|
| Image Gen (SD) | Yes | 8GB | RTX 4070+ | 2 per GPU |
| Image Upscale | Yes | 4GB | RTX 3060+ | 4 per GPU |
| Animation | Yes | 12GB | RTX 4090 | 1 per GPU |
| Whisper | Optional | 2GB | Any CUDA | 8 per GPU |
| FFmpeg NVENC | Yes | 1GB | Any NVENC | 4 per GPU |
| LLM (Ollama) | Yes | 16GB | RTX 4090 24GB | 1 per GPU |

### 9.4 Caching Strategy

```python
# backend/infrastructure/external_services/cache.py

class AICache:
    """
    Multi-level caching for AI responses.
    
    Level 1: In-memory (Redis)
    - LLM responses (prompt_hash → response)
    - TTS audio (text_hash → audio_path)
    - Image metadata (prompt_hash → image_path)
    - TTL: 24 hours
    
    Level 2: Persistent (Database + S3)
    - Previous generation results
    - User preference embeddings
    - TTL: 30 days or until project deleted
    """
    
    def _generate_key(self, provider: str, model: str, params: dict) -> str:
        """Generate deterministic cache key from request parameters."""
        
    def get_or_generate(self, key: str, generator: Callable) -> Any:
        """Cache-aside pattern: return cached or generate and store."""
```

---

## Appendix: Key Interfaces

```python
# backend/application/interfaces/ai_service.py

class IAIService(ABC):
    """Port interface for AI service providers."""
    
    @abstractmethod
    async def generate_script(self, params: ScriptGenerationParams) -> ScriptResult:
        ...
    
    @abstractmethod
    async def generate_image(self, params: ImageGenerationParams) -> ImageResult:
        ...
    
    @abstractmethod
    async def generate_tts(self, params: TTSGenerationParams) -> TTSResult:
        ...
    
    @abstractmethod
    async def transcribe_audio(self, audio_path: str, language: str) -> TranscriptionResult:
        ...
    
    @abstractmethod
    async def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        ...
    
    @abstractmethod
    async def evaluate_quality(self, script: str, params: QualityParams) -> QualityScore:
        ...


class BaseAdapter(ABC):
    """Base class for all provider adapters."""
    
    provider_name: str
    model_name: str
    priority: int
    
    @abstractmethod
    async def health_check(self) -> HealthStatus:
        ...
    
    @abstractmethod
    async def get_cost_estimate(self, params: Any) -> CostEstimate:
        ...