# 🛠 SyncroMSP Python Wrapper Roadmap

This list tracks the planned improvements to transform this wrapper into a professional-grade SDK and a powerful base for MCP tools.

## 🟢 Step 1: Robust Type Safety (Completed)
- [x] Implement Pydantic models for core Syncro objects (Ticket, Customer, Asset, Contact).
- [x] Refactor wrapper functions to return model instances instead of raw dictionaries.
- [x] Add field validation to ensure data integrity.

## 🟡 Step 2: Error Handling & Rate Limiting
- [ ] Create custom exception hierarchy (`SyncroAPIError`, `SyncroAuthError`, etc.).
- [ ] Implement automatic retries with exponential backoff.
- [ ] Add rate limit detection and handling.

## 🟡 Step 3: Asynchronous Support
- [ ] Migrate core requests logic to `httpx`.
- [ ] Provide `async` versions of all API wrapper functions.
- [ ] Optimize for high-concurrency MCP server environments.

## 🟡 Step 4: Search Primitives
- [ ] Create "Smart Search" functions that query multiple endpoints (e.g., searching customers by phone/email/name in one call).
- [ ] Add advanced filtering capabilities for ticket and asset searches.
