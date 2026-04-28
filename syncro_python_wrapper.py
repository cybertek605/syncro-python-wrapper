## SyncroMSP Python Wrapper ##
## A COMMUNITY-DRIVEN API WRAPPER FOR SYNCROMSP ##
##
## github.com/cybertek605/syncro-python-wrapper ##

import sys
import os
import re
import requests
import datetime
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
from typing import Union, List, Optional

# Import Pydantic models
try:
    from .models import Ticket, Customer, Asset
except ImportError:
    # Handle cases where the package is not installed as a module
    from models import Ticket, Customer, Asset

# Load environment variables from .env file
load_dotenv()

# API Configuration
baseurl = os.getenv("SYNCRO_API_BASE_URL")
bearertoken = os.getenv("SYNCRO_API_TOKEN")

# Global setting for model usage
RETURN_MODELS = os.getenv("SYNCRO_RETURN_MODELS", "False").lower() == "true"

# Custom Field Configuration (IDs specific to your Syncro instance)
UNIFIED_CUSTOM_FIELD_TYPE_ID = int(os.getenv("SYNCRO_UNIFIED_CUSTOM_FIELD_TYPE_ID", "0"))
LABOR_CATEGORY_ID = int(os.getenv("SYNCRO_LABOR_CATEGORY_ID", "0"))

# Company Configuration
COMPANY_NAME = os.getenv("COMPANY_NAME", "Your Company")

# Setup Requests Headers
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
if bearertoken:
    headers["Authorization"] = "Bearer " + bearertoken

def configure_syncro_api(new_base_url, new_api_token):
    """
    Dynamically reconfigure the API credentials for multi-tenant use.
    
    Args:
        new_base_url (str): The new base URL for the Syncro API.
        new_api_token (str): The new API token to use for authentication.
    """
    global baseurl, bearertoken, headers
    baseurl = new_base_url
    bearertoken = new_api_token
    headers["Authorization"] = "Bearer " + new_api_token
    print(f"[CONFIG] Syncro API Wrapper reconfigured for: {baseurl}")

def to_model(data: Union[dict, list], model_class: Any) -> Any:
    """
    Helper to convert dictionary or list of dictionaries to Pydantic models.
    
    This function respects the global RETURN_MODELS setting.
    
    Args:
        data (Union[dict, list]): The raw data from the API response.
        model_class (Any): The Pydantic model class to convert the data into.
        
    Returns:
        Any: The converted Pydantic model(s) if RETURN_MODELS is True, 
             otherwise returns the original dictionary/list.
    """
    if not RETURN_MODELS or data is None:
        return data
    
    try:
        if isinstance(data, list):
            return [model_class(**item) for item in data]
        return model_class(**data)
    except Exception as e:
        print(f"⚠️ Model conversion error: {e}")
        return data

####
#### BASIC API REQUESTS
####

def getAppointment(id):
    """
    Retrieve a single appointment by its ID.
    
    Args:
        id (int/str): The unique ID of the appointment.
        
    Returns:
        dict: The appointment data.
    """
    url = f"{baseurl}appointments/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('appointment')

def getAppointments():
    """
    Retrieve all appointments.
    
    Returns:
        list: A list of all appointment dictionaries.
    """
    url = f"{baseurl}appointments"
    resp = requests.get(url, headers=headers)
    return resp.json().get('appointments')

def getAsset(id):
    """
    Retrieve a single customer asset by its ID.
    
    Args:
        id (int/str): The unique ID of the asset.
        
    Returns:
        Union[dict, Asset]: The asset data (as a dict or Pydantic model).
    """
    url = f"{baseurl}customer_assets/{id}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('asset')
    return to_model(data, Asset)

def getAssets():
    """
    Retrieve all customer assets.
    
    Returns:
        Union[list, List[Asset]]: A list of assets (as dicts or Pydantic models).
    """
    url = f"{baseurl}customer_assets"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('assets')
    return to_model(data, Asset)

def getContact(id):
    """
    Retrieve a single contact by its ID.
    
    Args:
        id (int/str): The unique ID of the contact.
        
    Returns:
        dict: The contact data.
    """
    url = f"{baseurl}contacts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contact')

def getContacts():
    """
    Retrieve all contacts.
    
    Returns:
        list: A list of all contact dictionaries.
    """
    url = f"{baseurl}contacts"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contacts')

