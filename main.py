from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import auth, payment, transactions, user, product, category, supplier
from app.__init__ import create_tables

app = FastAPI(
    title="Inventory Management Backend",
    description="Inventory Management App's Backend for 470 Course Project",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(supplier.router)
app.include_router(transactions.router)
app.include_router(payment.router)


@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Auth API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
