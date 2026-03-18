"""Tests for Cache-Control middleware."""

import pytest
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from fastapi_middleware_toolkit import setup_cache_control_middleware


def test_default_cache_control_set():
    """Test that default Cache-Control is set when route doesn't set it."""
    app = FastAPI()
    setup_cache_control_middleware(app)
    
    @app.get("/test")
    def test_endpoint():
        return {"message": "ok"}
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert "cache-control" in response.headers
    assert response.headers["cache-control"] == "public, max-age=60, stale-while-revalidate=30"


def test_route_can_override_cache_control():
    """Test that routes can override the default Cache-Control."""
    app = FastAPI()
    setup_cache_control_middleware(app)
    
    @app.get("/test")
    def test_endpoint(response: Response):
        response.headers["Cache-Control"] = "no-store"
        return {"message": "sensitive"}
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"


def test_custom_default_cache_control():
    """Test middleware with custom default Cache-Control."""
    app = FastAPI()
    setup_cache_control_middleware(app, default_cache_control="no-store")
    
    @app.get("/test")
    def test_endpoint():
        return {"message": "ok"}
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"


def test_cache_control_not_duplicated():
    """Test that Cache-Control is not duplicated if already set."""
    app = FastAPI()
    setup_cache_control_middleware(app)
    
    @app.get("/test")
    def test_endpoint(response: Response):
        response.headers["Cache-Control"] = "private, max-age=0"
        return {"message": "ok"}
    
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    assert response.headers["cache-control"] == "private, max-age=0"
    assert response.headers["cache-control"].count("max-age") == 1


def test_multiple_routes_work():
    """Test that middleware works correctly for multiple routes."""
    app = FastAPI()
    setup_cache_control_middleware(app, default_cache_control="public, max-age=300")
    
    @app.get("/cacheable")
    def cacheable():
        return {"type": "cacheable"}
    
    @app.get("/no-cache")
    def no_cache(response: Response):
        response.headers["Cache-Control"] = "no-cache"
        return {"type": "no-cache"}
    
    client = TestClient(app)
    
    cacheable_response = client.get("/cacheable")
    assert cacheable_response.headers["cache-control"] == "public, max-age=300"
    
    no_cache_response = client.get("/no-cache")
    assert no_cache_response.headers["cache-control"] == "no-cache"
