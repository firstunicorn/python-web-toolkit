# Transactional Outbox Implementation Guide

## ✅ Pre-Implementation Checklist

- [ ] Identify domain events that need reliable publishing
- [ ] Choose message broker (Kafka strongly recommended)
- [ ] Decide on worker scheduling strategy
- [ ] Plan monitoring & alerting approach

## 📋 Step-by-Step Implementation

### Phase 1: Core Setup
- [ ] Install `python-outbox-core` library
- [ ] Create ORM model for outbox table (extend `IOutboxEvent`)
- [ ] Implement `IOutboxRepository` with SQLAlchemy
- [ ] Add database migration for outbox table

### Phase 2: Event Publishing
- [ ] Define domain events (inherit from `IOutboxEvent`)
- [ ] Implement `to_message()` for each event
- [ ] Update command handlers to write events to outbox

### Phase 3: Worker Setup
- [ ] Implement `IEventPublisher` for your broker (Kafka strongly recommended)
- [ ] Create worker class extending `OutboxPublisherBase`
- [ ] Implement `schedule_publishing()` method
- [ ] Configure worker startup/shutdown

### Phase 4: Monitoring
- [ ] Add metrics for outbox lag (`count_unpublished()`)
- [ ] Set up alerts for publishing failures
- [ ] Monitor batch processing performance
- [ ] Add health checks

## 🔧 Integration Patterns

### Pattern A: FastAPI (lifespan) + Kafka + FastStream + Celery + Kong Events Gate
// TODO: (code example)


## 🔄 **Lifespan implementation**

### **What Is Lifespan?**

**Lifespan** is FastAPI's way to run code **before** your app starts and **after** it shuts down. It's like "hooks" for startup/shutdown.

### **Your Current Lifespan** (`app_factory.py`)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # ⬇️ STARTUP - runs ONCE when FastAPI starts
    logger.info("GridFlow API starting up")
    await init_db()  # Initialize database connection pool
    logger.info("Database initialized successfully")

    yield  # ← App is now running and serving requests

    # ⬇️ SHUTDOWN - runs ONCE when FastAPI stops
    logger.info("GridFlow API shutting down")
```

**Flow:**
```
1. Server starts (uvicorn run)
   ↓
2. Lifespan STARTUP runs
   - Initialize database
   - Log startup
   ↓
3. yield ← App is now ready
   ↓
4. App serves requests... (your API endpoints work)
   ↓
5. Server stops (Ctrl+C or crash)
   ↓
6. Lifespan SHUTDOWN runs
   - Cleanup resources
   - Log shutdown
```

---

## 🎯 **Where Outbox Worker Fits**

You need to **start the outbox worker** in the lifespan startup!

### **Current (Without Outbox):**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("GridFlow API starting up")
    await init_db()
    yield
    # Shutdown
    logger.info("GridFlow API shutting down")
```

### **Updated (With Outbox Worker):**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("GridFlow API starting up")
    await init_db()

    # 🆕 Start outbox worker as background task
    outbox_worker = create_outbox_worker()  # Your worker instance
    worker_task = asyncio.create_task(outbox_worker.schedule_publishing())
    logger.info("Outbox worker started")

    yield  # App is running

    # Shutdown
    logger.info("GridFlow API shutting down")

    # 🆕 Stop outbox worker gracefully
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        logger.info("Outbox worker stopped")
```

---

## 📊 **Complete Flow with Outbox**

```
┌─────────────────────────────────────────────────────────┐
│ 1. FastAPI Server Starts (uvicorn)                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. Lifespan STARTUP                                     │
│    ├─ Initialize database (init_db)                     │
│    ├─ Create outbox worker                             │
│    └─ Start background task (asyncio.create_task)      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. App Running (yield)                                  │
│                                                         │
│    ┌─────────────────────────────────────────────┐    │
│    │ Main FastAPI Process                        │    │
│    │ - Handles HTTP requests                     │    │
│    │ - Command handlers store events to outbox   │    │
│    └─────────────────────────────────────────────┘    │
│                                                         │
│    ┌─────────────────────────────────────────────┐    │
│    │ Background Outbox Worker (asyncio task)     │    │
│    │ - Polls outbox table every 5s               │    │
│    │ - Publishes events to Kafka                 │    │
│    │ - Marks events as published                 │    │
│    │ - Runs in parallel with FastAPI             │    │
│    └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. Server Stops (Ctrl+C)                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. Lifespan SHUTDOWN                                    │
│    ├─ Cancel worker task                               │
│    ├─ Wait for graceful stop                           │
│    └─ Close database connections                       │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 **Why Use Lifespan for Outbox Worker?**

