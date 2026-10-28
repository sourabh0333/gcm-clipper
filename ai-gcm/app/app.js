// GCM Clipper: start a job from a YouTube link, watch it run, swipe through the clips, keep, download, share.
// Plain modules with no build step; the server is aigcm/server.py.

const app = document.getElementById("app");
const STAGE_NAMES = {
  ingest: "Download video", vision: "Read kills from the HUD", audio: "Measure audio",
  sounds: "Listen for laughs and gunfire", moments: "Find moments",
  judge: "Rank moments", captions: "Write captions", render: "Make 9:16 clips", review: "Finish",
};
const TYPE_NAMES = { multi_kill: "Multi kill", fight: "Fight", win: "Chicken dinner", reaction: "Reaction" };
const STATE_NAMES = { done: "Ready", running: "Processing", stopped: "Stopped", failed: "Failed" };
const ICON = {
  keep: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  reject: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  undo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 14L4 9l5-5"/><path d="M4 9h10a6 6 0 010 12h-3"/></svg>',
  soundOn: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 010 7M19 6a8.5 8.5 0 010 12"/></svg>',
  soundOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>',
};

let poll = null;
let muted = true;

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const clipUrl = (job, clip, download = false) =>
  `/media/${encodeURIComponent(job)}/${encodeURIComponent(clip.file)}${download ? "?download=1" : ""}`;

function clock(seconds) {
  seconds = Math.max(0, Math.round(seconds || 0));
  const h = Math.floor(seconds / 3600), m = Math.floor(seconds / 60) % 60, s = seconds % 60;
  return h ? `${h}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}` : `${m}:${String(s).padStart(2, "0")}`;
}

function took(seconds) {
  if (seconds == null) return "";
  if (seconds < 60) return `${Math.round(seconds)} s`;
  return `${Math.round(seconds / 60)} min`;
}

function toast(message) {
  const el = document.getElementById("toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), 3500);
}

async function api(path, body) {
  const res = await fetch(path, body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `The laptop answered ${res.status}.`);
  return data;
}

function every(ms, fn) {
  clearInterval(poll);
  poll = setInterval(fn, ms);
}

function chip(state) {
  return `<span class="chip ${state}">${STATE_NAMES[state] || state}</span>`;
}

function sectionText(section) {
  return section ? `${clock(section[0])}–${clock(section[1])}` : "Whole video";
}

// ---------- Home: new job and the job list ----------

async function home() {
  document.title = "GCM Clipper";
  app.innerHTML = `
    <header class="bar"><h1 class="logo"><span aria-hidden="true">GC</span>GCM Clipper</h1></header>
    <main class="page">
      <form class="panel" id="new" novalidate>
        <h2>New job</h2>
        <label>YouTube link
          <input name="url" type="url" inputmode="url" autocomplete="off" placeholder="https://www.youtube.com/watch?v=…" required>
        </label>
        <details>
          <summary>Only part of the video</summary>
          <div class="row">
            <label>From<input name="from" inputmode="numeric" placeholder="0:30:00"></label>
            <label>To<input name="to" inputmode="numeric" placeholder="1:30:00"></label>
          </div>
        </details>
        <p class="hint">30 minutes of stream takes about 30–45 minutes on the laptop. You can close this page; the laptop keeps working.</p>
        <p class="error" id="new-error"></p>
        <button class="btn primary" type="submit">Start</button>
      </form>
      <section>
        <div class="section-head"><h2>Jobs</h2></div>
        <ul class="jobs" id="jobs"><li class="empty">Loading…</li></ul>
      </section>
    </main>`;

  const form = document.getElementById("new");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const error = document.getElementById("new-error");
    const url = form.url.value.trim();
    const from = form.from.value.trim(), to = form.to.value.trim();
    error.textContent = "";
    if (!url) return (error.textContent = "Paste a YouTube link first.");
    if (!!from !== !!to) return (error.textContent = "Fill in both From and To, or leave both empty.");
    const button = form.querySelector("button");
    button.disabled = true;
    try {
      const job = await api("/api/jobs", { url, section: from ? `${from}-${to}` : "" });
      location.hash = `#/job/${encodeURIComponent(job.name)}`;
    } catch (err) {
      error.textContent = err.message;
      button.disabled = false;
    }
  });

  const load = async () => {
    try {
      const jobs = await api("/api/jobs");
      const list = document.getElementById("jobs");
      if (!list) return;
      list.innerHTML = jobs.length ? jobs.map(jobCard).join("") : '<li class="empty">No jobs yet. Paste a link above to make your first clips.</li>';
    } catch (err) {
      toast("Can't reach the laptop. Is the app running there?");
    }
  };
  await load();
  every(4000, load);
}