def getContract(id):
    """
    Retrieve a single contract by its ID.
    
    Args:
        id (int/str): The unique ID of the contract.
        
    Returns:
        dict: The contract data.
    """
    url = f"{baseurl}contracts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contract')

def getContracts():
    """
    Retrieve all contracts.
    
    Returns:
        list: A list of all contract dictionaries.
    """
    url = f"{baseurl}contracts"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contracts')

def getCustomer(id):
    """
    Retrieve a single customer by their ID.
    
    Args:
        id (int/str): The unique ID of the customer.
        
    Returns:
        Union[dict, Customer]: The customer data (as a dict or Pydantic model).
    """
    url = f"{baseurl}customers/{id}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('customer')
    return to_model(data, Customer)

def getCustomers():
    """
    Fetch all customers from Syncro, handling paginated responses automatically.
    
    Returns:
        Union[list, List[Customer]]: A list of all customers (as dicts or models).
    """
    url = f"{baseurl}customers"
    all_customers = []
    page = 1

    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        
        if response.status_code != 200:
            print(f"⚠️ Failed to retrieve customers. Status Code: {response.status_code}")
            return to_model(all_customers, Customer)
        
        customers = response.json().get("customers", [])
        if not customers:
            break
        
        all_customers.extend(customers)
        page += 1

    return to_model(all_customers, Customer)

def getEstimate(id):
    """
    Retrieve a single estimate by its ID.
    
    Args:
        id (int/str): The unique ID of the estimate.
        
    Returns:
        dict: The estimate data.
    """
    url = f"{baseurl}estimates/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('estimate')

def getEstimates():
    """
    Retrieve all estimates.
    
    Returns:
        list: A list of all estimate dictionaries.
    """
    url = f"{baseurl}estimates"
    resp = requests.get(url, headers=headers)
    return resp.json().get('estimates')

def getInvoice(id):
    """
    Retrieve a single invoice by its ID.
    
    Args:
        id (int/str): The unique ID of the invoice.
        
    Returns:
        dict: The invoice data.
    """
    url = f"{baseurl}invoices/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('invoice')

def getInvoices():
    """
    Retrieve all invoices.
    
    Returns:
        list: A list of all invoice dictionaries.
    """
    url = f"{baseurl}invoices"
    resp = requests.get(url, headers=headers)
    return resp.json().get('invoices')

def getItems():
    """
    Retrieve all items (products/services).
    
    Returns:
        list: A list of all item dictionaries.
    """
    url = f"{baseurl}items"
    resp = requests.get(url, headers=headers)
    return resp.json().get('items')

def getLead(id):
    """
    Retrieve a single lead by its ID.
    
    Args:
        id (int/str): The unique ID of the lead.
        
    Returns:
        dict: The lead data.
    """
    url = f"{baseurl}leads/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('lead')

def getLeads():
    """
    Retrieve all leads.
    
    Returns:
        list: A list of all lead dictionaries.
    """
    url = f"{baseurl}leads"
    resp = requests.get(url, headers=headers)
    return resp.json().get('leads')

def getLineitems():
    """
    Retrieve all line items.
    
    Returns:
        list: A list of all line item dictionaries.
    """
    url = f"{baseurl}line_items"
    resp = requests.get(url, headers=headers)
    return resp.json().get('line_items')

def getPaymentmethods():
    """
    Retrieve all payment methods.
    
    Returns:
        list: A list of all payment method dictionaries.
    """
    url = f"{baseurl}payment_methods"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payment_methods')

def getPayment(id):
    """
    Retrieve a single payment by its ID.
    
    Args:
        id (int/str): The unique ID of the payment.
        
    Returns:
        dict: The payment data.
    """
    url = f"{baseurl}payments/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payment')

def getPayments():
    """
    Retrieve all payments.
    
    Returns:
        list: A list of all payment dictionaries.
    """
    url = f"{baseurl}payments"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payments')

def getPortalusers():
    """
    Retrieve all portal users.
    
    Returns:
        list: A list of all portal user dictionaries.
    """
    url = f"{baseurl}portal_users"
    resp = requests.get(url, headers=headers)
    return resp.json().get('portal_users')

