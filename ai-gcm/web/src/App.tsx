import { useEffect, useState } from "react";
import { Navigate, NavLink, Route, Routes, useLocation } from "react-router";
import { api, ApiError, type Me } from "./api";
import Brand from "./pages/Brand";
import Compilation from "./pages/Compilation";
import Editor from "./pages/Editor";
import Library from "./pages/Library";
import Live from "./pages/Live";
import NewStream from "./pages/NewStream";
import Review from "./pages/Review";
import Settings from "./pages/Settings";
import PostPage from "./pages/PostPage";
import Posts from "./pages/Posts";
import SignIn from "./pages/SignIn";
import Accept from "./pages/Accept";
import StreamPage from "./pages/StreamPage";
import StudioPage from "./pages/StudioPage";
import Streams from "./pages/Streams";

export default function App() {
  const [me, setMe] = useState<Me | null | undefined>(undefined);
  const [offline, setOffline] = useState(false);
  // Reviewing and editing are full-screen: the tab bar would cover their buttons on a phone.
  const path = useLocation().pathname;
  const reviewing = path.endsWith("/review") || path.endsWith("/edit");

  useEffect(() => {
    api<Me>("/api/me")
      .then(setMe)
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) setMe(null);
        else setOffline(true);
      });
  }, []);

  if (offline)
    return (
      <div className="shell">
        <h1>Can't reach the laptop</h1>
        <p className="muted">Kaatclip runs on the laptop at home. Check that it's on and connected, then try again.</p>
        <button onClick={() => location.reload()}>Try again</button>
      </div>
    );
  if (me === undefined) return <div className="shell"><p className="muted">Loading…</p></div>;
  if (me === null) return <SignIn />;
  if (me.accepted === false) return <Accept me={me} onAccepted={() => setMe({ ...me, accepted: true })} />;

  return (
    <>
      <header className="topbar">
        <NavLink to="/" className="brand">Kaat<span>clip</span></NavLink>
        <NavLink to="/new" className="button primary">+ Upload</NavLink>
      </header>
      <main className={reviewing ? "shell reviewing" : "shell"}>
        <Routes>
          <Route path="/" element={<Streams />} />
          <Route path="/new" element={<NewStream />} />
          <Route path="/streams/:id" element={<StreamPage />} />
          <Route path="/streams/:id/review" element={<Review />} />
          <Route path="/library" element={<Library />} />
          <Route path="/kept" element={<Navigate to="/library?decision=keep" replace />} />
          <Route path="/clips/:id/studio" element={<StudioPage />} />
          <Route path="/clips/:id/edit" element={<Editor />} />
          <Route path="/live" element={<Live />} />
          <Route path="/settings" element={<Settings me={me} />} />
          <Route path="/posts" element={<Posts />} />
          <Route path="/posts/:id" element={<PostPage />} />
          <Route path="/brand" element={<Brand />} />
          <Route path="/compilation" element={<Compilation />} />
          <Route path="*" element={<p>Page not found. <NavLink to="/">Back to your streams</NavLink></p>} />
        </Routes>
      </main>
      {!reviewing && <nav className="tabs">
        <NavLink to="/" end><span className="icon">🎬</span>Streams</NavLink>
        <NavLink to="/library"><span className="icon">📚</span>Library</NavLink>
        <NavLink to="/posts"><span className="icon">📅</span>Posts</NavLink>
        <NavLink to="/live"><span className="icon">🔴</span>Live</NavLink>
        <NavLink to="/settings"><span className="icon">⚙️</span>Settings</NavLink>
      </nav>}
    </>
  );
}
