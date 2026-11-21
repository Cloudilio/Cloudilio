import { useEffect, useState } from "react";

// Set VITE_BOARD_NAME on the app's Secrets page to rename the board. Cloudilio gives the build every
// setting whose name starts with VITE_, and Vite writes it into the site, so it's public.
const BOARD_NAME = import.meta.env.VITE_BOARD_NAME || "My task board";
const STORAGE_KEY = "task-board";

// Two pages without a router package. Cloudilio sends every address that isn't a file to index.html,
// so /about opens directly, and so would the routes of React Router or any other router.
function usePath() {
  const [path, setPath] = useState(window.location.pathname);
  useEffect(() => {
    const onPop = () => setPath(window.location.pathname);
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);
  const go = (to) => {
    window.history.pushState({}, "", to);
    setPath(to);
  };
  return [path, go];
}

function Link({ to, go, children }) {
  return (
    <a
      href={to}
      onClick={(event) => {
        event.preventDefault();
        go(to);
      }}
    >
      {children}
    </a>
  );
}

function loadTasks() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function Board() {
  const [tasks, setTasks] = useState(loadTasks);
  const [text, setText] = useState("");

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  }, [tasks]);

  const add = (event) => {
    event.preventDefault();
    if (!text.trim()) return;
    setTasks([...tasks, { id: Date.now(), text: text.trim(), done: false }]);
    setText("");
  };
  const toggle = (id) => setTasks(tasks.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  const remove = (id) => setTasks(tasks.filter((t) => t.id !== id));
  const left = tasks.filter((t) => !t.done).length;

  return (
    <section className="card">
      <form className="add" onSubmit={add}>
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Add a task" aria-label="New task" />
        <button type="submit">Add</button>
      </form>
      {tasks.length === 0 ? (
        <p className="empty">Nothing here yet. Add your first task above.</p>
      ) : (
        <ul className="tasks">
          {tasks.map((task) => (
            <li key={task.id} className={task.done ? "done" : ""}>
              <label>
                <input type="checkbox" checked={task.done} onChange={() => toggle(task.id)} />
                <span>{task.text}</span>
              </label>
              <button className="remove" onClick={() => remove(task.id)} aria-label={`Remove ${task.text}`}>
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
      <p className="count">{left === 1 ? "1 task left" : `${left} tasks left`}</p>
    </section>
  );
}

function About() {
  return (
    <section className="card">
      <h2>About this board</h2>
      <p>
        A React app built with Vite. Your tasks are kept in this browser, so they stay when you come back but
        aren't shared with anyone else.
      </p>
      <p>
        Change the code in <code>src/App.jsx</code> and the look in <code>src/styles.css</code>. Each publish
        builds the site again.
      </p>
    </section>
  );
}

export default function App() {
  const [path, go] = usePath();
  return (
    <main>
      <header>
        <h1>{BOARD_NAME}</h1>
        <nav>
          <Link to="/" go={go}>Tasks</Link>
          <Link to="/about" go={go}>About</Link>
        </nav>
      </header>
      {path === "/about" ? <About /> : <Board />}
    </main>
  );
}
