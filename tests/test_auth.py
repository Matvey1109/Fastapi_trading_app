from sqlalchemy import insert, select
from src.auth.models import role
from tests.conftest import client, async_session_maker


# >>> pytest -v -s tests/

async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name="admin", permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], "Role wasn't added"


def test_register():
    url = "/auth/register"
    response = client.post(url, json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 0
    })

    assert response.status_code == 201, "User wasn't registered"
