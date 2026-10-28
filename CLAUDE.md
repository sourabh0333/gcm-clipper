# AI-GCM

AI that turns long BGMI livestreams into ranked, captioned 9:16 clips for Indian gaming creators. The Python prototype is in `ai-gcm/` (see `ai-gcm/README.md` and `ai-gcm/TEST_RESULTS.md`). The next step is a PWA on top of it; progress is tracked in `ai-gcm/PWA_NOTES.md`.

## Working in two places

The owner works from two Claude Code sessions, never at the same time, and GitHub (`sourabh0333/gcm-clipper`, branch `main`) is how they share work:

- **Laptop** (Windows, `C:\Users\green\Sourabh\My All Projects\Content-Management`): the full pipeline runs here. Python venv in `ai-gcm/.venv`, ffmpeg in `C:\ffmpeg\bin`, test streams and rendered clips in `ai-gcm/jobs/` (not in git).
- **Phone** (a cloud session on the GitHub repo): code only. There are no test streams, and the pipeline's models may not be installed. Build and check screens against the demo jobs in `ai-gcm/demo/` instead (set `AIGCM_JOBS_DIR=demo`; rebuild them with `python make_demo.py` from `ai-gcm/`).

**At the start of every session:** pull `main`, then read `ai-gcm/PWA_NOTES.md` and carry on from its "Next" list.

**Before stopping, or when the owner says they are switching:** update `ai-gcm/PWA_NOTES.md` (what was done, what is next, decisions, anything not finished or not tested), run the tests (`python -m pytest` in `ai-gcm/`), then commit and push to `main`. If this environment can only push to another branch, push that branch and write its name at the top of the notes, so the other session merges it into `main` first.

## Owner preferences

- Spend nothing until the product proves itself: free tools, free tiers and the owner's own laptop only.
- The owner wants Claude to handle code, git and setup without asking them to do manual steps.
- Keep replies short and plain; the owner writes in English and Hinglish.

## Rules for the repo

- Never commit `ai-gcm/jobs/`, `.env`, downloaded streams or real streamers' footage. Demo clips are generated placeholders.
- Commits end with the Co-Authored-By line the session is given.