def getProduct(id):
    """
    Retrieve a single product by its ID.
    
    Args:
        id (int/str): The unique ID of the product.
        
    Returns:
        dict: The product data.
    """
    url = f"{baseurl}products/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('product')

def getProducts():
    """
    Retrieve all products.
    
    Returns:
        list: A list of all product dictionaries.
    """
    url = f"{baseurl}products"
    resp = requests.get(url, headers=headers)
    return resp.json().get('products')

def getProductcategories():
    """
    Retrieve all product categories.
    
    Returns:
        list: A list of all product category dictionaries.
    """
    url = f"{baseurl}products/categories"
    resp = requests.get(url, headers=headers)
    return resp.json().get('categories')

def getPurchaseorder(id):
    """
    Retrieve a single purchase order by its ID.
    
    Args:
        id (int/str): The unique ID of the purchase order.
        
    Returns:
        dict: The purchase order data.
    """
    url = f"{baseurl}purchase_orders/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('purchase_order')

def getPurchaseorders():
    """
    Retrieve all purchase orders.
    
    Returns:
        list: A list of all purchase order dictionaries.
    """
    url = f"{baseurl}purchase_orders"
    resp = requests.get(url, headers=headers)
    return resp.json().get('purchase_orders')

def getRMMalert(id):
    """
    Retrieve a single RMM alert by its ID.
    
    Args:
        id (int/str): The unique ID of the RMM alert.
        
    Returns:
        dict: The RMM alert data.
    """
    url = f"{baseurl}rmm_alerts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('rmm_alert')

def getRMMalerts():
    """
    Retrieve all active RMM alerts.
    
    Returns:
        list: A list of active RMM alert dictionaries.
    """
    url = f"{baseurl}rmm_alerts?status=active"
    resp = requests.get(url, headers=headers)
    return resp.json().get('rmm_alerts')

def getSchedule(id):
    """
    Retrieve a single schedule by its ID.
    
    Args:
        id (int/str): The unique ID of the schedule.
        
    Returns:
        dict: The schedule data.
    """
    url = f"{baseurl}schedules/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('schedule')

def getSchedules():
    """
    Retrieve all schedules.
    
    Returns:
        list: A list of all schedule dictionaries.
    """
    url = f"{baseurl}schedules"
    resp = requests.get(url, headers=headers)
    return resp.json().get('schedules')

def getTicket(id):
    """
    Retrieve a single ticket by its ID.
    
    Args:
        id (int/str): The unique ID of the ticket.
        
    Returns:
        Union[dict, Ticket]: The ticket data (as a dict or Pydantic model).
    """
    url = f"{baseurl}tickets/{id}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('ticket')
    return to_model(data, Ticket)

def getSettings():
    """
    Retrieve system settings.
    
    Returns:
        dict: The system settings data.
    """
    url = f"{baseurl}settings"
    resp = requests.get(url, headers=headers)
    return resp.json().get('settings')

def getSettingstabs():
    """
    Retrieve system settings tabs.
    
    Returns:
        list: A list of system settings tabs.
    """
    url = f"{baseurl}settings/tabs"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tabs')

def getTickets():
    """
    Retrieve all tickets.
    
    Returns:
        Union[list, List[Ticket]]: A list of all tickets (as dicts or models).
    """
    url = f"{baseurl}tickets"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('tickets')
    return to_model(data, Ticket)

def getTickets_bycustomer_afterdate(customerid, createdafterdate):
    """
    Retrieve tickets for a specific customer created after a certain date.
    
    Args:
        customerid (int/str): The unique ID of the customer.
        createdafterdate (str): Date in YYYY-MM-DD format.
        
    Returns:
        Union[list, List[Ticket]]: A list of matching tickets.
    """
    url = f"{baseurl}tickets?customer_id={customerid}&created_after={createdafterdate}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('tickets')
    return to_model(data, Ticket)

def getTickets_byuser(user_id):
    """
    Retrieve all tickets assigned to a specific user (technician).
    
    Args:
        user_id (int/str): The unique ID of the user.
        
    Returns:
        Union[list, List[Ticket]]: A list of tickets assigned to the user.
    """
    url = f"{baseurl}tickets?user_id={user_id}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('tickets')
    return to_model(data, Ticket)

