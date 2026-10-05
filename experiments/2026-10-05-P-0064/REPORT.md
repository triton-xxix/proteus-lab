# P-0064, mesh-avatar-studio: does the sample install, load and lip-sync with no keys?

Ran 5 Oct 2026. Repo fetched as a tarball by `sandbox/mesh-avatar/fetch.py` (git clone and npm are
off the unattended safe list). Inspection output in `sandbox/mesh-avatar/inspect.json`.

What I could measure without installing:
- 19.8 MB tarball, 167 files, lockfile present. Two runtime dependencies (react, react-dom), 14 dev
  dependencies (vite 7, vitest, playwright, typescript, pngjs).
- The sample avatar is bundled: `samples/miko-qipao/` with rig.json, the source image, built layers
  and seven mouth and eye variant images.
- No key, no outbound fetch, no TTS vendor in the source: a grep for API_KEY, apiKey, openai,
  elevenlabs and fetch("http found nothing.
- The lip-sync is honest about what it is (`src/engine/motion.js`): from audio it reads loudness
  only, finds syllables as dips relative to the recent peak, and gives each syllable a random vowel
  weighted to "a" (40 percent). Proper mouth shapes come only from Japanese kana text.

What I could not do: `npm install` and `npm run dev`, so whether it loads and animates in a browser
is not measured. Blocked on an interactive session with npm, about 10 minutes.
