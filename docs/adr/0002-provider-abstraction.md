# ADR-0002: AI Provider Abstraction with Free/Open Defaults

**Status**: Accepted  
**Date**: 2026-07-02  
**Author**: Principal Software Architect

---

## Decision

Implement a **Provider Abstraction Layer** using the Strategy pattern. The default provider priority must favor free and open-source providers. Commercial providers (OpenAI, Anthropic, ElevenLabs) are optional plugins that can be configured but are never required.

Default provider priority for MVP:

| Category | Priority | Provider | Cost | GPU Required |
|----------|----------|----------|------|--------------|
| LLM | 1 (Primary) | DeepSeek (deepseek-chat) | Free | No |
| LLM | 2 | Qwen (Qwen2.5-72B) | Free | No |
| LLM | 3 | Gemini (Free Tier) | Free | No |
| LLM | 4 | Ollama (local) | Free | Optional |
| TTS | 1 (Primary) | pyttsx3 / gTTS | Free | No |
| TTS | 2 | Ollama TTS (local) | Free | No |
| Image | 1 (Primary) | FLUX.1-schnell (local) | Free | Optional |
| Image | 2 | Stable Diffusion (local) | Free | Optional |
| Image | 3 | Pillow fallback (text+shape) | Free | No |
| Transcription | 1 (Primary) | Whisper (local, CPU) | Free | Optional |
| Transcription | 2 | Faster-Whisper (CPU) | Free | No |

---

## Context

The MVP goal is: **"Generate a complete Shorts video using only free or open-source providers whenever possible."** The system must not require any paid API key to function. Commercial providers add value (better quality, lower latency) but must be optional plugins.

Key requirements:
1. Zero paid API keys required for MVP functionality.
2. All AI operations must have a free fallback.
3. Provider selection must be configurable at runtime via environment variables.
4. Adding a new provider must not require changes to business logic.

---

## Rationale

1. **MVP Viability**: The MVP must be demonstrable without any paid subscriptions. DeepSeek and Gemini Free Tier provide capable LLM inference at no cost. gTTS and pyttsx3 provide TTS without API keys. Whisper runs locally on CPU.

2. **Future-Proofing**: The abstraction layer means commercial providers can be added later as performance upgrades, not as requirements. Users who want higher quality can configure their own API keys.

3. **Offline Capability**: Ollama and local Whisper enable fully offline operation, which is valuable for development and demos.

4. **Cost Predictability**: By defaulting to free providers, the system has zero runtime cost. Users opt into costs explicitly.

---

## Consequences

### Positive
- MVP can be demonstrated with zero API keys.
- No vendor lock-in at the architecture level.
- Users can choose their preferred provider mix.
- Offline development possible.

### Negative
- Free providers may have lower quality (DeepSeek vs GPT-4o, gTTS vs ElevenLabs).
- Rate limits on free tiers (Gemini: 60 requests/min).
- Local models require significant disk space (Whisper large-v3: ~3GB, SD: ~6GB).

### Mitigation
- Quality evaluation pipeline can recommend switching to commercial providers when quality is insufficient.
- Rate limit handling with automatic retry and queueing.
- Download-on-demand for local models with progress indication.

---

## Compliance

- **Rule**: Every AI operation must have at least one free provider implementation.
- **Rule**: No paid API key may be required for the application to start.
- **Enforcement**: CI test that runs the full pipeline with only free providers configured.