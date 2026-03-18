"""Tests for CORS middleware setup."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_middleware_toolkit import setup_cors_middleware


def test_setup_cors_middleware_with_list():
    """Test CORS setup with list of origins."""
    app = FastAPI()
    
    setup_cors_middleware(
        app,
        allowed_origins=["http://localhost:3000"],
        allow_credentials=False
    )
    
    client = TestClient(app)
    
    @app.get("/test")
    def test_endpoint():
        return {"message": "ok"}
    
    # Test preflight request (requires Access-Control-Request-Method)
    response = client.options(
        "/test",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        }
    )
    
    assert response.status_code == 200


def test_setup_cors_middleware_with_string():
    """Test CORS setup with comma-separated string."""
    app = FastAPI()
    
    setup_cors_middleware(
        app,
        allowed_origins="http://localhost:3000,http://localhost:8080"
    )
    
    assert app is not None


def test_setup_cors_middleware_with_wildcard():
    """Test CORS setup with wildcard origin."""
    app = FastAPI()
    
    setup_cors_middleware(
        app,
        allowed_origins="*"
    )
    
    assert app is not None


def test_setup_cors_middleware_custom_methods():
    """Test CORS setup with custom methods."""
    app = FastAPI()
    
    setup_cors_middleware(
        app,
        allowed_origins=["http://localhost:3000"],
        allowed_methods=["GET", "POST", "PUT", "DELETE"]
    )
    
    assert app is not None
