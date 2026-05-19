from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import load_tenant_config
from payment import get_processor

app = FastAPI(title="Multitenant Demo Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS = [
    {"id": 1, "name": "Widget Básico", "price": 199.00},
    {"id": 2, "name": "Widget Pro", "price": 599.00},
    {"id": 3, "name": "Widget Enterprise", "price": 1999.00},
]

ORDERS = [
    {"id": "ord-001", "product": "Widget Pro", "amount": 599.00, "status": "paid"},
    {"id": "ord-002", "product": "Widget Básico", "amount": 199.00, "status": "pending"},
    {"id": "ord-003", "product": "Widget Enterprise", "amount": 1999.00, "status": "paid"},
]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/me")
def me():
    cfg = load_tenant_config()
    return {"slug": cfg.slug, "name": cfg.branding.name}


@app.get("/api/branding")
def branding():
    cfg = load_tenant_config()
    return cfg.branding.model_dump()


@app.get("/api/features")
def features():
    cfg = load_tenant_config()
    return cfg.features


@app.get("/api/products")
def products():
    return PRODUCTS


@app.get("/api/orders")
def orders():
    return ORDERS


class CheckoutRequest(BaseModel):
    product_id: int


@app.post("/api/checkout")
def checkout(req: CheckoutRequest):
    cfg = load_tenant_config()
    product = next((p for p in PRODUCTS if p["id"] == req.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    processor = get_processor(cfg.payment_provider)
    receipt = processor.process(product["price"])
    return {"product": product, "payment": receipt}