def getTickets_byuser_status(user_id, status):
    """
    Retrieve tickets assigned to a specific user with a specific status.
    
    Args:
        user_id (int/str): The unique ID of the user.
        status (str): The status to filter by (e.g., "In Progress").
        
    Returns:
        Union[list, List[Ticket]]: A list of matching tickets.
    """
    url = f"{baseurl}tickets?user_id={user_id}&status={status}"
    resp = requests.get(url, headers=headers)
    data = resp.json().get('tickets')
    return to_model(data, Ticket)

def getTicketssettings():
    """
    Retrieve ticket-related settings.
    
    Returns:
        dict: Ticket settings data.
    """
    url = f"{baseurl}tickets/settings"
    resp = requests.get(url, headers=headers)
    return resp.json()

def getTickettimers():
    """
    Retrieve all ticket timers.
    
    Returns:
        list: A list of all ticket timer dictionaries.
    """
    url = f"{baseurl}tickets_timers"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets_timers')

def getTimelogs():
    """
    Retrieve all time logs.
    
    Returns:
        list: A list of all time log dictionaries.
    """
    url = f"{baseurl}timelogs"
    resp = requests.get(url, headers=headers)
    return resp.json().get('timelogs')

def getTimelogs_user(id):
    """
    Retrieve time logs for a specific user.
    
    Args:
        id (int/str): The unique ID of the user.
        
    Returns:
        list: A list of time logs for the user.
    """
    url = f"{baseurl}timelogs?user_id={id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('timelogs')

def getVendor(id):
    """
    Retrieve a single vendor by its ID.
    
    Args:
        id (int/str): The unique ID of the vendor.
        
    Returns:
        dict: The vendor data.
    """
    url = f"{baseurl}vendors/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('vendor')

def getVendors():
    """
    Retrieve all vendors.
    
    Returns:
        list: A list of all vendor dictionaries.
    """
    url = f"{baseurl}vendors"
    resp = requests.get(url, headers=headers)
    return resp.json().get('vendors')

def getUser(id):
    """
    Retrieve a single user by their ID.
    
    Args:
        id (int/str): The unique ID of the user.
        
    Returns:
        dict: The user data.
    """
    url = f"{baseurl}users/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('user')

def getUsers():
    """
    Retrieve all users.
    
    Returns:
        list: A list of all user dictionaries.
    """
    url = f"{baseurl}users"
    resp = requests.get(url, headers=headers)
    return resp.json().get('users')

def getUseremail(id):
    """
    Retrieve the email address of a specific user.
    
    Args:
        id (int/str): The unique ID of the user.
        
    Returns:
        str: The user's email address.
    """
    user = getUser(id)
    return user.get('email') if user else None

def getUserfullname(id):
    """
    Retrieve the full name of a specific user.
    
    Args:
        id (int/str): The unique ID of the user.
        
    Returns:
        str: The user's full name.
    """
    user = getUser(id)
    return user.get('full_name') if user else None

def getWikipages():
    """
    Retrieve all wiki pages.
    
    Returns:
        list: A list of all wiki page dictionaries.
    """
    url = f"{baseurl}wiki_pages"
    resp = requests.get(url, headers=headers)
    return resp.json().get('wiki_pages')

###
### Complex API Requests
###

def getFullTicket(ticket_id):
    """
    Retrieves complete details for a given ticket, including notes, 
    status, custom fields, and attachments.
    
    Args:
        ticket_id (int/str): The unique ID of the ticket.
        
    Returns:
        dict: The complete ticket data.
    """
    url = f"{baseurl}tickets/{ticket_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('ticket', {})
    else:
        return {"error": f"Failed to retrieve ticket. Status code: {response.status_code}"}

def setTicketCustomFields(ticket_id, custom_fields):
    """
    Sets multiple custom field values for a ticket in a single API call.
    
    Args:
        ticket_id (int/str): The unique ID of the ticket.
        custom_fields (dict): A dictionary of field names and values.
        
    Returns:
        str: A status message indicating success or failure.
    """
    url = f"{baseurl}tickets/{ticket_id}"
    payload = {"properties": custom_fields}
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return f"Successfully updated ticket {ticket_id} custom fields."
    else:
        return f"Failed to update ticket {ticket_id}. Status: {response.status_code}"

