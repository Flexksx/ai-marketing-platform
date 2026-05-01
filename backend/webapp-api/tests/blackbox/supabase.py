import os

import public
import pytest
from dotenv import load_dotenv
from supabase import create_async_client
from supabase.client import AsyncClient


load_dotenv()

SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL") or ""
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""


@public.add
@pytest.fixture
async def supabase_service_client() -> AsyncClient:
    return await create_async_client(SUPABASE_URL, SUPABASE_KEY)
