# 🚀 SyncroMSP Python Wrapper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)

A robust, community-driven Python wrapper for the **SyncroMSP API**. Designed for MSPs and DevOps engineers who want to automate their workflows, build custom reporting tools, or create powerful AI-driven integrations.

---

## 📋 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [MCP Integration (Model Context Protocol)](#-mcp-integration-model-context-protocol)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **Full API Coverage:** Seamlessly interact with Tickets, Assets, Customers, Invoices, and more.
- **Smart Pagination:** Built-in handling for large datasets (e.g., fetching 1000+ customers).
- **Developer Friendly:** Clean, readable functions that return typed dictionary responses.
- **Environment Variable Support:** Easy configuration via `.env` files.
- **Robustness:** Built-in error handling and Unicode-safe printing for Windows environments.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/cybertek605/syncro-python-wrapper.git
cd syncro-python-wrapper
pip install -r requirements.txt
```

### 2. Set Up Environment
Copy the example environment file and add your Syncro API credentials:
```bash
cp .env.example .env
```

---

## ⚙️ Configuration

Edit your `.env` file with the following:

| Variable | Description |
|----------|-------------|
| `SYNCRO_API_BASE_URL` | Your Syncro instance URL (e.g., `https://yourdomain.syncromsp.com/api/v1/`) |
| `SYNCRO_API_TOKEN` | Your API token from Syncro Admin |
| `COMPANY_NAME` | Your MSP Company name |

---

## 💡 Usage Examples

### Tickets
Retrieve and search for tickets with ease:
```python
from syncro_python_wrapper import getTicket, getTickets_byuser

# Get a specific ticket
ticket = getTicket(12345)
print(f"[{ticket['number']}] {ticket['subject']}")

# Get all open tickets for a technician
tech_tickets = getTickets_byuser(789)
```

### Customers
Handle large customer lists using automatic pagination:
```python
from syncro_python_wrapper import getCustomers

all_customers = getCustomers()
print(f"Total Customers: {len(all_customers)}")
```

---

## 🛠 MCP Integration (Model Context Protocol)

This wrapper is designed to be **MCP-Ready**. Because the functions are structured cleanly and return standard Python dictionaries, any modern AI coding agent (like Claude, ChatGPT, or Gemini) can wrap this library into a fully functional **MCP Server** at the drop of a hat.

Simply provide this codebase to your agent and ask:
> "Use the functions in `syncro_python_wrapper.py` to create a Model Context Protocol (MCP) server so I can interact with my SyncroMSP data directly from my AI assistant."

---

## 🤝 Contributing

We welcome contributions! 
1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. **Open** a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ by the community for MSPs everywhere.*