def assignUnifiedCustomFields(ticket_id):
    """
    Assigns the unified custom field set to a ticket.
    
    Args:
        ticket_id (int/str): The unique ID of the ticket.
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if not UNIFIED_CUSTOM_FIELD_TYPE_ID:
        return False, "Unified custom field type ID not configured."

    url = f"{baseurl}tickets/{ticket_id}"
    payload = {"ticket_type_id": UNIFIED_CUSTOM_FIELD_TYPE_ID}
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        return True, f"Successfully assigned unified custom fields to ticket {ticket_id}"
    else:
        return False, f"Failed to assign custom fields. Status: {response.status_code}"

def addTicketComment(ticket_id, body, hidden=True, tech="Automation"):
    """
    Adds a comment/note to a ticket.
    
    Args:
        ticket_id (int/str): The unique ID of the ticket.
        body (str): The text content of the comment.
        hidden (bool): Whether the comment is private (hidden from customer).
        tech (str): The name to associate with the comment (e.g., "Automation").
        
    Returns:
        bool: True if successful, False otherwise.
    """
    url = f"{baseurl}tickets/{ticket_id}/comment"
    payload = {
        "subject": "Ticket Update",
        "tech": tech, 
        "body": body,
        "hidden": hidden,
        "do_not_email": True
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200

def getTicketByNumber(ticket_number):
    """
    Retrieve a single ticket by its display number.
    
    Args:
        ticket_number (int/str): The display number of the ticket.
        
    Returns:
        dict: The ticket data.
    """
    url = f"{baseurl}tickets?number={ticket_number}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tickets = response.json().get('tickets', [])
        return tickets[0] if tickets else None
    return None

def getCustomerDetails(customer_id):
    """
    Fetches comprehensive customer details.
    
    Args:
        customer_id (int/str): The unique ID of the customer.
        
    Returns:
        dict: The customer details data.
    """
    url = f"{baseurl}customers/{customer_id}"
    response = requests.get(url, headers=headers)
    return response.json().get("customer", {}) if response.status_code == 200 else {}

def updateCustomerCustomField(customer_id, field_name, field_value):
    """
    Updates a specific custom field for a customer.
    
    Args:
        customer_id (int/str): The unique ID of the customer.
        field_name (str): The name of the custom field to update.
        field_value (str): The new value for the field.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    url = f"{baseurl}customers/{customer_id}"
    payload = {"properties": {field_name: field_value}}
    response = requests.put(url, headers=headers, json=payload)
    return response.status_code == 200

def getLaborProducts():
    """
    Fetches all products in the 'Labor' category.
    
    Returns:
        list: A list of labor product dictionaries.
    """
    if not LABOR_CATEGORY_ID:
        print("Labor category ID not configured.")
        return []
    url = f"{baseurl}products?category_id={LABOR_CATEGORY_ID}"
    response = requests.get(url, headers=headers)
    return response.json().get("products", []) if response.status_code == 200 else []

def getLaborEntries(ticket_id, full_ticket=None):
    """
    Fetches labor/time entries for a specific ticket.
    
    Args:
        ticket_id (int/str): The unique ID of the ticket.
        full_ticket (dict, optional): If provided, serves as a fallback.
        
    Returns:
        list: A list of labor entry dictionaries.
    """
    url = f"{baseurl}tickets/{ticket_id}/time_entries"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("time_entries", [])
    if full_ticket:
        return full_ticket.get("ticket_timers", []) + full_ticket.get("line_items", [])
    return []

def _safe_print(text):
    """Helper to print text safely, handling Unicode encoding issues on Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))

def lookupCallerByPhone(phone_number: str) -> dict:
    """
    Look up an incoming caller in Syncro by phone number.
    
    Args:
        phone_number (str): The phone number to search for.
        
    Returns:
        dict: Information about the match found (found, company_name, etc.).
    """
    normalized = re.sub(r'\D', '', str(phone_number))[-10:]
    if len(normalized) < 7:
        return {"found": False}

    # Search customers
    resp = requests.get(f"{baseurl}customers", headers=headers, params={"q": normalized})
    if resp.status_code == 200:
        for customer in resp.json().get("customers", []):
            if re.sub(r'\D', '', customer.get("phone", ""))[-10:] == normalized:
                return {
                    "found": True,
                    "company_name": customer.get("business_name") or customer.get("name"),
                    "customer_id": customer["id"],
                    "match_type": "customer",
                }
    return {"found": False}