### **Option A: Lifespan (Recommended for Single Server)**

✅ **Pros:**
- Simple - worker runs in same process as FastAPI
- No separate Celery infrastructure
- Graceful shutdown
- Good for MVP/small scale

❌ **Cons:**
- Single worker (no horizontal scaling)
- Worker restarts when app restarts

**Use when:**
- MVP or small-scale app
- Running 1-2 FastAPI instances
- Don't want Celery complexity

---

### **Option B: Celery (Recommended for Production)**

✅ **Pros:**
- Distributed workers (horizontal scaling)
- Workers independent of FastAPI
- Can restart FastAPI without stopping workers
- Better for high event volume

❌ **Cons:**
- Requires Redis/RabbitMQ
- More complex infrastructure
- Separate worker process to manage

**Use when:**
- Production scale
- Multiple FastAPI instances
- High event throughput
- Need worker redundancy

---

## 🔧 **Your Implementation Options**

### **Option 1: Simple Lifespan Worker (Start Here)**

```python
# backend/src/infrastructure/app_factory.py

from contextlib import asynccontextmanager
import asyncio
from backend.src.infrastructure.messaging.outbox_worker import create_outbox_worker

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with outbox worker."""
    # Startup
    logger.info("GridFlow API starting up")
    await init_db()

    # Start outbox worker
    worker = create_outbox_worker()
    worker_task = asyncio.create_task(worker.schedule_publishing())
    logger.info("Outbox worker started in background")

    yield  # App is running

    # Shutdown
    logger.info("GridFlow API shutting down")

    # Stop worker gracefully
    worker_task.cancel()
    try:
        await asyncio.wait_for(worker_task, timeout=10.0)
    except (asyncio.CancelledError, asyncio.TimeoutError):
        logger.info("Outbox worker stopped")
```

---

### **Option 2: Celery Worker (Later/Production)**

```python
# backend/src/infrastructure/app_factory.py
# (NO changes to lifespan - Celery runs separately)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - Celery worker runs separately."""
    # Startup
    logger.info("GridFlow API starting up")
    await init_db()
    yield
    # Shutdown
    logger.info("GridFlow API shutting down")

# Separate Celery worker process:
# celery -A backend.celery_worker worker --loglevel=info
# celery -A backend.celery_worker beat --loglevel=info
```

---

**simple startup integration**:

### **Start with Option 1 (Lifespan)**

**Why:**
- ✅ Simpler to implement initially
- ✅ No Celery infrastructure needed yet
- ✅ Good for testing outbox pattern
- ✅ Can migrate to Celery later without changing core logic

**Later, move to Option 2 (Celery) when:**
- You need to scale (multiple workers)
- Event volume is high
- You need worker monitoring
- You already use Celery for other tasks

---

## 📋 **What You Need to Add**

1. **Outbox worker factory:**
```python
# backend/src/infrastructure/messaging/outbox_worker.py

from outbox_sdk.core import OutboxPublisherBase
from outbox_sdk.integrations.faststream import FastStreamKafkaPublisher

class GridFlowOutboxWorker(OutboxPublisherBase):
    async def schedule_publishing(self):
        """Simple polling loop."""
        while True:
            await self.publish_batch(limit=100)
            await asyncio.sleep(5)

def create_outbox_worker() -> GridFlowOutboxWorker:
    """Factory to create configured worker."""
    repo = get_outbox_repository()  # Your SQLAlchemy repo
    publisher = FastStreamKafkaPublisher(kafka_broker)  # Your Kafka publisher
    return GridFlowOutboxWorker(repo, publisher)
```

2. **Update lifespan** (as shown above)

3. **Done!** Worker runs automatically when FastAPI starts.

---

**TL;DR:** Lifespan = FastAPI's startup/shutdown hooks. You'll start your outbox worker there as a background task, running in parallel with your API. 🚀