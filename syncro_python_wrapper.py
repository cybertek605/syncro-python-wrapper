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

# Load environment variables from .env file
load_dotenv()

# API Configuration
baseurl = os.getenv("SYNCRO_API_BASE_URL")
bearertoken = os.getenv("SYNCRO_API_TOKEN")

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
    """Dynamically reconfigure the API credentials for multi-tenant use."""
    global baseurl, bearertoken, headers
    baseurl = new_base_url
    bearertoken = new_api_token
    headers["Authorization"] = "Bearer " + new_api_token
    print(f"[CONFIG] Syncro API Wrapper reconfigured for: {baseurl}")

####
#### BASIC API REQUESTS
####

def getAppointment(id):
    url = f"{baseurl}appointments/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('appointment')

def getAppointments():
    url = f"{baseurl}appointments"
    resp = requests.get(url, headers=headers)
    return resp.json().get('appointments')

def getAsset(id):
    url = f"{baseurl}customer_assets/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('asset')

def getAssets():
    url = f"{baseurl}customer_assets"
    resp = requests.get(url, headers=headers)
    return resp.json().get('assets')

def getContact(id):
    url = f"{baseurl}contacts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contact')

def getContacts():
    url = f"{baseurl}contacts"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contacts')

def getContract(id):
    url = f"{baseurl}contracts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contract')

def getContracts():
    url = f"{baseurl}contracts"
    resp = requests.get(url, headers=headers)
    return resp.json().get('contracts')

def getCustomer(id):
    url = f"{baseurl}customers/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('customer')

def getCustomers():
    """Fetch all customers from Syncro, handling paginated responses."""
    url = f"{baseurl}customers"
    all_customers = []
    page = 1

    while True:
        response = requests.get(f"{url}?page={page}", headers=headers)
        
        if response.status_code != 200:
            print(f"⚠️ Failed to retrieve customers. Status Code: {response.status_code}")
            return all_customers
        
        customers = response.json().get("customers", [])
        if not customers:
            break
        
        all_customers.extend(customers)
        page += 1

    return all_customers

def getEstimate(id):
    url = f"{baseurl}estimates/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('estimate')

def getEstimates():
    url = f"{baseurl}estimates"
    resp = requests.get(url, headers=headers)
    return resp.json().get('estimates')

def getInvoice(id):
    url = f"{baseurl}invoices/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('invoice')

def getInvoices():
    url = f"{baseurl}invoices"
    resp = requests.get(url, headers=headers)
    return resp.json().get('invoices')

def getItems():
    url = f"{baseurl}items"
    resp = requests.get(url, headers=headers)
    return resp.json().get('items')

def getLead(id):
    url = f"{baseurl}leads/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('lead')

def getLeads():
    url = f"{baseurl}leads"
    resp = requests.get(url, headers=headers)
    return resp.json().get('leads')

def getLineitems():
    url = f"{baseurl}line_items"
    resp = requests.get(url, headers=headers)
    return resp.json().get('line_items')

def getPaymentmethods():
    url = f"{baseurl}payment_methods"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payment_methods')

def getPayment(id):
    url = f"{baseurl}payments/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payment')

def getPayments():
    url = f"{baseurl}payments"
    resp = requests.get(url, headers=headers)
    return resp.json().get('payments')

def getPortalusers():
    url = f"{baseurl}portal_users"
    resp = requests.get(url, headers=headers)
    return resp.json().get('portal_users')

def getProduct(id):
    url = f"{baseurl}products/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('product')

def getProducts():
    url = f"{baseurl}products"
    resp = requests.get(url, headers=headers)
    return resp.json().get('products')

def getProductcategories():
    url = f"{baseurl}products/categories"
    resp = requests.get(url, headers=headers)
    return resp.json().get('categories')

def getPurchaseorder(id):
    url = f"{baseurl}purchase_orders/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('purchase_order')

def getPurchaseorders():
    url = f"{baseurl}purchase_orders"
    resp = requests.get(url, headers=headers)
    return resp.json().get('purchase_orders')

def getRMMalert(id):
    url = f"{baseurl}rmm_alerts/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('rmm_alert')

def getRMMalerts():
    url = f"{baseurl}rmm_alerts?status=active"
    resp = requests.get(url, headers=headers)
    return resp.json().get('rmm_alerts')

def getSchedule(id):
    url = f"{baseurl}schedules/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('schedule')

