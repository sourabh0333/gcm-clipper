# Bundled assets

Free to redistribute; each keeps its licence file next to it.

| Folder | What | Source | Licence |
|---|---|---|---|
| `fonts/Anton-Regular.ttf` | Hook text (Latin): heavy condensed caps | github.com/google/fonts, `ofl/anton` | SIL Open Font License 1.1 (`OFL-Anton.txt`) |
| `fonts/Mukta-ExtraBold.ttf` | Hindi hooks and all captions (Latin and Devanagari) | github.com/google/fonts, `ofl/mukta` | SIL Open Font License 1.1 (`OFL-Mukta.txt`) |
| `emoji/<codepoint>.png` | 63 colour emoji (128 px) the hook can draw | github.com/googlefonts/noto-emoji, `2D/png/128` | Noto Emoji's licence (`LICENSE-noto-emoji.txt`; the README there names Apache 2.0 for the images) |

Used by `aigcm/studio/hook.py` (hook images) and `aigcm/studio/render.py` (captions); the web app loads the caption font from `/fonts/` for the editor's preview. To add an emoji, download its `emoji_u<codepoint>.png` from the same folder, save it here as `<codepoint>.png`, and add it to the editor's `EMOJI` list.
