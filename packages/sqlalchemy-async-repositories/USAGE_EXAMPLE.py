"""
Real-world usage example of the hybrid pagination approach.

This shows how the library works in actual code.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Import our hybrid repository
from sqlalchemy_async_repositories import (
    BaseRepository,
    FilterSpec,
    SortSpec,
    PaginatedResult,
    has_fastcrud
)


# ========================================
# 1. Define ORM Model (SQLAlchemy)
# ========================================

class Base(DeclarativeBase):
    pass


class InviteORM(Base):
    """ORM model for invites table."""
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)


# ========================================
# 2. Create Repository (Clean Interface)
# ========================================

class InviteRepository(BaseRepository[InviteORM]):
    """
    Invite repository using hybrid approach.

    - Basic CRUD uses native SQLAlchemy (fast!)
    - Pagination uses FastCRUD if available, else native
    """

    async def find_active_invites(
        self,
        page: int = 1,
        page_size: int = 10
    ) -> PaginatedResult[InviteORM]:
        """Find all active (unused, non-expired) invites."""
        now = datetime.utcnow()

        return await self.find_paginated(
            page=page,
            page_size=page_size,
            filters=[
                FilterSpec(field="is_used", operator="eq", value=False),
                FilterSpec(field="expires_at", operator="gt", value=now)
            ],
            sort=[
                SortSpec(field="created_at", direction="desc")
            ]
        )

    async def search_by_email_domain(
        self,
        domain: str,
        page: int = 1
    ) -> PaginatedResult[InviteORM]:
        """Search invites by email domain."""
        return await self.find_paginated(
            page=page,
            page_size=20,
            filters=[
                FilterSpec(field="email", operator="like", value=domain)
            ],
            sort=[
                SortSpec(field="email", direction="asc")
            ]
        )


# ========================================
# 3. Usage in Application Layer
# ========================================

async def example_usage(db_session: AsyncSession):
    """Example of using the hybrid repository."""

    # Create repository
    repo = InviteRepository(db_session, InviteORM)

    # Check which backend is being used
    print(f"Using FastCRUD: {has_fastcrud()}")

    # ========================================
    # Basic CRUD (Native SQLAlchemy - Fast!)
    # ========================================

    # Create invite
    new_invite = InviteORM(
        email="user@example.com",
        token="abc123",
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    created_invite = await repo.create(new_invite)
    print(f"Created invite ID: {created_invite.id}")

    # Get by ID
    invite = await repo.get_by_id(created_invite.id)
    print(f"Found invite: {invite.email}")

    # Update
    invite.is_used = True
    updated_invite = await repo.update(invite)
    print(f"Updated invite: {updated_invite.is_used}")

    # Check existence
    exists = await repo.exists(created_invite.id)
    print(f"Invite exists: {exists}")

    # Count all
    total = await repo.count()
    print(f"Total invites: {total}")

    # ========================================
    # Advanced Pagination (Hybrid Approach!)
    # ========================================

    # Example 1: Find active invites
    result = await repo.find_active_invites(page=1, page_size=10)

    print(f"\nActive Invites:")
    print(f"  Total: {result.total}")
    print(f"  Page: {result.page}/{result.pages}")
    print(f"  Has next: {result.has_next}")
    print(f"  Has prev: {result.has_prev}")

    for invite in result.items:
        print(f"  - {invite.email} (created: {invite.created_at})")

    # Example 2: Complex filtering
    yesterday = datetime.utcnow() - timedelta(days=1)

    result = await repo.find_paginated(
        page=1,
        page_size=5,
        filters=[
            FilterSpec(field="is_used", operator="eq", value=False),
            FilterSpec(field="created_at", operator="gte", value=yesterday),
            FilterSpec(field="email", operator="like", value="example.com")
        ],
        sort=[
            SortSpec(field="created_at", direction="desc"),
            SortSpec(field="email", direction="asc")
        ]
    )

    print(f"\nFiltered Results:")
    print(f"  Found {result.total} invites matching criteria")

    # Example 3: Search by domain
    result = await repo.search_by_email_domain("gmail.com", page=1)

    print(f"\nGmail Invites:")
    print(f"  Found {result.total} Gmail addresses")

    # Example 4: Pagination loop
    page = 1
    all_invites: List[InviteORM] = []

    while True:
        result = await repo.find_paginated(
            page=page,
            page_size=100,
            sort=[SortSpec(field="id", direction="asc")]
        )

        all_invites.extend(result.items)

        if not result.has_next:
            break

        page += 1

    print(f"\nLoaded all {len(all_invites)} invites")

    # ========================================
    # The beauty: Same API, Different Backend!
    # ========================================
    # If FastCRUD is installed: Uses FastCRUD (battle-tested)
    # If FastCRUD not available: Uses native SQLAlchemy (zero dependencies)
    # Your code works either way! 🎉


# ========================================
# 4. Usage in FastAPI Handler
# ========================================

async def fastapi_handler_example(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10,
    only_active: bool = True,
    email_filter: Optional[str] = None
):
    """Example FastAPI handler using the repository."""

    repo = InviteRepository(db, InviteORM)

    # Build filters dynamically
    filters = []

    if only_active:
        filters.append(FilterSpec(field="is_used", operator="eq", value=False))
        filters.append(
            FilterSpec(
                field="expires_at",
                operator="gt",
                value=datetime.utcnow()
            )
        )

    if email_filter:
        filters.append(
            FilterSpec(field="email", operator="like", value=email_filter)
        )

    # Get paginated results
    result = await repo.find_paginated(
        page=page,
        page_size=page_size,
        filters=filters if filters else None,
        sort=[SortSpec(field="created_at", direction="desc")]
    )

    # Return API response
    return {
        "invites": [
            {
                "id": inv.id,
                "email": inv.email,
                "is_used": inv.is_used,
                "created_at": inv.created_at.isoformat()
            }
            for inv in result.items
        ],
        "pagination": {
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "pages": result.pages,
            "has_next": result.has_next,
            "has_prev": result.has_prev
        }
    }


# ========================================
# 5. Integration with Specification Pattern
# ========================================

def specification_to_filters(specification) -> List[FilterSpec]:
    """
    Convert Specification Pattern to FilterSpec.

    This shows how to integrate with your existing
    Specification Pattern if needed.
    """
    # Example: Convert domain specification to filters
    # This would depend on your specific specification implementation

    filters = []

    # Pseudo-code example:
    # if isinstance(specification, ActiveInviteSpec):
    #     filters.append(FilterSpec(field="is_used", operator="eq", value=False))
    #     filters.append(FilterSpec(field="expires_at", operator="gt", value=datetime.utcnow()))

    return filters


if __name__ == "__main__":
    print("This is a usage example file.")
    print("See the functions above for real-world usage patterns.")
    print(f"\nFastCRUD available: {has_fastcrud()}")

