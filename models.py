from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime

class SyncroBaseModel(BaseModel):
    """
    Base model for all Syncro objects to handle common configuration.
    
    Attributes:
        Config: Pydantic configuration class to allow field aliasing and 
                arbitrary types (useful for complex Syncro responses).
    """
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Ticket(SyncroBaseModel):
    """
    Represents a SyncroMSP Ticket.
    
    Attributes:
        id (int): The internal unique ID of the ticket.
        number (Optional[str]): The display number of the ticket (e.g., "28001").
        subject (str): The subject or title of the ticket.
        status (str): Current status (e.g., "New", "In Progress", "Resolved").
        problem_type (Optional[str]): The category of the problem.
        issue_type (Optional[str]): The specific type of issue.
        created_at (Optional[datetime]): Timestamp when the ticket was created.
        updated_at (Optional[datetime]): Timestamp when the ticket was last updated.
        resolved_at (Optional[datetime]): Timestamp when the ticket was resolved.
        customer_id (Optional[int]): ID of the customer associated with this ticket.
        customer_business_then_name (Optional[str]): Formatted name of the customer.
        user_id (Optional[int]): ID of the technician assigned to the ticket.
        properties (Dict[str, Any]): Dictionary of custom fields assigned to the ticket.
        comments (List[Dict[str, Any]]): List of comments/notes attached to the ticket.
    """
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
    comments: List[Dict[str, Any]] = Field(default_factory=list)

class Customer(SyncroBaseModel):
    """
    Represents a SyncroMSP Customer.
    
    Attributes:
        id (int): The internal unique ID of the customer.
        firstname (Optional[str]): Customer's first name.
        lastname (Optional[str]): Customer's last name.
        fullname (Optional[str]): Combined full name.
        business_name (Optional[str]): Name of the business.
        email (Optional[str]): Primary email address.
        phone (Optional[str]): Primary phone number.
        address (Optional[str]): Street address.
        city (Optional[str]): City.
        state (Optional[str]): State or Province.
        zip (Optional[str]): Postal code.
        properties (Dict[str, Any]): Dictionary of custom fields for the customer.
    """
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
    """
    Represents a SyncroMSP Customer Asset (Device).
    
    Attributes:
        id (int): The internal unique ID of the asset.
        name (str): The name of the asset (e.g., computer name).
        asset_type (Optional[str]): Type of asset (e.g., "Desktop", "Server").
        customer_id (Optional[int]): ID of the customer who owns this asset.
        properties (Dict[str, Any]): Dictionary of custom fields for the asset.
    """
    id: int
    name: str
    asset_type: Optional[str] = None
    customer_id: Optional[int] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
