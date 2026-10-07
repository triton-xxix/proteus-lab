# P-0071: scene-change frames from ffmpeg, lined up with captions

Run 7 Oct 2026, interactive probe loop. The question came from H-0155 (feeding a video to an agent
as scene-change frames plus transcript): at threshold 0.3, how many frames does ffmpeg give on a
public 10-minute video, and do they line up with the captions?

YouTube refused downloads from this Mac tonight (403, see P-0068), so the video is *Tears of Steel*
(Blender Foundation, CC-BY 3.0, mango.blender.org): 12 min 14 s, 1280x534, 24 fps, with the
official English subtitles `TOS-en.srt` (76 cues).

## Numbers

- Scene detection over the whole film (`select='gt(scene,0.3)'`): 136 frames in 13.6 s wall, about
  54x real time on the Intel i7.
- Every frame's score logged once, then thresholds compared:

| Threshold | Frames | One frame per |
|---|---|---|
| 0.2 | 157 | 4.7 s |
| 0.3 | 136 | 5.4 s |
| 0.4 | 105 | 7.0 s |
| 0.5 | 53 | 13.9 s |

- Lining up: each subtitle cue gets the most recent cut before it starts. The 76 cues use 55 of the
  137 shots; 70 shots carry no dialogue at all; 24 cues span a cut, so a single frame per cue
  misses a change of shot about a third of the time.
- `contact-sheet-0.3.jpg` shows all 136 frames; two are near-black fades, the rest are distinct shots.

## Verdict

Works, and cheap. For an agent, "frames plus transcript" at 0.3 on a fast-cut film is about 55
frames if you keep only the ones a caption points at, or 136 if you keep every shot. A screen
recording or a talking head will cut far less, so 0.3 with a cap is a sensible default. Worth
adding to the transcript step for videos where the screen matters, not for talking heads.

Files: `cuts-0.3.txt` (cut times in seconds), `aligned.json` (cue, frame, cuts inside the cue),
`contact-sheet-0.3.jpg`, `TOS-en.srt`. The film itself stays in `sandbox/scene/` (372 MB, gitignored).
