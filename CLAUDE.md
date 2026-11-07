# AI-GCM

**Kaatclip** (working name GCM Clipper): AI that turns long BGMI livestreams into ranked, captioned 9:16 clips for Indian gaming creators. The engine is in `ai-gcm/aigcm/` (see `ai-gcm/README.md` and `ai-gcm/TEST_RESULTS.md`); the platform built in M2 is the API (`ai-gcm/aigcm/api/`), the worker (`ai-gcm/aigcm/worker.py`) and the React web app (`ai-gcm/web/`). Detection work is tracked in `ai-gcm/ANALYSIS_NOTES.md`; the old PWA (`PWA_NOTES.md`) is retired. The full app is now being built from `plans/GCM Clipper master plan.md` (the single plan: features, milestones, owner tasks, risks); its progress is in `ai-gcm/BUILD_NOTES.md` and its technical setup in `docs/ARCHITECTURE.md`.

## Working in two places

The owner works from two Claude Code sessions, never at the same time, and GitHub (`sourabh0333/gcm-clipper`, branch `main`) is how they share work:

- **Laptop** (Windows, `C:\Users\green\Sourabh\My All Projects\Content-Management`): the full pipeline and the live app run here. Python venv in `ai-gcm/.venv`, ffmpeg in `C:\ffmpeg\bin`, test streams and rendered clips in `ai-gcm/jobs/`, the database in `ai-gcm/data/` (neither in git). `ai-gcm/Start Kaatclip.cmd` starts the API and web app (port 8770) and the worker; the owner reaches it from the phone at the Tailscale Funnel address in `.env` (`AIGCM_PUBLIC_URL`), signed in with Google. Restart them after changing platform code, and run `npm run build` in `ai-gcm/web` after changing the web app.
- **Phone** (a cloud session on the GitHub repo): code only. There are no test streams, and the pipeline's models may not be installed; install `ai-gcm/requirements-api.txt` for the platform. Check screens against the demo jobs: copy `ai-gcm/demo/` to a scratch folder, then from `ai-gcm/` run `python -m aigcm.manage import-jobs --owner dev@example.com` and `python -m aigcm.api` with `AIGCM_JOBS_DIR=<copy>`, `AIGCM_DB_URL=sqlite:///<scratch>/dev.db`, `AIGCM_DEV_LOGIN=1` and `AIGCM_INVITES=dev@example.com`, after building the web app (`cd ai-gcm/web && npm install && npm run build`). Rebuild the demo jobs with `python make_demo.py`.

**At the start of every session:** pull `main`, then read `ai-gcm/BUILD_NOTES.md` (and `ANALYSIS_NOTES.md` for background) and carry on from its "Next" list.

**Before stopping, or when the owner says they are switching:** update the notes file for the work you did (what was done, what is next, decisions, anything not finished or not tested), run the tests (`python -m pytest` in `ai-gcm/`, and `npm test` in `ai-gcm/web/` if the web app changed), then commit and push to `main`. If this environment can only push to another branch, push that branch and write its name at the top of the notes, so the other session merges it into `main` first.

## Owner preferences

- Spend nothing until the product proves itself: free tools, free tiers and the owner's own laptop only.
- The owner wants Claude to handle code, git and setup without asking them to do manual steps.
- Keep replies short and plain; the owner writes in English and Hinglish.

## Rules for the repo

- Never commit `ai-gcm/jobs/`, `ai-gcm/data/`, `.env`, `web/node_modules`, `web/dist`, downloaded streams or real streamers' footage. Demo clips are generated placeholders. The GitHub repo is public: never put a key, token or secret in any committed file.
- Commits end with the Co-Authored-By line the session is given.
