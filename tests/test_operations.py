from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    url = "/operations"
    response = await ac.post(url, json={
        "id": 1,
        "quantity": "25.5",
        "figi": "figi_CODE",
        "instrument_type": "bond",
        "date": "2023-02-01T00:00:00",
        "type": "Coupon payment",
    })

    assert response.status_code == 200, "Operation wasn't created"


async def test_get_specific_operations(ac: AsyncClient):
    url = "/operations"
    response = await ac.get(url, params={
        "operation_type": "Coupon payment",
    })

    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) == 1


async def test_get_all_users(ac: AsyncClient):
    url = "/operations/get_all_users"
    response = await ac.get(url)

    assert response.status_code == 200