function jobCard(job) {
  const done = job.state === "done";
  const detail = done
    ? `${job.clips} clips${job.reviewed ? ` · ${job.kept} kept` : " · not reviewed"}`
    : job.state === "running" ? `${Math.round(job.progress * 100)}%` : job.state === "failed" ? "Tap to see what went wrong" : "Tap to resume";
  return `<li><a class="job" href="#/job/${encodeURIComponent(job.name)}">
      <h3>${esc(job.title)}</h3>
      <div class="meta">${chip(job.state)}${job.channel ? `<span>${esc(job.channel)}</span>` : ""}<span>${sectionText(job.section)}</span><span>${detail}</span></div>
      ${done ? "" : `<div class="progress" aria-hidden="true"><i style="width:${job.progress * 100}%"></i></div>`}
    </a></li>`;
}

// ---------- Job: progress while it runs, kept clips when done ----------

async function jobPage(name) {
  app.innerHTML = `<header class="bar"><a class="back" href="#/">← Jobs</a></header><main class="page" id="job"><p class="empty">Loading…</p></main>`;
  let lastState = null;

  const load = async () => {
    let job;
    try {
      job = await api(`/api/jobs/${encodeURIComponent(name)}`);
    } catch (err) {
      return toast(err.message);
    }
    const main = document.getElementById("job");
    if (!main) return;
    document.title = `${job.title} · GCM Clipper`;
    // Don't rebuild a finished job's page on every poll: it would restart the videos.
    if (job.state === "done" && lastState === "done") return;
    lastState = job.state;
    main.innerHTML = header(job) + (job.state === "done" ? finished(job) : progress(job));
    bindJob(job);
    if (job.state === "done") clearInterval(poll);
  };
  await load();
  every(3000, load);
}

function header(job) {
  const source = job.source ? `<a href="${esc(job.source)}" target="_blank" rel="noopener">Open on YouTube</a>` : "";
  return `<section class="panel">
      <h2>${esc(job.title)}</h2>
      <div class="meta">${chip(job.state)}${job.channel ? `<span>${esc(job.channel)}</span>` : ""}<span>${sectionText(job.section)}</span>${source}</div>
    </section>`;
}

function progress(job) {
  const now = Date.now() / 1000;
  const stages = job.stages.map((s) => {
    const status = s.status === "running" && job.state !== "running" ? "stopped" : s.status;
    const when = status === "done" ? took(s.seconds) : status === "running" && s.started ? `${took(now - s.started)} so far` : "";
    const err = status === "failed" && s.error ? `<span class="err">${esc(s.error)}</span>` : "";
    return `<li><span class="dot ${status}" aria-label="${status}"></span><span>${STAGE_NAMES[s.name]}</span><span class="when">${when}</span>${err}</li>`;
  }).join("");
  const action = job.state === "running"
    ? '<button class="btn danger" data-act="stop">Stop</button>'
    : `<button class="btn primary" data-act="resume">${job.state === "failed" ? "Try again" : "Resume"}</button>`;
  const note = job.state === "running"
    ? "You can close this page. Come back any time to check."
    : job.state === "failed" ? "A step failed. Try again resumes from that step." : "Stopped. Resume continues from where it left off.";
  return `<section class="panel">
      <div class="section-head"><h2>${job.state === "running" ? "Processing" : STATE_NAMES[job.state]}</h2><span class="meta">${Math.round(job.progress * 100)}%</span></div>
      <div class="progress" role="progressbar" aria-valuenow="${Math.round(job.progress * 100)}" aria-valuemin="0" aria-valuemax="100"><i style="width:${job.progress * 100}%"></i></div>
      <ul class="stages">${stages}</ul>
      ${job.last_log ? `<p class="log">${esc(job.last_log)}</p>` : ""}
      <p class="hint">${note}</p>
      <div class="btns">${action}</div>
    </section>`;
}

function finished(job) {
  const decided = Object.keys(job.decisions).length;
  const kept = job.items.filter((c) => job.decisions[c.id]?.verdict === "keep");
  const reviewLabel = decided === 0 ? "Review clips" : decided < job.items.length ? `Continue review (${decided}/${job.items.length})` : "Review again";
  const canShare = !!navigator.canShare;
  const cards = kept.map((clip) => `<article class="clip">
      <video src="${clipUrl(job.name, clip)}#t=0.5" preload="metadata" controls playsinline></video>
      <div class="body">
        <div class="meta"><strong>${esc(clipTitle(clip))}</strong><span>${clock(clip.end - clip.start)}</span></div>
        <div class="btns">
          <a class="btn" href="${clipUrl(job.name, clip, true)}" download="${esc(clip.file)}">Download</a>
          ${canShare ? `<button class="btn" data-share="${esc(clip.id)}">Share</button>` : ""}
        </div>
      </div>
    </article>`).join("");
  return `<section class="panel">
      <h2>${job.items.length} clips ready</h2>
      <p class="hint">Swipe right to keep a clip and left to reject it. Kept clips show up below to download${canShare ? " or share" : ""}.</p>
      <div class="btns"><a class="btn primary" href="#/review/${encodeURIComponent(job.name)}">${reviewLabel}</a></div>
    </section>
    <section>
      <div class="section-head"><h2>Kept clips</h2><span class="meta">${kept.length} of ${job.items.length}</span></div>
      ${kept.length ? `<div class="clips">${cards}</div>` : '<p class="empty">No kept clips yet.</p>'}
    </section>`;
}