def getSchedules():
    url = f"{baseurl}schedules"
    resp = requests.get(url, headers=headers)
    return resp.json().get('schedules')

def getTicket(id):
    url = f"{baseurl}tickets/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('ticket')

def getSettings():
    url = f"{baseurl}settings"
    resp = requests.get(url, headers=headers)
    return resp.json().get('settings')

def getSettingstabs():
    url = f"{baseurl}settings/tabs"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tabs')

def getTickets():
    url = f"{baseurl}tickets"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets')

def getTickets_bycustomer_afterdate(customerid, createdafterdate):
    url = f"{baseurl}tickets?customer_id={customerid}&created_after={createdafterdate}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets')

def getTickets_byuser(user_id):
    url = f"{baseurl}tickets?user_id={user_id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets')

def getTickets_byuser_status(user_id, status):
    url = f"{baseurl}tickets?user_id={user_id}&status={status}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets')

def getTicketssettings():
    url = f"{baseurl}tickets/settings"
    resp = requests.get(url, headers=headers)
    return resp.json()

def getTickettimers():
    url = f"{baseurl}tickets_timers"
    resp = requests.get(url, headers=headers)
    return resp.json().get('tickets_timers')

def getTimelogs():
    url = f"{baseurl}timelogs"
    resp = requests.get(url, headers=headers)
    return resp.json().get('timelogs')

def getTimelogs_user(id):
    url = f"{baseurl}timelogs?user_id={id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('timelogs')

def getVendor(id):
    url = f"{baseurl}vendors/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('vendor')

def getVendors():
    url = f"{baseurl}vendors"
    resp = requests.get(url, headers=headers)
    return resp.json().get('vendors')

def getUser(id):
    url = f"{baseurl}users/{id}"
    resp = requests.get(url, headers=headers)
    return resp.json().get('user')

def getUsers():
    url = f"{baseurl}users"
    resp = requests.get(url, headers=headers)
    return resp.json().get('users')

def getUseremail(id):
    user = getUser(id)
    return user.get('email') if user else None

def getUserfullname(id):
    user = getUser(id)
    return user.get('full_name') if user else None

def getWikipages():
    url = f"{baseurl}wiki_pages"
    resp = requests.get(url, headers=headers)
    return resp.json().get('wiki_pages')

###
### Complex API Requests
###

def getFullTicket(ticket_id):
    """Retrieves complete details for a given ticket, including notes, status, custom fields, and attachments."""
    url = f"{baseurl}tickets/{ticket_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('ticket', {})
    else:
        return {"error": f"Failed to retrieve ticket. Status code: {response.status_code}"}

def setTicketCustomFields(ticket_id, custom_fields):
    """Sets multiple custom field values for a ticket in a single API call."""
    url = f"{baseurl}tickets/{ticket_id}"
    payload = {"properties": custom_fields}
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return f"Successfully updated ticket {ticket_id} custom fields."
    else:
        return f"Failed to update ticket {ticket_id}. Status: {response.status_code}"

def assignUnifiedCustomFields(ticket_id):
    """Assigns the unified custom field set to a ticket."""
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
    """Adds a comment to a ticket."""
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
    url = f"{baseurl}tickets?number={ticket_number}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tickets = response.json().get('tickets', [])
        return tickets[0] if tickets else None
    return None

def getCustomerDetails(customer_id):
    url = f"{baseurl}customers/{customer_id}"
    response = requests.get(url, headers=headers)
    return response.json().get("customer", {}) if response.status_code == 200 else {}

def updateCustomerCustomField(customer_id, field_name, field_value):
    url = f"{baseurl}customers/{customer_id}"
    payload = {"properties": {field_name: field_value}}
    response = requests.put(url, headers=headers, json=payload)
    return response.status_code == 200

def getLaborProducts():
    if not LABOR_CATEGORY_ID:
        print("Labor category ID not configured.")
        return []
    url = f"{baseurl}products?category_id={LABOR_CATEGORY_ID}"
    response = requests.get(url, headers=headers)
    return response.json().get("products", []) if response.status_code == 200 else []

def getLaborEntries(ticket_id, full_ticket=None):
    url = f"{baseurl}tickets/{ticket_id}/time_entries"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("time_entries", [])
    if full_ticket:
        return full_ticket.get("ticket_timers", []) + full_ticket.get("line_items", [])
    return []

def _safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))

def lookupCallerByPhone(phone_number: str) -> dict:
    """Look up an incoming caller in Syncro by phone number."""
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
