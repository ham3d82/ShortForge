# ShortForge — AI Agent Orchestration Design

This document defines the **AI agent architecture** for ShortForge. Rather than a single monolithic prompt, we decompose the Shorts generation process into specialized sub-agents, each with a focused responsibility.

---

## 🧩 Agent Architecture

```
                     ┌─────────────────────────────────┐
                     │     Orchestrator Agent            │
                     │  (Manages workflow, state, retry)│
                     └──────────┬──────────────────────┘
                                │
          ┌─────────────────────┼──────────────────────┐
          │                     │                      │
          ▼                     ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Script Agent   │  │   Audio Agent     │  │   Video Agent    │
│  (LLM-based)     │  │  (TTS, Mixing)    │  │  (Composition)   │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│- Topic analysis  │  │- Voice selection  │  │- Scene planning  │
│- Hook generation │  │- Speech synthesis │  │- Clip assembly   │
│- Structure       │  │- Pacing & pauses  │  │- Transitions     │
│- Call-to-action  │  │- Background music │  │- Overlays        │
└──────────────────┘  └──────────────────┘  └──────────────────┘
          │                     │                      │
          └─────────────────────┼──────────────────────┘
                                │
                                ▼
                     ┌─────────────────────────┐
                     │    Caption Agent          │
                     │  (Whisper + Burn-in)      │
                     ├─────────────────────────┤
                     │- Audio transcription     │
                     │- Word-level timestamps   │
                     │- SRT/ASS formatting      │
                     │- Burn-in compositing     │
                     └─────────────────────────┘
```

---

## 🤖 Agent Definitions

### 1. Orchestrator Agent
- **Responsibility**: Coordinate the entire generation pipeline; handle state transitions, retries, and failures.
- **Input**: User topic, style preferences, duration target
- **Output**: Final video URL or error report
- **Pattern**: Chain-of-responsibility with circuit breaker for each sub-agent

### 2. Script Agent
- **Responsibility**: Generate a compelling Shorts script optimized for engagement.
- **Input**: Topic, tone (humorous/inspirational/educational), target duration, keywords
- **Output**: Structured script with scene breakdown, hook, body, CTA
- **Model**: GPT-4o / Claude 3.5 Sonnet (via LangChain)
- **Prompt Strategy**: Few-shot examples + constraints (character count, pacing)

### 3. Audio Agent
- **Responsibility**: Convert script to natural-sounding speech with proper pacing.
- **Input**: Script text, voice ID, language, speed
- **Output**: WAV/MP3 audio file, timing metadata
- **Provider**: ElevenLabs (primary) or Azure TTS (fallback)
- **Processing**: Silence insertion for dramatic pauses, background music layering

### 4. Video Agent
- **Responsibility**: Assemble video clips, animations, and overlays.
- **Input**: Audio file, captions, style template, background media
- **Output**: MP4 video (1080x1920, 9:16)
- **Engine**: FFmpeg via Python subprocess + MoviePy composition helpers
- **Features**: Ken Burns effect on stills, dynamic text overlays, transitions

### 5. Caption Agent
- **Responsibility**: Generate and burn-in captions with word-level highlighting.
- **Input**: Audio file, script text, style (font, color, position)
- **Output**: Video with burned-in subtitles, SRT file
- **Engine**: Whisper (transcription) + FFmpeg (drawtext filter)
- **Features**: Word-by-word highlight sync, multiple languages

---

## 📝 Prompt Engineering Strategy

### Prompt Registry (`backend/ai/prompts/`)

```
backend/ai/prompts/
├── __init__.py
├── registry.py           # Central prompt registry with versioning
├── templates/
│   ├── script_generation/
│   │   ├── v1_hook.txt       # Hook generation prompt
│   │   ├── v1_body.txt       # Body structure prompt
│   │   └── v1_cta.txt        # Call-to-action prompt
│   ├── thumbnail/
│   │   └── v1_description.txt
│   └── evaluation/
│       └── v1_quality_score.txt
└── examples/
    ├── successful_shorts.yaml
    └── failed_shorts.yaml
```

### Guiding Principles
1. **Chain-of-Thought**: Script agent reasons step-by-step (hook → body → CTA)
2. **Structured Output**: Always return JSON with defined schema (Pydantic models)
3. **Few-Shot**: Include 2-3 exemplar Shorts scripts in prompt context
4. **Constrained Generation**: Enforce character limits via `max_tokens` + system prompt
5. **Self-Critique**: Optional second LLM call to evaluate output quality

---

## 🔄 Generation Pipeline (Detailed)

```
  User Prompt
      │
      ▼
┌─────────────────────┐
│  1. Script Agent     │  ◄── LLM Call (GPT-4o)
│     - Analyze topic  │       Returns ScriptJSON
│     - Write hook     │
│     - Structure body │
│     - Add CTA        │
└─────────┬───────────┘
          │ Script approved? ── No ──► Edit UI (Frontend)
          │ Yes
          ▼
┌─────────────────────┐
│  2. Audio Agent      │  ◄── ElevenLabs / Azure TTS
│     - Select voice   │       Returns .wav + timing.json
│     - Generate TTS   │
│     - Add pauses     │
│     - Mix background │
└─────────┬───────────┘
          │
          ▼
┌──────────────────────┐
│  3. Caption Agent     │  ◄── Whisper
│     - Transcribe audio│       Returns .srt + word-level
│     - Generate SRT    │       timestamps
│     - Style captions  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  4. Video Agent       │  ◄── FFmpeg / MoviePy
│     - Load media      │       Returns .mp4
│     - Apply Ken Burns │       (1080x1920, 30fps)
│     - Add captions    │
│     - Render + encode │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  5. Thumbnail Agent   │  ◄── Pillow / AI Gen
│     - Extract frame   │       Returns thumbnail.jpg
│     - Overlay text    │
│     - Generate if AI  │
└──────────┬───────────┘
           │
           ▼
     Ready for Review
```

---

## ⚙️ Error Handling & Retry

| Failure Point | Strategy | Retries |
|---------------|----------|---------|
| LLM API timeout | Exponential backoff + jitter | 3 |
| LLM malformed output | Re-prompt with stricter schema | 2 |
| TTS generation failure | Fallback to offline TTS (pyttsx3) | 1 |
| FFmpeg render crash | Retry with different codec | 2 |
| YouTube upload | Exponential backoff + webhook callback | 3 |

---

## 📊 Evaluation & Quality

- **Script Quality Score**: Relevance, engagement, tone consistency (LLM-judged)
- **Audio Quality**: Naturalness score, silence detection
- **Video Quality**: Resolution check, bitrate compliance, freeze-frame detection
- **Human-in-the-Loop**: All generated content requires user approval before publishing

---

## 🔌 Extensibility

New agents can be added by:
1. Creating a new directory under `backend/ai/agents/`
2. Implementing the `BaseAgent` interface
3. Registering in the `OrchestratorAgent` pipeline
4. Adding corresponding prompt templates

Example future agents:
- **Music Agent**: AI music generation (Suno / Udio)
- **Viral Agent**: Trend analysis + hashtag optimization
- **A/B Agent**: Multi-variant testing of hooks/titles