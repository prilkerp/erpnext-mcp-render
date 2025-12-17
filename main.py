from fastapi import FastAPI
import httpx
import os

app = FastAPI()

ERP_URL = os.getenv("ERP_URL")  # e.g. https://yourcompany.frappe.cloud
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

HEADERS = {"Authorization": f"token {API_KEY}:{API_SECRET}"}

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/mcp")
async def mcp(payload: dict):
    method = payload.get("method")

    if method == "list_tools":
        return {"tools": [{"name": "get_customers"}, {"name": "get_overdue_invoices"}]}

    if method == "get_customers":
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(f"{ERP_URL}/api/resource/Customer", headers=HEADERS)
            return r.json()

    if method == "get_overdue_invoices":
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(
                f"{ERP_URL}/api/resource/Sales Invoice",
                headers=HEADERS,
                params={"filters": '[["status","=","Overdue"]]'}
            )
            return r.json()

    return {"error": f"Unknown method: {method}"}
