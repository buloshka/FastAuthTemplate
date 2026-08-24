import pytest
import uuid
import secrets
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.role import Role
from src.models.user import User
from src.models.verification import UserVerification


fake = Faker()


@pytest.fixture(scope="function")
async def seed_roles(db_session: AsyncSession) -> dict[str, Role]:
    """
    Seed basic system roles into the test database.
    Returns a dictionary mapping role names to their ORM instances.
    """
    roles_data = [
        Role(name="superadmin", description="Full system access", permissions={"all": True}),
        Role(name="admin", description="Administrative access", permissions={"user:read": True, "user:update": True}),
        Role(name="user", description="Standard user access", permissions={"user:read": True}),
    ]

    db_session.add_all(roles_data)
    await db_session.flush()

    return {role.name: role for role in roles_data}


@pytest.fixture(scope="function")
async def seed_user(db_session: AsyncSession, seed_roles: dict[str, Role]) -> User:
    """
    Seed a single standard verified user linked with the 'user' role.
    """
    test_user = User(
        id=uuid.uuid4(),
        name=fake.name(),
        email=fake.unique.email(),
        hashed_password="hashed_secure_password_123",
        is_active=True
    )
    test_user.roles.append(seed_roles["user"])

    db_session.add(test_user)
    await db_session.flush()
    return test_user


@pytest.fixture(scope="function")
async def seed_user_with_verification(db_session: AsyncSession, seed_user: User) -> User:
    """
    Adds dynamic email verification status record to the seeded user.
    """
    verification_record = UserVerification(
        user_id=seed_user.id,
        channel="email",
        destination=seed_user.email,
        is_verified=True,
        verification_value=secrets.token_urlsafe(32)
    )

    db_session.add(verification_record)
    await db_session.flush()
    return seed_user
