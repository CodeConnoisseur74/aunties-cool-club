from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()


@app.get("/htmx-example", response_class=HTMLResponse)
async def htmx_example():
    return "<div>HTMX content</div>"
