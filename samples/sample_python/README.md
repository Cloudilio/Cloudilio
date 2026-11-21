# General Python Application

This sample demonstrates a general Python application running on the Cloudilio SaaS platform.

### Capabilities
- **Pure Python**: Runs standard Python without requiring Flask, Django, or FastAPI.
- **Background Worker**: Spawns continuous background threads or loop scripts.
- **Persistent Data**: Saves state to `/app/data` (persisted across restarts).
- **Embedded Web Server**: Serves status and health check on `$PORT` using Python's built-in `http.server`.

### Deployment Command
```bash
python main.py
```
