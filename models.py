from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class SyncroBaseModel(BaseModel):
    """Base model for all Syncro objects to handle common configuration."""
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Ticket(SyncroBaseModel):
    id: int
    number: Optional[str] = None
    subject: str
    status: str
    problem_type: Optional[str] = Field(None, alias="problem_type")
    issue_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    customer_id: Optional[int] = None
    customer_business_then_name: Optional[str] = None
    user_id: Optional[int] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    # Nested objects if present in full ticket response
    comments: List[Dict[str, Any]] = Field(default_factory=list)

class Customer(SyncroBaseModel):
    id: int
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    fullname: Optional[str] = None
    business_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)

class Asset(SyncroBaseModel):
    id: int
    name: str
    asset_type: Optional[str] = None
    customer_id: Optional[int] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
