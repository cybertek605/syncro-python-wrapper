import os
import re
import datetime
import asyncio
import httpx
from dotenv import load_dotenv
from typing import Union, List, Optional, Any
from functools import wraps

# Import Pydantic models and Exceptions
try:
    from .models import Ticket, Customer, Asset
    from .exceptions import (
        SyncroError, SyncroAuthError, SyncroPermissionError, 
        SyncroNotFoundError, SyncroRateLimitError, SyncroServerError, SyncroValidationError
    )
except ImportError:
    from models import Ticket, Customer, Asset
    from exceptions import (
        SyncroError, SyncroAuthError, SyncroPermissionError, 
        SyncroNotFoundError, SyncroRateLimitError, SyncroServerError, SyncroValidationError
    )

# Load environment variables
load_dotenv()

class SyncroClient:
    """
    An asynchronous client for the SyncroMSP API.
    
    This client handles authentication, retries, rate limiting, and 
    provides typed responses using Pydantic models.
    """

    def __init__(self, base_url: str = None, api_token: str = None):
        self.base_url = base_url or os.getenv("SYNCRO_API_BASE_URL")
        self.api_token = api_token or os.getenv("SYNCRO_API_TOKEN")
        
        if not self.base_url or not self.api_token:
            raise SyncroAuthError("Syncro API Base URL and Token must be provided.")

        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
        
        self.max_retries = int(os.getenv("SYNCRO_MAX_RETRIES", "3"))
        self.retry_delay = int(os.getenv("SYNCRO_RETRY_DELAY", "2"))
        self.return_models = os.getenv("SYNCRO_RETURN_MODELS", "False").lower() == "true"
        
        # Initialize an async client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=30.0
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()

    def _to_model(self, data: Union[dict, list], model_class: Any) -> Any:
        """Converts raw data to Pydantic models if enabled."""
        if not self.return_models or data is None:
            return data
        try:
            if isinstance(data, list):
                return [model_class(**item) for item in data]
            return model_class(**data)
        except Exception as e:
            print(f"⚠️ Model conversion error: {e}")
            return data

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Centralized async request handler with retry logic."""
        retries = 0
        while retries <= self.max_retries:
            try:
                response = await self.client.request(method, endpoint, **kwargs)
                
                if response.status_code in [200, 201]:
                    return response
                
                if response.status_code == 401:
                    raise SyncroAuthError("Invalid API Token or unauthorized access.")
                elif response.status_code == 403:
                    raise SyncroPermissionError("API Token lacks required permissions.")
                elif response.status_code == 404:
                    raise SyncroNotFoundError(f"Resource not found: {response.url}")
                elif response.status_code == 422:
                    raise SyncroValidationError(f"Validation error: {response.text}")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", self.retry_delay))
                    print(f"⚠️ Rate limit hit. Retrying in {retry_after}s...")
                    await asyncio.sleep(retry_after)
                    retries += 1
                    continue
                elif response.status_code >= 500:
                    if retries < self.max_retries:
                        print(f"⚠️ Server error ({response.status_code}). Retrying...")
                        await asyncio.sleep(self.retry_delay * (retries + 1))
                        retries += 1
                        continue
                    raise SyncroServerError(f"Syncro server error: {response.status_code}")
                else:
                    raise SyncroError(f"Unexpected API error: {response.status_code} - {response.text}")
                    
            except httpx.RequestError as e:
                if retries < self.max_retries:
                    print(f"⚠️ Network error: {e}. Retrying...")
                    await asyncio.sleep(self.retry_delay * (retries + 1))
                    retries += 1
                    continue
                raise SyncroError(f"Network request failed: {e}")
        
        return None

    # --- API Methods ---

    async def get_ticket(self, ticket_id: int) -> Union[dict, Ticket]:
        """Retrieve a single ticket by ID."""
        resp = await self._request("GET", f"tickets/{ticket_id}")
        data = resp.json().get('ticket')
        return self._to_model(data, Ticket)

    async def get_tickets(self) -> Union[list, List[Ticket]]:
        """Retrieve all tickets."""
        resp = await self._request("GET", "tickets")
        data = resp.json().get('tickets')
        return self._to_model(data, Ticket)

    async def get_customer(self, customer_id: int) -> Union[dict, Customer]:
        """Retrieve a single customer by ID."""
        resp = await self._request("GET", f"customers/{customer_id}")
        data = resp.json().get('customer')
        return self._to_model(data, Customer)

    async def get_customers(self) -> Union[list, List[Customer]]:
        """Fetch all customers with automatic pagination."""
        all_customers = []
        page = 1
        while True:
            resp = await self._request("GET", "customers", params={"page": page})
            customers = resp.json().get("customers", [])
            if not customers:
                break
            all_customers.extend(customers)
            page += 1
        return self._to_model(all_customers, Customer)

    async def get_asset(self, asset_id: int) -> Union[dict, Asset]:
        """Retrieve a single asset by ID."""
        resp = await self._request("GET", f"customer_assets/{asset_id}")
        data = resp.json().get('asset')
        return self._to_model(data, Asset)

    async def get_assets(self) -> Union[list, List[Asset]]:
        """Retrieve all assets."""
        resp = await self._request("GET", "customer_assets")
        data = resp.json().get('assets')
        return self._to_model(data, Asset)

    async def add_ticket_comment(self, ticket_id: int, body: str, hidden: bool = True, tech: str = "Automation"):
        """Add a comment to a ticket."""
        payload = {
            "subject": "Ticket Update",
            "tech": tech, 
            "body": body,
            "hidden": hidden,
            "do_not_email": True
        }
        resp = await self._request("POST", f"tickets/{ticket_id}/comment", json=payload)
        return resp.status_code in [200, 201]

    async def update_ticket_custom_fields(self, ticket_id: int, custom_fields: dict):
        """Update custom fields on a ticket."""
        await self._request("PUT", f"tickets/{ticket_id}", json={"properties": custom_fields})
        return True

    # Helper for legacy lookups
    async def lookup_caller_by_phone(self, phone_number: str) -> dict:
        """Search for a customer by phone number."""
        normalized = re.sub(r'\D', '', str(phone_number))[-10:]
        if len(normalized) < 7:
            return {"found": False}

        resp = await self._request("GET", "customers", params={"q": normalized})
        for customer in resp.json().get("customers", []):
            if re.sub(r'\D', '', customer.get("phone", ""))[-10:] == normalized:
                return {
                    "found": True,
                    "company_name": customer.get("business_name") or customer.get("name"),
                    "customer_id": customer["id"],
                    "match_type": "customer",
                }
        return {"found": False}

# Legacy Function support (Functional Wrapper)
# These allow users to use the library without managing the class instance themselves.

_global_client: Optional[SyncroClient] = None

def get_client() -> SyncroClient:
    global _global_client
    if _global_client is None:
        _global_client = SyncroClient()
    return _global_client

async def getTicket(id): return await get_client().get_ticket(id)
async def getTickets(): return await get_client().get_tickets()
async def getCustomer(id): return await get_client().get_customer(id)
async def getCustomers(): return await get_client().get_customers()
async def getAsset(id): return await get_client().get_asset(id)
async def getAssets(): return await get_client().get_assets()
async def addTicketComment(ticket_id, body, **kwargs): return await get_client().add_ticket_comment(ticket_id, body, **kwargs)
async def lookupCallerByPhone(phone): return await get_client().lookup_caller_by_phone(phone)
