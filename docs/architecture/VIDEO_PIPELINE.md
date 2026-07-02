# ShortForge — Video Pipeline Architecture

> **Author**: Principal Software Architect  
> **Version**: 1.0.0  
> **Last Updated**: 2026-07-02

---

## Table of Contents

1. [Pipeline Overview](#1-pipeline-overview)
2. [Video Composition Engine](#2-video-composition-engine)
3. [Audio Processing Pipeline](#3-audio-processing-pipeline)
4. [Subtitle / Caption Pipeline](#4-subtitle--caption-pipeline)
5. [Thumbnail Generation](#5-thumbnail-generation)
6. [FFmpeg GPU Acceleration](#6-ffmpeg-gpu-acceleration)
7. [Output Specifications](#7-output-specifications)
8. [Error Handling & Retry](#8-error-handling--retry)
9. [Performance Benchmarks](#9-performance-benchmarks)

---

## 1. Pipeline Overview

The Video Pipeline takes assets from the AI Pipeline (script, audio, images, captions) and composes them into a final YouTube Shorts video.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Video Pipeline Orchestrator                          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Stage 1: Scene Planning                                             │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Parse   │  │  Assign  │  │  Layout  │  │  Timing  │            │   │
│  │  │  Script  │─▶│  Media   │─▶│  Scene   │─▶│  Map     │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Stage 2: Asset Preparation                                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Ken     │  │  Image   │  │  Audio   │  │  Caption │            │   │
│  │  │  Burns   │─▶│  Overlay │─▶│  Mix     │─▶│  Prep    │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Stage 3: Composition (FFmpeg)                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Scene   │  │  Transi- │  │  Caption │  │  Audio   │            │   │
│  │  │  Clips   │─▶│  tions   │─▶│  Burn-in │─▶│  Merge   │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Stage 4: Final Rendering                                           │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │   │
│  │  │  Encode  │  │  Meta    │  │  Upload  │  │  Cleanup │            │   │
│  │  │  (NVENC) │─▶│  Inject  │─▶│  to S3   │─▶│  Temp    │            │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Video Composition Engine

### 2.1 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  VideoCompositionEngine                                                     │
│                                                                              │
│  The engine builds an FFmpeg filter complex graph programmatically.          │
│  No high-level library (MoviePy) in production — direct FFmpeg subprocess   │
│  for maximum performance and control.                                       │
│                                                                              │
│  ┌────────────────┐                                                         │
│  │  Composition   │  Builds the filter graph as a directed acyclic graph    │
│  │  Graph Builder │                                                         │
│  └───────┬────────┘                                                         │
│          │                                                                   │
│          ▼                                                                   │
│  ┌────────────────┐                                                         │
│  │  Filter Graph  │  JSON representation of the complete filter chain       │
│  │  (JSON)        │  Debuggable, inspectable, cacheable                     │
│  └───────┬────────┘                                                         │
│          │                                                                   │
│          ▼                                                                   │
│  ┌────────────────┐                                                         │
│  │  FFmpeg CLI    │  Converts graph → ffmpeg -filter_complex arguments      │
│  │  Generator     │  + codec parameters, output flags                       │
│  └───────┬────────┘                                                         │
│          │                                                                   │
│          ▼                                                                   │
│  ┌────────────────┐                                                         │
│  │  Subprocess    │  Async subprocess with progress monitoring via stderr   │
│  │  Runner        │  Reads 'frame=xxx' or 'time=xx:xx:xx.xx' for progress  │
│  └────────────────┘                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Filter Graph Example (Simple)

```python
# For a video with: background image + Ken Burns + text overlay + captions

filter_complex = """
[0:v]zoompan=z='min(zoom+0.0015,1.15)':d=150:fps=30,format=yuv420p[v0];
[1:v]scale=1080:1920,format=yuv420p[v1];
[v0][v1]overlay=0:0:format=auto,drawtext=
  fontfile=/usr/share/fonts/Inter-Regular.ttf:
  text='Hello World':
  fontsize=48:
  fontcolor=white:
  x=(w-text_w)/2:
  y=h-th-100:
  enable='between(t,0,3)'[v_out]
"""
```

### 2.3 Scene Composition

Each scene in the video is composed of:

```
┌─────────────────────────────────────────────────────────────────┐
│  Scene Layout (9:16 Portrait)                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Top Bar (optional)                                       │    │
│  │  - Progress bar (if multi-part series)                   │    │
│  │  - Channel logo (optional)                                │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │                                                          │    │
│  │  Background (Animated Image / Video)                     │    │
│  │  - Ken Burns effect applied                               │    │
│  │  - 1080×1920 resolution                                   │    │
│  │                                                          │    │
│  │                                                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │  Caption Text (burned-in)                       │    │    │
│  │  │  - Bottom third                                  │    │    │
│  │  │  - Word-by-word highlight                        │    │    │
│  │  │  - Max 2 lines                                   │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                                                          │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │  Bottom Bar                                       │    │    │
│  │  │  - Like/Subscribe overlay (CTA)                  │    │    │
│  │  │  - Social handle (optional)                      │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │  Safe Zone Margins                                       │    │
│  │  - Left/Right: 5% padding                               │    │
│  │  - Top/Bottom: 8% padding                               │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Composition Config (JSON)

```json
{
  "resolution": "1080x1920",
  "fps": 30,
  "scenes": [
    {
      "index": 0,
      "duration_sec": 5.0,
      "background": {
        "type": "image",
        "source": "s3://shortforge-media/images/scene_0.png",
        "ken_burns": {
          "zoom_start": 1.0,
          "zoom_end": 1.15,
          "pan_x_start": 0,
          "pan_x_end": -50,
          "pan_y_start": 0,
          "pan_y_end": 0,
          "easing": "ease_in_out"
        }
      },
      "overlays": [
        {
          "type": "text",
          "content": "Hook text here",
          "position": { "x": "center", "y": "center" },
          "font": "Inter-Bold.ttf",
          "font_size": 72,
          "color": "#FFFFFF",
          "stroke_color": "#000000",
          "stroke_width": 2,
          "animation": {
            "type": "fade_in",
            "duration_sec": 0.5
          }
        }
      ],
      "audio": {
        "voiceover": {
          "source": "s3://shortforge-media/audio/scene_0.mp3",
          "start_offset_ms": 0
        },
        "background_music": {
          "source": "s3://shortforge-media/music/background.mp3",
          "volume": 0.3,
          "fade_in_ms": 500,
          "fade_out_ms": 500
        }
      }
    }
  ],
  "captions": {
    "source": "s3://shortforge-media/captions/scene_0.srt",
    "style": {
      "font": "Inter-Regular.ttf",
      "font_size": 48,
      "color": "#FFFFFF",
      "highlight_color": "#FFD700",
      "background_color": "#00000080",
      "position": "bottom_center",
      "max_lines": 2,
      "word_highlight_ms": 200
    }
  },
  "transitions": [
    {
      "from_scene": 0,
      "to_scene": 1,
      "type": "fade",
      "duration_sec": 0.3
    }
  ],
  "output": {
    "format": "mp4",
    "codec": "h264_nvenc",
    "bitrate_kbps": 12000,
    "max_bitrate_kbps": 15000,
    "profile": "high",
    "level": "4.2",
    "pixel_format": "yuv420p",
    "color_primaries": "bt709",
    "color_trc": "bt709",
    "colorspace": "bt709"
  }
}
```

### 2.5 Transition Effects

| Transition | FFmpeg Filter | GPU Support | Duration |
|------------|--------------|-------------|----------|
| **Cut** | None (direct concatenation) | Yes | 0s |
| **Fade** | `fade=t=in:st=0:d=0.3` | Yes | 0.3s |
| **Crossfade** | `xfade=transition=fade:duration=0.3:offset=4.7` | Yes | 0.3s |
| **Slide Left** | `xfade=transition=slideleft:duration=0.3` | Yes | 0.3s |
| **Slide Right** | `xfade=transition=slideright:duration=0.3` | Yes | 0.3s |
| **Zoom** | `xfade=transition=zoomin:duration=0.5` | Yes | 0.5s |
| **Wipe** | `xfade=transition=wipeleft:duration=0.3` | Yes | 0.3s |
| **Pixelize** | `xfade=transition=pixelize:duration=0.5` | Partial | 0.5s |

### 2.6 Scene Planner Algorithm

```python
class ScenePlanner:
    """
    Converts a Script's scene_breakdown into a complete video composition plan.
    
    Steps:
    1. Parse scene_breakdown JSON from Script
    2. For each scene:
       a. Assign background media (image/video)
       b. Apply Ken Burns parameters based on duration
       c. Layout text overlays (hook, CTA, statistics)
       d. Assign audio segments (voiceover + music)
    3. Calculate global timings:
       - Scene start/end times
       - Caption synchronization points
       - Transition placement
    4. Validate total duration matches target (±0.5s)
    5. Return CompositionPlan JSON
    
    Duration calculation:
    - Each scene: background_duration = scene_duration
    - Transition: overlaps scenes by transition_duration
    - Total = sum(scene_durations) - sum(transition_overlaps)
    """
    
    def plan(self, script: Script, images: list[Image], 
             voiceover: Voiceover, captions: Subtitles,
             style: StylePreset) -> CompositionPlan:
        """
        1. Verify asset count matches scene count
        2. Assign each image to its scene_index
        3. Calculate Ken Burns parameters per scene
           - Longer scenes: more dramatic zoom
           - Shorter scenes: subtle motion
        4. Layout text overlays with safe-zone calculations
        5. Map voiceover segments to scenes
        6. Generate caption timing
        7. Return validated CompositionPlan
        """
```

---

## 3. Audio Processing Pipeline

### 3.1 Audio Mixer

```python
# backend/media/audio/mixer.py

class AudioMixer:
    """
    Multi-track audio mixer for Shorts videos.
    
    Tracks:
    1. Voiceover (TTS) — Primary track, center panned
    2. Background Music — Stereo, volume ducked during speech
    3. Sound Effects — Optional, for emphasis moments
    
    Ducking Strategy:
    - When voiceover is active: reduce BGM volume by 60-80%
    - When voiceover is silent: restore BGM to full volume
    - Ducking attack: 50ms (fast)
    - Ducking release: 200ms (smooth)
    
    Processing Steps:
    1. Normalize voiceover volume to -3dB peak
    2. Apply compressor to voiceover (threshold: -12dB, ratio: 3:1)
    3. Apply EQ to voiceover (high-pass at 80Hz, gentle presence boost at 3kHz)
    4. Apply side-chain compression to BGM using voiceover as trigger
    5. Mix tracks together
    6. Apply limiter (ceiling: -1dB, lookahead: 5ms)
    7. Encode to target format
    """
    
    def mix(self, voiceover_path: str, music_path: str = None,
            sfx_paths: list[str] = None, 
            settings: AudioMixSettings = None) -> str:
        """
        Returns: Path to mixed audio file
        """
```

### 3.2 Audio Processing Graph

```
Voiceover Track:
  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  Normalize│─▶│ Compress │─▶│   EQ     │─▶│  Gate    │
  │  -3dB peak│  │  3:1     │  │ HP+Pres  │  │  Noise   │
  └──────────┘  └──────────┘  └──────────┘  └──────────┘
                          │
                          ▼
Background Music:
  ┌──────────┐  ┌──────────┐  ┌──────────┐
  │  Fade In │─▶│ Duck     │─▶│  Fade Out│
  │  500ms   │  │ 60-80%   │  │  500ms   │
  └──────────┘  └──────────┘  └──────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │  Audio Mixer   │
                 │  (FFmpeg amix) │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │   Limiter      │
                 │  -1dB ceiling  │
                 └───────┬────────┘
                         │
                         ▼
                 ┌────────────────┐
                 │  Encode        │
                 │  AAC 192kbps   │
                 └────────────────┘
```

### 3.3 Silence Insertion

```python
class SilenceInserter:
    """
    Inserts strategic pauses into voiceover audio for dramatic effect.
    
    When to insert silence:
    - After hook (500-1000ms pause)
    - Before key statistic (300-500ms pause)
    - Between major sections (200-300ms pause)
    - Before CTA (500ms pause)
    
    Rules:
    - Never insert silence mid-sentence
    - Total added silence should not exceed 15% of total duration
    - Pause durations are proportional to video length
      (30s video: shorter pauses; 60s: longer)
    """
    
    def insert_pauses(self, audio_path: str, 
                      pause_points: list[PausePoint]) -> str:
        """
        Uses FFmpeg's adelay + concat to insert silences
        at specified timestamps.
        """
```

---

## 4. Subtitle / Caption Pipeline

### 4.1 Pipeline Overview

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Audio File   │───▶│  Whisper         │───▶│  Word-Level      │
│               │    │  Transcription   │    │  Timestamps      │
└──────────────┘    └──────────────────┘    └──────────────────┘
                                                     │
                                                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Burn-in     │◄───│  SRT/ASS Format  │◄───│  Text Alignment  │
│  (drawtext)  │    │  + Styling       │    │  with Script     │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

### 4.2 Whisper Transcription

```python
# backend/media/subtitles/transcriber.py

class WhisperTranscriber:
    """
    Transcribes audio using OpenAI Whisper with word-level timestamps.
    
    Model: large-v3 (best accuracy)
    
    Steps:
    1. Load audio file
    2. Pad to 30s chunks (Whisper requirement)
    3. Run inference (GPU optional, ~2x real-time on RTX 4090)
    4. Merge overlapping segments
    5. Align text with original script text for accuracy
    6. Generate word-level timestamps
    
    Output format (per word):
    [
      {"word": "Hello", "start_ms": 0, "end_ms": 300, "confidence": 0.98},
      {"word": "world", "start_ms": 310, "end_ms": 550, "confidence": 0.95}
    ]
    
    Alignment with script:
    - Use the generated script text as ground truth
    - Whisper output may have slight variations
    - Algorithm: dynamic time warping between Whisper words and script words
    - Result: corrected word timestamps matching script text exactly
    """
    
    MODEL_SIZES = {
        "tiny": {"speed": "10x", "accuracy": "fair"},
        "base": {"speed": "7x", "accuracy": "good"},
        "small": {"speed": "4x", "accuracy": "very good"},
        "medium": {"speed": "2x", "accuracy": "excellent"},
        "large-v3": {"speed": "1x", "accuracy": "best"},
    }
    
    def transcribe(self, audio_path: str, language: str = "en") -> TranscriptionResult:
        ...
```

### 4.3 SRT/ASS Generation

```python
class SubtitleFormatter:
    """
    Converts word timestamps to SRT or ASS format.
    
    SRT (Simple):
    1
    00:00:01,000 --> 00:00:03,500
    Hello world, this is a caption
    
    ASS (Advanced - used for word-level highlighting):
    Dialogue: 0,0:00:01.00,0:00:01.15,Default,,0,0,0,,{\\k10}Hel{\\k5}lo
    Dialogue: 0,0:00:01.15,0:00:02.50,Default,,0,0,0,,{\\k30}world
    
    ASS Features:
    - Word-by-word highlight via \\k (karaoke) timing
    - Font, color, position control
    - Shadow/outline for readability
    - Multi-language support (Unicode)
    
    For burn-in, we generate intermediate ASS format
    then use FFmpeg's ass filter (faster than drawtext for complex captions)
    """
    
    STYLE_TEMPLATE = """
    [Script Info]
    ScriptType: v4.00+
    PlayResX: 1080
    PlayResY: 1920
    
    [V4+ Styles]
    Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour,
            OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline,
            Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    Style: Default,{font},{font_size},&H{color},&H{highlight_color},
           &H{outline_color},&H{background_color},0,0,1,{outline_width},
           {shadow_width},{alignment},30,30,{margin_v},1
    """
```

### 4.4 Burn-in Strategies

| Strategy | Method | Quality | Speed | Flexibility |
|----------|--------|---------|-------|-------------|
| **ASS Filter** | `ffmpeg -vf ass=captions.ass` | Best | Fast | High |
| **Drawtext** | `ffmpeg -vf drawtext=text='...'` | Good | Slow | Medium |
| **SRT Burn** | `ffmpeg -vf subtitles=captions.srt` | Good | Fast | Low |
| **Client-side** | React overlay on video element | Best | N/A | Highest |

**Recommendation**: Use ASS filter for production (fastest burn-in with word highlighting). Offer client-side rendering as alternative for users who want to customize captions.

### 4.5 Word-by-Word Highlight

```
Frame 1 (t=1.00): "Hello" is highlighted (yellow), rest dimmed
  ┌──────────────────────────────────┐
  │                                  │
  │   Hello world, this is a         │
  │   caption for this video.        │
  │   ^^^^^ (highlighted)            │
  │                                  │
  └──────────────────────────────────┘

Frame 2 (t=1.15): "world" is highlighted
  ┌──────────────────────────────────┐
  │                                  │
  │   Hello world, this is a         │
  │   caption for this video.        │
  │         ^^^^^ (highlighted)      │
  │                                  │
  └──────────────────────────────────┘
```

Implementation via ASS karaoke timing:
- Each word is wrapped in `{\\k<duration in centiseconds>}` tag
- The highlighting advances word-by-word as the video plays
- Highlight color is controlled by `SecondaryColour` in ASS style
- The transition between words is instantaneous (snap) or smooth (fade)

---

## 5. Thumbnail Generation

### 5.1 Thumbnail Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Thumbnail Pipeline                                                         │
│                                                                              │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐          │
│  │  Extract      │───▶│  Frame           │───▶│  Overlay Text    │          │
│  │  Best Frame   │    │  Enhancement     │    │  + Graphics      │          │
│  └──────────────┘    └──────────────────┘    └──────────────────┘          │
│                            │                       │                        │
│                            ▼                       ▼                        │
│  ┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐          │
│  │  AI Generate  │───▶│  A/B Variants    │───▶│  Encode & Upload│          │
│  │  (Alternative)│    │  (3 options)     │    │  to S3           │          │
│  └──────────────┘    └──────────────────┘    └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Thumbnail Strategies

| Strategy | Method | Quality | Speed | When to Use |
|----------|--------|---------|-------|-------------|
| **Frame Extraction** | FFmpeg extract at 25% position | Good | Instant | Default |
| **AI Generation** | SD/FLUX with title overlay | Excellent | 15s | If frame is boring |
| **Template-based** | Pre-designed template + text | Good | 1s | Brand consistency |
| **Hybrid** | Extract frame + AI enhance | Very Good | 5s | Best balance |

### 5.3 Thumbnail Specs

| Property | Value |
|----------|-------|
| **Resolution** | 1280×720 (16:9, YouTube standard) |
| **Format** | JPEG (quality: 90) |
| **File Size** | < 2MB |
| **Text Overlay** | Max 3 words, bold, high contrast |
| **Safe Area** | Center 80% (text/CTAs inside) |
| **Branding** | Channel logo in bottom-right (100×100px) |

---

## 6. FFmpeg GPU Acceleration

### 6.1 Hardware Acceleration Matrix

| Operation | CPU (libx264) | GPU (NVENC) | GPU (AMF) | GPU (QSV) |
|-----------|---------------|-------------|-----------|-----------|
| **H.264 Encode** | 1x (baseline) | 8x | 7x | 6x |
| **H.265/HEVC Encode** | 0.5x | 6x | 5x | 4x |
| **Scale** | 1x | 15x | 12x | 10x |
| **Overlay** | 1x | 10x | 8x | 7x |
| **Drawtext** | 1x | 0.5x | 0.5x | 0.5x |
| **Ass Filter** | 1x | 1x | 1x | 1x |
| **Zoompan** | 1x | 0.3x | 0.3x | 0.3x |

**Key Insight**: Some filters DON'T benefit from GPU (drawtext, ass, zoompan). The optimal pipeline runs these on CPU while using GPU for encode/scale/overlay.

### 6.2 Optimized Filter Chain

```python
# The optimal pipeline for a Shorts video:

# Step 1: CPU - Generate animated clip from image (zoompan)
# Step 2: GPU - Overlay text with drawtext (slightly slower on GPU, but 
#               saves a copy to/from GPU memory for the next step)
# Step 3: GPU - Scale to output resolution
# Step 4: GPU - Encode with NVENC

# Why not GPU for zoompan?
# GPU zoompan (scale_cuda + interlace) produces lower quality
# CPU zoompan produces better results and is fast enough for 30fps

ffmpeg_command = [
    "ffmpeg",
    "-y",
    # Input: background image
    "-i", image_path,
    # Input: captions ASS file
    "-i", captions_path,
    # Complex filter
    "-filter_complex", """
        [0:v]
        zoompan=
          z='min(zoom+0.0015,1.15)':
          d=150:
          fps=30:
          s=1080x1920[zoomed];
        [zoomed]
        ass=
          filename=captions.ass:
          original_size=1080x1920[ass_out];
        [ass_out]
        format=nv12,
        hwupload_cuda[hw]
    """,
    # Hardware encoding
    "-c:v", "h264_nvenc",
    "-preset", "p7",
    "-profile:v", "high",
    "-rc", "vbr",
    "-b:v", "12M",
    "-maxrate", "15M",
    "-bufsize", "20M",
    # Audio
    "-i", audio_path,
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_path
]
```

### 6.3 NVENC Encoding Parameters

| Setting | Draft | Standard | High |
|---------|-------|----------|------|
| **Preset** | p1 (fastest) | p4 (balanced) | p7 (quality) |
| **Bitrate** | 4M | 12M | 20M |
| **Max Bitrate** | 6M | 15M | 25M |
| **Profile** | main | high | high |
| **B-frames** | 0 | 2 | 4 |
| **RC Mode** | cbr | vbr | vbr |
| **Lookahead** | 0 | 16 | 32 |
| **Time per 30s video** | ~5s | ~15s | ~30s |

### 6.4 GPU Memory Budget

| Operation | VRAM Usage (1080p) |
|-----------|-------------------|
| H.264 Encoding Session | 150-200 MB |
| H.265 Encoding Session | 200-300 MB |
| Scale (CUDA) | 100 MB |
| Overlay (CUDA) | 100 MB |
| Frame Buffer (30fps, 1080p) | 200 MB |
| **Total per encode session** | **~800 MB** |

**Concurrent sessions on a 24GB GPU**: ~28 simultaneous encodes  
**Safety limit**: 20 concurrent sessions (leave headroom for OS + other processes)

---

## 7. Output Specifications

### 7.1 Video Specs

| Property | Value |
|----------|-------|
| **Resolution** | 1080×1920 (9:16 portrait) |
| **Aspect Ratio** | 9:16 |
| **Frame Rate** | 30 fps |
| **Video Codec** | H.264 (primary) / H.265 (optional) |
| **Video Bitrate** | 12 Mbps (1080p) |
| **Audio Codec** | AAC |
| **Audio Bitrate** | 192 kbps |
| **Audio Sample Rate** | 48 kHz |
| **Audio Channels** | Stereo |
| **Container** | MP4 (ISO 14496-12) |
| **Color Space** | BT.709 |
| **Pixel Format** | yuv420p |
| **Color Range** | tv (limited) |

### 7.2 YouTube Shorts Requirements

| Requirement | YouTube Standard | Our Output |
|-------------|-----------------|------------|
| **Aspect Ratio** | 9:16 (vertical) | 9:16 ✓ |
| **Resolution** | 1080×1920 max | 1080×1920 ✓ |
| **Duration** | 15-60 seconds | 15-180 ✓ |
| **Frame Rate** | 30 or 60 fps | 30 fps ✓ |
| **Audio Codec** | AAC or MP3 | AAC ✓ |
| **File Size** | < 256 GB | ~45 MB (30s) ✓ |
| **Container** | MP4, MOV, AVI | MP4 ✓ |

### 7.3 File Size Estimates

| Duration | Draft (4Mbps) | Standard (12Mbps) | High (20Mbps) |
|----------|--------------|-------------------|---------------|
| 15 sec | ~7.5 MB | ~22.5 MB | ~37.5 MB |
| 30 sec | ~15 MB | ~45 MB | ~75 MB |
| 60 sec | ~30 MB | ~90 MB | ~150 MB |
| 180 sec | ~90 MB | ~270 MB | ~450 MB |

---

## 8. Error Handling & Retry

### 8.1 Failure Modes

| Failure | Symptom | Detection | Recovery |
|---------|---------|-----------|----------|
| **Missing asset** | FFmpeg "No such file" | Pre-flight check | Skip scene, use fallback |
| **Corrupt image** | FFmpeg "Invalid data" | Image validation | Regenerate image |
| **Corrupt audio** | FFmpeg "Invalid audio" | Audio validation | Regenerate TTS |
| **GPU OOM** | FFmpeg "CUDA OOM" | Monitor VRAM | Retry with CPU fallback |
| **GPU hang** | Process timeout | Watchdog timer | Kill process, retry |
| **Disk full** | Write error | Disk check | Clean temp, retry |
| **FFmpeg crash** | Non-zero exit | Exit code check | Retry up to 2x |

### 8.2 Pre-flight Checks

```python
class RenderValidator:
    """
    Validates all assets before starting the render.
    Catches issues early to avoid wasting GPU time.
    """
    
    def validate(self, plan: CompositionPlan) -> ValidationResult:
        checks = []
        
        # 1. File existence
        for scene in plan.scenes:
            checks.append(self._check_file(scene.background.source))
            if scene.audio.voiceover:
                checks.append(self._check_file(scene.audio.voiceover.source))
        
        # 2. Image dimensions
        for scene in plan.scenes:
            if scene.background.type == "image":
                checks.append(self._check_image_dimensions(
                    scene.background.source, 1080, 1920))
        
        # 3. Audio duration match
        total_audio_ms = self._get_total_audio_duration(plan)
        expected_ms = plan.total_duration_sec * 1000
        checks.append(abs(total_audio_ms - expected_ms) < 500)
        
        # 4. Caption timing bounds
        checks.append(self._validate_caption_timing(plan.captions, plan.total_duration_sec))
        
        # 5. Disk space
        required_space = self._estimate_output_size(plan) * 2  # ×2 for temp files
        checks.append(self._check_disk_space(required_space))
        
        # 6. GPU availability
        checks.append(self._check_gpu_available())
        
        return ValidationResult(all(checks), [c for c in checks if not c.passed])
```

### 8.3 Progress Monitoring

```python
class RenderProgressMonitor:
    """
    Monitors FFmpeg progress by parsing stderr output.
    
    FFmpeg outputs lines like:
    frame=  120 fps=30 q=28.0 size=    5120kB time=00:00:04.00
    
    We parse:
    - frame: current frame number
    - fps: current encoding speed
    - q: quality factor
    - size: output file size
    - time: current encoded duration
    
    Progress % = (current_time / total_duration) * 100
    
    Updates DB record every 5% progress change.
    Sends WebSocket event to frontend.
    """
    
    def parse_progress(self, line: str) -> ProgressUpdate | None:
        pattern = r"frame=\s*(\d+)\s+fps=\s*([\d.]+)\s+.*time=(\d+:\d+:\d+\.\d+)"
        match = re.search(pattern, line)
        if match:
            current_time = self._parse_time(match.group(3))
            progress = (current_time / self.total_duration) * 100
            return ProgressUpdate(
                frame=int(match.group(1)),
                fps=float(match.group(2)),
                current_time=current_time,
                progress_pct=min(progress, 99)  # Leave 100% for completion
            )
        return None
```

### 8.4 Fallback Strategy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Quality Tier Fallback                                                      │
│                                                                              │
│  User selects: "High Quality"                                               │
│                                                                              │
│  Attempt 1: High Quality                                                    │
│  ├─ FLUX Pro (image gen)                                                    │
│  ├─ Real-ESRGAN 4x (upscale)                                                │
│  ├─ NVENC preset p7 (encode)                                                │
│  └─ Failed? → Attempt 2                                                     │
│                                                                              │
│  Attempt 2: Standard Quality                                                │
│  ├─ Stable Diffusion 3.5 (image gen)                                        │
│  ├─ Real-ESRGAN 2x (upscale)                                                │
│  ├─ NVENC preset p4 (encode)                                                │
│  └─ Failed? → Attempt 3                                                     │
│                                                                              │
│  Attempt 3: Draft Quality                                                   │
│  ├─ SDXL Turbo (image gen, 4 steps)                                         │
│  ├─ No upscale                                                              │
│  ├─ CPU encode (libx264 ultrafast)                                          │
│  └─ Failed? → Mark pipeline as failed with error details                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Performance Benchmarks

### 9.1 Render Times (30-second Short)

| GPU | Resolution | Quality | Time | Speed Factor |
|-----|-----------|---------|------|-------------|
| **CPU** (AMD 7950X) | 1080p | Draft | 45s | 0.67x |
| **CPU** (AMD 7950X) | 1080p | Standard | 180s | 0.17x |
| **RTX 3060** | 1080p | Draft | 8s | 3.75x |
| **RTX 3060** | 1080p | Standard | 25s | 1.2x |
| **RTX 4070** | 1080p | Draft | 5s | 6x |
| **RTX 4070** | 1080p | Standard | 15s | 2x |
| **RTX 4090** | 1080p | Draft | 3s | 10x |
| **RTX 4090** | 1080p | Standard | 10s | 3x |
| **RTX 4090** | 1080p | High | 20s | 1.5x |

### 9.2 Full Pipeline Times (60-second video)

| Stage | GPU | Draft | Standard | High |
|-------|-----|-------|----------|------|
| Script Gen | N/A | 8s | 8s | 10s |
| Image Gen (5 images) | RTX 4090 | 5s | 50s | 150s |
| TTS (60s audio) | N/A | 3s | 3s | 3s |
| Caption/Whisper | RTX 4090 | 10s | 10s | 10s |
| Video Render | RTX 4090 | 5s | 15s | 30s |
| **Total** | | **~31s** | **~86s** | **~203s** |

### 9.3 Bottleneck Analysis

```
60-second video, Standard quality, RTX 4090:

Total: ~86 seconds

Breakdown:
  ████████████████░░░░░░░░░░░░░░░░░░░░  Script Gen (8s, 9%)
  █████████████████████████████████████  Image Gen (50s, 58%)  ← BOTTLENECK
  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  TTS (3s, 3%)
  ██████████████████░░░░░░░░░░░░░░░░░░  Whisper (10s, 12%)
  ████████████████████████████░░░░░░░░  Video Render (15s, 17%)

Optimization targets:
1. Image generation: 58% of total time
   → Batch generation (all images in parallel)
   → Reduce steps for interior scenes (30→20)
   → Use SDXL Turbo for preview, full model only for final
2. Whisper: 12% of total time
   → Already GPU accelerated
   → Could use medium model instead of large-v3 (2x faster, slightly less accurate)
```

---

## Appendix: Key Interfaces

```python
# backend/application/interfaces/video_pipeline.py

class IVideoPipeline(ABC):
    """Port interface for the video composition pipeline."""
    
    @abstractmethod
    async def compose(self, plan: CompositionPlan) -> VideoResult:
        """Execute the full video composition pipeline."""
        ...
    
    @abstractmethod
    async def render_scene(self, scene: Scene, settings: RenderSettings) -> str:
        """Render a single scene to a video clip."""
        ...
    
    @abstractmethod
    async def merge_audio(self, voiceover: str, music: str = None) -> str:
        """Merge and mix audio tracks."""
        ...


class CompositionPlan(BaseModel):
    """Complete plan for video composition."""
    scenes: list[Scene]
    captions: CaptionConfig
    transitions: list[Transition]
    output: OutputConfig
    total_duration_sec: float


class RenderSettings(BaseModel):
    quality: Literal["draft", "standard", "high"] = "standard"
    gpu_device: int = 0
    temp_dir: str = "./temp"
    preserve_temp: bool = False


class VideoResult(BaseModel):
    video_id: UUID
    file_path: str
    thumbnail_path: str | None
    duration_sec: float
    file_size_bytes: int
    render_time_sec: float
    quality_tier_used: str
    warnings: list[str]