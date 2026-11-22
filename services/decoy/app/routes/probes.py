from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from app.capture.request_capture import extract_request_metadata
from app.capture.event_builder import build_threat_event
from app.client.ingest_client import forward_event_to_ingest

router = APIRouter()

@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt(request: Request):
    """
    Simulated robots.txt baiting attackers towards sensitive honey-paths.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="path_probe",
        status_code=200,
        severity="low",
        payload_summary={"target": "/robots.txt"}
    )
    await forward_event_to_ingest(event)

    content = """User-agent: *
Disallow: /wp-admin/
Disallow: /admin
Disallow: /backup/
Disallow: /.env
Disallow: /config/
"""
    return PlainTextResponse(content=content, status_code=200)

@router.api_route("/xmlrpc.php", methods=["GET", "POST"])
async def xmlrpc_probe(request: Request):
    """
    Common WordPress XML-RPC brute-force & DDoS target.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="path_probe",
        status_code=403,
        severity="medium",
        payload_summary={"target": "/xmlrpc.php"}
    )
    await forward_event_to_ingest(event)
    return PlainTextResponse("XML-RPC server accepts POST requests only.", status_code=403)

@router.api_route("/.env", methods=["GET", "POST"])
@router.api_route("/.git{rest_of_path:path}", methods=["GET", "POST"])
@router.api_route("/backup.sql", methods=["GET", "POST"])
@router.api_route("/phpmyadmin{rest_of_path:path}", methods=["GET", "POST"])
async def sensitive_file_probes(request: Request):
    """
    Probes for secrets, config leaks, and management tools.
    """
    metadata = await extract_request_metadata(request)
    event = build_threat_event(
        metadata=metadata,
        event_type="suspicious_request",
        status_code=404,
        severity="high",
        payload_summary={"probe": request.url.path}
    )
    await forward_event_to_ingest(event)
    return PlainTextResponse("File Not Found", status_code=404)
