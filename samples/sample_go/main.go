// A visit counter in Go, built with its own Dockerfile.
// Cloudilio passes the port in PORT and keeps APP_DATA_DIR across publishes and restarts.
package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
)

var (
	mu      sync.Mutex
	dataDir = envOr("APP_DATA_DIR", "data")
	page    = template.Must(template.New("page").Parse(`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visit counter</title>
<style>
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:#f4f6f8;color:#1c2733;
display:grid;place-items:center;min-height:100vh}
main{background:#fff;border:1px solid #dde4ea;border-radius:16px;padding:40px 48px;text-align:center}
h1{margin:0 0 8px;font-size:1.4rem} .count{font-size:3.5rem;font-weight:700;color:#00add8;margin:8px 0}
p{color:#5d6b78;margin:0}
</style></head>
<body><main><h1>Hello from Go</h1><div class="count">{{.}}</div><p>visits so far, saved on the server</p></main></body></html>`))
)

func envOr(name, fallback string) string {
	if value := os.Getenv(name); value != "" {
		return value
	}
	return fallback
}

// count adds one visit and returns the total, kept in a file in the data folder
func count() (int, error) {
	mu.Lock()
	defer mu.Unlock()
	file := filepath.Join(dataDir, "visits.txt")
	visits := 0
	if raw, err := os.ReadFile(file); err == nil {
		visits, _ = strconv.Atoi(strings.TrimSpace(string(raw)))
	}
	visits++
	temporary := file + ".tmp"
	if err := os.WriteFile(temporary, []byte(strconv.Itoa(visits)), 0o644); err != nil {
		return 0, err
	}
	return visits, os.Rename(temporary, file)
}

func main() {
	if err := os.MkdirAll(dataDir, 0o755); err != nil {
		log.Fatal(err)
	}
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		visits, err := count()
		if err != nil {
			http.Error(w, "Could not save the visit", http.StatusInternalServerError)
			return
		}
		page.Execute(w, visits)
	})
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "ok")
	})
	port := envOr("PORT", "8000")
	log.Printf("Listening on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
