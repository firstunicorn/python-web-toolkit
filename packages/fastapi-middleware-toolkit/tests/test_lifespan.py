"""Tests for lifespan management."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi_middleware_toolkit import (
    create_lifespan_manager,
    create_health_check_endpoint
)


def test_lifespan_manager_with_startup():
    """Test lifespan manager with startup function."""
    startup_called = []

    async def on_startup():
        startup_called.append(True)

    lifespan = create_lifespan_manager(
        on_startup=on_startup,
        service_name="test-api"
    )

    app = FastAPI(lifespan=lifespan)

    with TestClient(app):
        assert len(startup_called) == 1


def test_lifespan_manager_with_shutdown():
    """Test lifespan manager with shutdown function."""
    shutdown_called = []

    async def on_shutdown():
        shutdown_called.append(True)

    lifespan = create_lifespan_manager(
        on_shutdown=on_shutdown,
        service_name="test-api"
    )

    app = FastAPI(lifespan=lifespan)

    with TestClient(app):
        pass

    assert len(shutdown_called) == 1


def test_health_check_endpoint():
    """Test health check endpoint creation."""
    app = FastAPI()
    
    health_check = create_health_check_endpoint(
        service_name="test-api",
        version="1.0.0"
    )
    
    app.get("/health")(health_check)
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "test-api"
    assert response.json()["version"] == "1.0.0"


def test_health_check_endpoint_with_additional_checks():
    """Test health check with additional checks."""
    app = FastAPI()
    
    health_check = create_health_check_endpoint(
        service_name="test-api",
        version="1.0.0",
        additional_checks={"database": "connected", "cache": "ready"}
    )
    
    app.get("/health")(health_check)
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["database"] == "connected"
    assert response.json()["cache"] == "ready"
