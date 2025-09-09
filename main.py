from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import Product


app = FastAPI()

# Serve static assets
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

# Serve index.html at root
@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse("frontend/build/index.html")

# SPA fallback for client-side routing
@app.get("/{full_path:path}", include_in_schema=False)
def spa_fallback(full_path: str):
    if full_path.startswith(("api", "docs", "openapi.json", "redoc")):
        return {"detail": "Not Found"}
    return FileResponse("frontend/build/index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

@app.get("/api/products/")
def get_all_products():
    return products


@app.get("/api/products/{product_id}")
def get_product_by_id(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}

@app.post("/api/products/")
def create_product(product: Product):
    products.append(product)
    return {"message": "Product created successfully", "product": product}

@app.put("/api/products/{product_id}")
def update_product(product_id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == product_id:
            products[i] = product
            return {"message": "Product updated successfully", "product": product}
    return {"error": "Product not found"}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    for i in range(len(products)):
        if products[i].id == product_id:
            del products[i]
            return {"message": "Product deleted successfully"}
    return {"error": "Product not found"}
