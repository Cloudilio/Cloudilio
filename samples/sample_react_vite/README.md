# Task board: a React app built with Vite

- `src/App.jsx` is the app: a task list kept in the browser, and an About page.
- Each publish runs `npm ci` and `npm run build`, then serves the `dist` folder. Only the built files go online.
- Set `VITE_BOARD_NAME` on the app's Secrets page to rename the board. Settings named `VITE_...` are given to
  the build and end up in the site, so anyone can read them: never use them for private keys.
- `/about` opens directly because addresses that aren't files get `index.html`.

To run it on your computer: `npm install`, then `npm run dev`.
