from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.capture.request_capture import extract_request_metadata, sanitize_payload
from app.capture.event_builder import build_threat_event
from app.client.ingest_client import forward_event_to_ingest
import os

router = APIRouter()
templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/wp-login.php", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Renders realistic WordPress fake login page and logs page_access event.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="page_access",
        status_code=200,
        severity="low",
        payload_summary={"view": "wp-login.php"}
    )
    await forward_event_to_ingest(event)
    return templates.TemplateResponse(request=request, name="login.html", context={"error_msg": None})

@router.post("/wp-login.php", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    log: str = Form(default=""),
    pwd: str = Form(default=""),
    wp_submit: str = Form(default="")
):
    """
    Intercepts fake login attempts, strictly redacts submitted passwords,
    forwards high-severity event to internal Ingest API, and returns HTTP 401 Unauthorized.
    """
    metadata = await extract_request_metadata(request)
    sanitized = sanitize_payload({"username": log, "password": pwd, "action": wp_submit})

    event = build_threat_event(
        metadata=metadata,
        event_type="login_attempt",
        status_code=401,
        severity="high",
        payload_summary=sanitized
    )
    await forward_event_to_ingest(event)

    # Return standard WordPress authentication failure response with 401 status code
    error_msg = f"Unknown username: '{log}'. Check again or try your email address." if log else "Invalid credentials."
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error_msg": error_msg},
        status_code=401
    )
