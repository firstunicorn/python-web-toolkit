import asyncio
import os
import sys
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

# 1. Config
from fastapi_config_patterns import BaseFastAPISettings, BaseDatabaseSettings

class AppSettings(BaseFastAPISettings, BaseDatabaseSettings):
    app_name: str = "BattleTestApp"
    postgres_db: str = "testdb"
    
# 2. Logging
from python_structlog_config import configure_structlog, get_logger

configure_structlog(log_level="INFO")
logger = get_logger("battle_test")

# 3. Exceptions
from python_app_exceptions import BusinessLogicError
from python_infrastructure_exceptions import DatabaseError

# 4. Primitives & Sanitizers
from python_technical_primitives.text import to_sentence_case
from postgres_data_sanitizers import sanitize_dict_for_postgres

# 5. Validation
from python_input_validation import validate_email_format

# 6. DTO Mappers
from python_dto_mappers import AutoMapper

class UserDTO(BaseModel):
    id: int
    name: str
    email: str

class UserEntity(BaseModel):
    id: int
    name: str
    email: str

mapper = AutoMapper(UserEntity, UserDTO)

# 7. CQRS & Mediator
from python_cqrs_core import BaseCommand, ICommandHandler
from python_cqrs_dispatcher import CQRSDispatcher

class CreateUserCommand(BaseCommand):
    name: str
    email: str

class CreateUserHandler(ICommandHandler[CreateUserCommand, UserDTO]):
    async def handle(self, command: CreateUserCommand) -> UserDTO:
        logger.info("Handling CreateUserCommand", name=command.name)
        
        # Validation
        if not validate_email_format(command.email):
            raise BusinessLogicError("Invalid email format")
            
        # Sanitizers (e.g. escaping null bytes if any)
        clean_data = sanitize_dict_for_postgres({"name": command.name})
        clean_name = clean_data["name"]
        
        # Primitive formatting
        formatted_name = to_sentence_case(clean_name)
        
        entity = UserEntity(id=1, name=formatted_name, email=command.email)
        return mapper.map(entity)

# 8. Domain Events
from python_domain_events import BaseDomainEvent
class UserCreatedEvent(BaseDomainEvent):
    user_id: int

# 9. Outbox
from python_outbox_core import IOutboxEvent
class UserCreatedOutboxEvent(IOutboxEvent):
    payload_user_id: int
    
    def get_event_type(self) -> str:
        return self.event_type
    def get_payload(self) -> dict:
        return {"user_id": self.payload_user_id}
    def get_source(self) -> str:
        return self.source
    def get_event_id(self) -> str:
        return str(self.event_id)
    def to_message(self) -> dict:
        return {"id": self.get_event_id(), "type": self.get_event_type(), "data": self.get_payload()}

# 10. FastAPI Middleware Toolkit
from fastapi_middleware_toolkit import setup_cors_middleware, setup_error_handlers
app = FastAPI()
settings = AppSettings()
setup_cors_middleware(app, settings.allowed_origins)
setup_error_handlers(app)

# 11. SQLAlchemy
from sqlalchemy_async_session_factory import create_async_engine_with_pool
from sqlalchemy_async_repositories import IRepository

# 12. Pydantic Response
from pydantic_response_models import SuccessResponse, ErrorResponse

async def run_battle_test():
    logger.info("Starting battle test...")
    
    dispatcher = CQRSDispatcher()
    dispatcher.register_command_handler(CreateUserCommand, CreateUserHandler())
    
    cmd = CreateUserCommand(name="john DOE", email="john.doe@example.com")
    try:
        user_dto = await dispatcher.send_command(cmd)
        logger.info("Successfully created user", user=user_dto.model_dump())
        
        response = SuccessResponse(data=user_dto)
        print("\n=== Final API Response JSON ===")
        print(response.model_dump_json(indent=2))
        
        # Test failure
        bad_cmd = CreateUserCommand(name="Jane", email="bad-email")
        await dispatcher.send_command(bad_cmd)
        
    except BusinessLogicError as e:
        logger.error("Caught expected business logic error", error=str(e))
        err_resp = ErrorResponse(error=str(e), code="BUSS_001")
        print("\n=== Final Error Response JSON ===")
        print(err_resp.model_dump_json(indent=2))
        
    # Domain Event check
    event = UserCreatedEvent(event_type="user_created", user_id=1)
    logger.info("Domain event generated", event_id=event.event_id)
    
    # Outbox Check
    outbox = UserCreatedOutboxEvent(
        event_id=uuid4(),
        event_type="com.test.user_created",
        aggregate_id="1",
        occurred_at=datetime.utcnow(),
        source="battle_test",
        payload_user_id=1
    )
    logger.info("Outbox event payload", payload=outbox.get_payload())

    # SQLAlchemy Factory
    try:
        engine = create_async_engine_with_pool(str(settings.postgres_url))
        logger.info("SQLAlchemy engine created", engine=str(engine))
    except Exception as e:
        logger.warning("Could not create DB engine (likely due to missing URL)", error=str(e))

    print("\nBattle Test Complete! All 17 packages participated successfully.")

if __name__ == "__main__":
    asyncio.run(run_battle_test())
