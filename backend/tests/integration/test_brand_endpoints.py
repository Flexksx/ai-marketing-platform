from pathlib import Path

import pytest

from tests.blackbox import AuthenticatedUser
from tests.blackbox.brands import BrandMockFactory
from vozai.domain.brand import (
    BrandColor,
    BrandCreateRequest,
    BrandData,
    BrandNotFoundError,
    BrandUpdateRequest,
)


CURRENT_DIR = Path(__file__).parent
RESOURCES_PATH = CURRENT_DIR / "res"
LOGO1_PATH = Path(RESOURCES_PATH, "logo1.png")
LOGO2_PATH = Path(RESOURCES_PATH, "logo2.jpg")


@pytest.mark.asyncio
async def test_create_brand(create_actor):
    user: AuthenticatedUser = await create_actor()
    brand_data = BrandMockFactory.create_brand_data()
    brand = await user.brands.create(
        brand=BrandCreateRequest(name="Test Brand", data=brand_data)
    )
    assert brand.name == "Test Brand"
    assert brand.data == brand_data


@pytest.mark.asyncio
async def test_update_brand(create_actor):
    user: AuthenticatedUser = await create_actor()
    brand_data = BrandMockFactory.create_brand_data()
    brand = await user.brands.create(
        brand=BrandCreateRequest(name="Test Brand", data=brand_data)
    )
    assert brand.name == "Test Brand"
    assert brand.data == brand_data

    new_data = BrandMockFactory.create_brand_data()
    new_data.colors = [BrandColor(name="New Color", hex_value="#FF0000")]

    updated_brand = await user.brands.update(
        brand_id=brand.id,
        update_request=BrandUpdateRequest(
            name="Updated Brand", data=BrandData(colors=new_data.colors)
        ),
    )
    assert updated_brand.name == "Updated Brand"
    assert updated_brand.data.colors[0].hex_value == "#FF0000"

    assert updated_brand.data.description == brand_data.description
    assert updated_brand.data.audiences == brand_data.audiences


@pytest.mark.asyncio
async def test_delete_brand(create_actor):
    user: AuthenticatedUser = await create_actor()
    brand_data = BrandMockFactory.create_brand_data()
    brand = await user.brands.create(
        brand=BrandCreateRequest(name="Test Brand", data=brand_data)
    )
    assert brand.name == "Test Brand"
    assert brand.data == brand_data

    await user.brands.delete(brand_id=brand.id)

    brands = await user.brands.search()
    assert len(brands) == 0


@pytest.mark.asyncio
async def test_accessing_a_different_user_brand_raises_error(create_actor):
    user1: AuthenticatedUser = await create_actor()
    user2: AuthenticatedUser = await create_actor()

    brand_data = BrandMockFactory.create_brand_data()
    brand = await user1.brands.create(
        brand=BrandCreateRequest(name="Test Brand", data=brand_data)
    )
    assert brand.name == "Test Brand"
    assert brand.data == brand_data

    with pytest.raises(BrandNotFoundError):
        await user2.brands.get(brand_id=brand.id)


@pytest.mark.asyncio
async def test_update_brand_logo(create_actor):
    user: AuthenticatedUser = await create_actor()
    brand_data = BrandMockFactory.create_brand_data()

    brand = await user.brands.create(
        brand=BrandCreateRequest(name="Test Brand", data=brand_data)
    )

    logo_bytes = LOGO1_PATH.read_bytes()

    logo_tuple = (LOGO1_PATH.name, logo_bytes, "image/png")

    updated_brand = await user.brands.update(brand_id=brand.id, logo_file=logo_tuple)

    assert updated_brand.data.logo_url is not None
    assert f"{brand.id}" in updated_brand.data.logo_url

    logo2_tuple = (LOGO2_PATH.name, LOGO2_PATH.read_bytes(), "image/jpeg")

    final_brand = await user.brands.update(brand_id=brand.id, logo_file=logo2_tuple)

    assert final_brand.data.logo_url is not None
    assert f"{brand.id}" in final_brand.data.logo_url