function bindJob(job) {
  document.querySelector("[data-act]")?.addEventListener("click", async (event) => {
    const button = event.currentTarget;
    button.disabled = true;
    try {
      await api(`/api/jobs/${encodeURIComponent(job.name)}/${button.dataset.act}`, {});
      jobPage(job.name);
    } catch (err) {
      toast(err.message);
      button.disabled = false;
    }
  });
  document.querySelectorAll("[data-share]").forEach((button) => button.addEventListener("click", () => {
    share(job, job.items.find((c) => c.id === button.dataset.share), button);
  }));
}

async function share(job, clip, button) {
  button.disabled = true;
  try {
    const blob = await (await fetch(clipUrl(job.name, clip))).blob();
    const file = new File([blob], clip.file, { type: "video/mp4" });
    if (!navigator.canShare({ files: [file] })) throw new Error("This browser can't share video files. Use Download instead.");
    await navigator.share({ files: [file], title: clipTitle(clip) });
  } catch (err) {
    if (err.name !== "AbortError") toast(err.message);
  } finally {
    button.disabled = false;
  }
}

function clipTitle(clip) {
  return clip.judge?.title || TYPE_NAMES[clip.type] || clip.type.replace(/_/g, " ");
}

// ---------- Review: one clip at a time ----------

async function review(name) {
  clearInterval(poll);
  let job;
  try {
    job = await api(`/api/jobs/${encodeURIComponent(name)}`);
  } catch (err) {
    toast(err.message);
    return (location.hash = "#/");
  }
  document.title = `Review · ${job.title}`;
  const clips = job.items;
  const decisions = job.decisions;
  const history = [];
  // Clip times count from the start of the downloaded part; show them as times in the whole stream.
  const offset = job.section?.[0] || 0;
  let index = clips.findIndex((c) => !decisions[c.id]);
  if (index < 0) index = 0;

  app.innerHTML = `<div class="review">
      <div class="review-top">
        <a href="#/job/${encodeURIComponent(name)}" aria-label="Close review">Close</a>
        <span class="count" id="count"></span>
        <button id="sound" aria-label="Sound"></button>
      </div>
      <div class="deck" id="deck"></div>
      <div class="controls" id="controls">
        <button class="round reject" id="reject" aria-label="Reject (left arrow)">${ICON.reject}</button>
        <button class="round small" id="undo" aria-label="Undo">${ICON.undo}</button>
        <button class="round keep" id="keep" aria-label="Keep (right arrow)">${ICON.keep}</button>
      </div>
    </div>`;
  const deck = document.getElementById("deck");
  const sound = document.getElementById("sound");
  const showSound = () => (sound.innerHTML = muted ? ICON.soundOff : ICON.soundOn);
  showSound();
  sound.addEventListener("click", () => {
    muted = !muted;
    showSound();
    const video = deck.querySelector("video");
    if (video) video.muted = muted;
  });

  const show = () => {
    const clip = clips[index];
    document.getElementById("undo").disabled = !history.length;
    if (!clip) return finish();
    document.getElementById("controls").hidden = false;
    document.getElementById("count").textContent = `${index + 1} / ${clips.length}`;
    const verdict = decisions[clip.id]?.verdict;
    const reasons = (clip.reasons || []).join(", ") || "loud moment";
    deck.innerHTML = `<article class="card" id="card" aria-label="${esc(clipTitle(clip))}${verdict ? `, ${verdict === "keep" ? "kept" : "rejected"}` : ""}">
        <video src="${clipUrl(name, clip)}" playsinline loop autoplay ${muted ? "muted" : ""}></video>
        <span class="stamp keep">KEEP</span><span class="stamp reject">NOPE</span>
        <span class="paused"><i></i></span>
        <div class="info">
          <h2>#${clip.rank} · ${esc(clipTitle(clip))}</h2>
          <p>${esc(reasons)}</p>
          <p>${clock(clip.end - clip.start)} long · at ${clock(offset + clip.start)} in the stream${verdict ? ` · ${verdict === "keep" ? "kept" : "rejected"} before` : ""}</p>
        </div>
      </article>`;
    const card = document.getElementById("card");
    const video = card.querySelector("video");
    video.muted = muted;
    video.play().catch(() => card.classList.add("is-paused"));
    swipe(card, video, decide);
  };

  const finish = () => {
    const kept = clips.filter((c) => decisions[c.id]?.verdict === "keep").length;
    document.getElementById("count").textContent = "Done";
    document.getElementById("controls").hidden = !history.length;
    document.getElementById("keep").hidden = document.getElementById("reject").hidden = true;
    deck.innerHTML = `<div class="finish">
        <h2>All ${clips.length} clips reviewed</h2>
        <p>${kept} kept, ${clips.length - kept} rejected.</p>
        <a class="btn primary" href="#/job/${encodeURIComponent(name)}">See kept clips</a>
      </div>`;
  };

  const save = (clip, verdict) => api(`/api/jobs/${encodeURIComponent(name)}/decisions`, { id: clip.id, verdict })
    .catch((err) => toast(`Not saved: ${err.message}`));

  function decide(verdict) {
    const clip = clips[index];
    if (!clip) return;
    const card = document.getElementById("card");
    history.push({ index, previous: decisions[clip.id] || null });
    decisions[clip.id] = { verdict };
    save(clip, verdict);
    index += 1;
    if (card) {
      card.classList.add("fly");
      card.style.transform = `translateX(${verdict === "keep" ? 130 : -130}%) rotate(${verdict === "keep" ? 18 : -18}deg)`;
      card.style.opacity = "0";
      card.querySelector("video").pause();
      setTimeout(show, 260);
    } else {
      show();
    }
  }

  document.getElementById("keep").addEventListener("click", () => decide("keep"));
  document.getElementById("reject").addEventListener("click", () => decide("reject"));
  document.getElementById("undo").addEventListener("click", () => {
    const last = history.pop();
    if (!last) return;
    const clip = clips[last.index];
    index = last.index;
    if (last.previous) decisions[clip.id] = last.previous;
    else delete decisions[clip.id];
    api(`/api/jobs/${encodeURIComponent(name)}/decisions`, { id: clip.id, verdict: last.previous?.verdict ?? null })
      .catch((err) => toast(`Not saved: ${err.message}`));
    document.getElementById("keep").hidden = document.getElementById("reject").hidden = false;
    show();
  });
  review.keys = (event) => {
    if (event.key === "ArrowRight") decide("keep");
    else if (event.key === "ArrowLeft") decide("reject");
  };
  show();
}

