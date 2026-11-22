from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.capture.request_capture import extract_request_metadata
from app.capture.event_builder import build_threat_event
from app.client.ingest_client import forward_event_to_ingest
import os

router = APIRouter()
templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Simulated corporate blog / landing page.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="page_access",
        status_code=200,
        severity="low",
        payload_summary={"page": "home"}
    )
    await forward_event_to_ingest(event)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Apex Dynamics - Enterprise Cloud Infrastructure</title>
        <style>
            body { font-family: -apple-system, sans-serif; margin: 0; padding: 40px; background: #fafafa; color: #222; }
            header { border-bottom: 2px solid #eaeaea; padding-bottom: 20px; }
            h1 { color: #1e3a8a; }
            .content { margin-top: 30px; font-size: 16px; line-height: 1.6; }
            footer { margin-top: 60px; font-size: 12px; color: #888; border-top: 1px solid #eaeaea; padding-top: 10px; }
        </style>
    </head>
    <body>
        <header>
            <h1>Apex Dynamics Corporate Portal</h1>
            <p>Next-generation distributed infrastructure systems.</p>
        </header>
        <div class="content">
            <h2>Welcome to our internal network</h2>
            <p>System Maintenance scheduled for 02:00 UTC. For administration, access the <a href="/wp-login.php">Management Portal</a>.</p>
        </div>
        <footer>
            &copy; 2026 Apex Dynamics Inc. All rights reserved. Powered by WordPress.
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.get("/admin", response_class=HTMLResponse)
@router.get("/wp-admin", response_class=HTMLResponse)
@router.get("/wp-admin/", response_class=HTMLResponse)
async def admin_portal(request: Request):
    """
    Decoy admin console returning HTTP 403 Forbidden.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="path_probe",
        status_code=403,
        severity="medium",
        payload_summary={"endpoint": request.url.path}
    )
    await forward_event_to_ingest(event)
    return templates.TemplateResponse(request=request, name="admin.html", context={}, status_code=403)
