import httpx
import logging
from typing import Dict, Any
from app.config import settings
from app.client.auth_client import get_internal_auth_headers

logger = logging.getLogger("decoy.ingest_client")

async def forward_event_to_ingest(event_data: Dict[str, Any]) -> bool:
    """
    Forwards captured threat events asynchronously to the Internal Ingest API.
    Handles network timeouts and errors gracefully without breaking the decoy response.
    """
    headers = get_internal_auth_headers()
    url = settings.ingest_service_url

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.post(url, json=event_data, headers=headers)
            if response.status_code in [200, 201]:
                logger.info(f"Successfully ingested event: {event_data.get('event_type')} from {event_data.get('source_ip')}")
                return True
            else:
                logger.warning(f"Failed to ingest event: HTTP {response.status_code} - {response.text}")
                return False
    except httpx.RequestError as e:
        logger.error(f"Error communicating with Ingest API at {url}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error forwarding event: {e}")
        return False