function swipe(card, video, decide) {
  let startX = null, startY = 0, dx = 0, moved = false;
  const stamps = { keep: card.querySelector(".stamp.keep"), reject: card.querySelector(".stamp.reject") };
  card.addEventListener("pointerdown", (event) => {
    startX = event.clientX; startY = event.clientY; dx = 0; moved = false;
    card.classList.remove("settle");
    card.setPointerCapture(event.pointerId);
  });
  card.addEventListener("pointermove", (event) => {
    if (startX === null) return;
    dx = event.clientX - startX;
    if (Math.abs(dx) > 8 || Math.abs(event.clientY - startY) > 8) moved = true;
    card.style.transform = `translateX(${dx}px) rotate(${dx / 20}deg)`;
    const strength = Math.min(1, Math.abs(dx) / (card.offsetWidth * 0.3));
    stamps.keep.style.opacity = dx > 0 ? strength : 0;
    stamps.reject.style.opacity = dx < 0 ? strength : 0;
  });
  const end = (event) => {
    if (startX === null) return;
    // Use where the finger lifted too, in case the browser sent few or no move events.
    if (event.type === "pointerup") dx = event.clientX - startX;
    if (Math.abs(dx) > 8) moved = true;
    startX = null;
    if (Math.abs(dx) > card.offsetWidth * 0.3) return decide(dx > 0 ? "keep" : "reject");
    card.classList.add("settle");
    card.style.transform = "";
    stamps.keep.style.opacity = stamps.reject.style.opacity = 0;
    if (!moved) {
      // A tap plays or pauses the clip.
      if (video.paused) video.play().then(() => card.classList.remove("is-paused")).catch(() => {});
      else { video.pause(); card.classList.add("is-paused"); }
    }
  };
  card.addEventListener("pointerup", end);
  card.addEventListener("pointercancel", end);
}

// ---------- Routing ----------

function route() {
  clearInterval(poll);
  review.keys = null;
  const [, page, name] = location.hash.replace(/^#\/?/, "/").split("/").map(decodeURIComponent);
  if (page === "job" && name) jobPage(name);
  else if (page === "review" && name) review(name);
  else home();
}

document.addEventListener("keydown", (event) => review.keys?.(event));
window.addEventListener("hashchange", route);
route();

if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
