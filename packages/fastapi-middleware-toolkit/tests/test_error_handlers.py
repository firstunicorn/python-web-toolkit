"""Tests for error handler setup."""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from fastapi_middleware_toolkit import setup_error_handlers


def test_http_exception_handler():
    """Test HTTP exception handling."""
    app = FastAPI()
    setup_error_handlers(app)
    
    @app.get("/test")
    def test_endpoint():
        raise HTTPException(status_code=404, detail="Not found")
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_unhandled_exception_handler():
    """Test unhandled exception handling."""
    app = FastAPI()
    setup_error_handlers(app)
    
    @app.get("/test")
    def test_endpoint():
        raise ValueError("Something went wrong")
    
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/test")
    
    assert response.status_code == 500
    assert "Internal server error" in response.json()["detail"]


def test_validation_error_handler():
    """Test validation error handling."""
    from pydantic import BaseModel
    
    class Item(BaseModel):
        name: str
        value: int
    
    app = FastAPI()
    setup_error_handlers(app)
    
    @app.post("/test")
    def test_endpoint(item: Item):
        return item
    
    client = TestClient(app)
    response = client.post("/test", json={"name": "test"})  # Missing value
    
    assert response.status_code == 422
    assert "errors" in response.json()


def test_custom_exception_handler():
    """Test custom exception class handling."""
    
    class CustomException(Exception):
        def __init__(self, message: str, details: dict = None):
            self.message = message
            self.details = details
            super().__init__(message)
    
    app = FastAPI()
    setup_error_handlers(app, CustomException)
    
    @app.get("/test")
    def test_endpoint():
        raise CustomException("Custom error", {"code": "ERR_001"})
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Custom error"
    assert response.json()["details"] == {"code": "ERR_001"}
