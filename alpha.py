from fastapi import FastAPI, Request, Response
from sse_starlette.sse import EventSourceResponse
import httpx

app = FastAPI()

# Simulated logic to determine backend (replace with real logic)
def select_mcp_backend(user_id: str) -> str:
    # Example: hash-based routing, lookup in Redis, etc.
    # For now, route user_id ending with even digit to server A, else B
    if int(user_id[-1]) % 2 == 0:
        return "http://mcp-server-a:5000/sse"
    else:
        return "http://mcp-server-b:5000/sse"

# Extract user (simulate JWT decode or cookie parsing)
def extract_user_id(request: Request) -> str:
    # In production, extract from JWT token or cookie/session
    return request.headers.get("x-user-id", "user42")  # fallback to demo ID

@app.get("/sse")
async def sse_proxy(request: Request):
    user_id = extract_user_id(request)
    backend_url = select_mcp_backend(user_id)

    async def event_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                async with client.stream("GET", backend_url) as backend_response:
                    async for line in backend_response.aiter_lines():
                        if await request.is_disconnected():
                            break
                        if line.strip():
                            yield {"data": line}
            except Exception as e:
                yield {"event": "error", "data": f"Error: {str(e)}"}

    return EventSourceResponse(event_generator())