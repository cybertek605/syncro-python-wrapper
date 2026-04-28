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

- **Asynchronous First:** Built on `httpx` and `asyncio` for high-performance, non-blocking API calls.
- **Robust Type Safety:** Created with Pydantic models for core Syncro objects (Ticket, Customer, Asset).
- **Self-Healing:** Automatic retries with exponential backoff for rate limits and server errors.
- **Smart Pagination:** Built-in handling for large datasets (e.g., fetching 1000+ customers).
- **Developer Friendly:** Modern class-based SDK or simple functional wrappers.

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
| `SYNCRO_RETURN_MODELS` | Set to `True` to receive Pydantic objects instead of dicts |

---

## 💡 Usage Examples

### Modern Class-based (Recommended)
The `SyncroClient` manages your connection pool efficiently:

```python
import asyncio
from syncro_python_wrapper import SyncroClient

async def main():
    async with SyncroClient() as syncro:
        # Fetch data concurrently
        ticket_task = syncro.get_ticket(12345)
        customer_task = syncro.get_customer(6789)
        
        ticket, customer = await asyncio.gather(ticket_task, customer_task)
        
        print(f"Ticket: {ticket.subject}")
        print(f"Customer: {customer.business_name}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Simple Functional Wrapper
If you just need a quick lookup:

```python
from syncro_python_wrapper import getTicket
import asyncio

ticket = asyncio.run(getTicket(12345))
print(ticket['subject'])
```

---

## 🛠 MCP Integration (Model Context Protocol)

This wrapper is designed to be **MCP-Ready**. Because the functions are structured cleanly and are asynchronous, any modern AI coding agent can wrap this library into a high-performance **MCP Server** instantly.

Simply provide this codebase to your agent and ask:
> "Use the SyncroClient in `syncro_python_wrapper.py` to create a Model Context Protocol (MCP) server so I can interact with my SyncroMSP data directly from my AI assistant."

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
