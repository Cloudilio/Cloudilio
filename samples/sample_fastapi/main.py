import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Sample FastAPI Service",
    description="Live FastAPI application hosted on Cloudilio",
    version="1.0.0"
)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI - Live on Cloudilio</title>
        <style>
            body { font-family: sans-serif; background: #f8fafc; color: #1e293b; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .card { background: white; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); text-align: center; max-width: 480px; }
            .badge { background: #dcfce7; color: #15803d; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 0.85rem; }
            a { color: #3b82f6; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">&bull; RUNNING</span>
            <h1>FastAPI is Live!</h1>
            <p>Your asynchronous Python service is serving live traffic with Uvicorn ASGI.</p>
            <p><a href="/docs">Open Interactive Swagger Docs &rarr;</a></p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "fastapi-uvicorn"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
