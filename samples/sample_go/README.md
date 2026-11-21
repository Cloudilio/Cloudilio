# Visit counter: a Go app with its own Dockerfile

- `main.go` serves a page that counts visits, saved in `APP_DATA_DIR`, the folder Cloudilio keeps across
  publishes and restarts.
- The `Dockerfile` builds the program with the Go image and runs it from a tiny distroless image.
- Cloudilio runs it as user 1000 with a read-only filesystem, and passes the port in `PORT` (8000).

To run it on your computer: `go run .`, then open http://localhost:8000.
