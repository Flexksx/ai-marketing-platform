from __future__ import annotations

from collections.abc import Sequence
from functools import cached_property
from typing import cast

import httpx
import public
import pytest
from faker import Faker
from pydantic import BaseModel, ConfigDict
from supabase.client import AsyncClient

from tests.blackbox.supabase import SUPABASE_KEY, SUPABASE_URL, create_async_client
from tests.endpoints import BrandEndpoints


fake = Faker()

EVENT_LOOP_CLOSED_MESSAGE = "Event loop is closed"


def _is_event_loop_closed_error(exc: BaseException) -> bool:
    seen: set[int] = set()
    stack: list[BaseException] = [exc]
    while stack:
        current = stack.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        if isinstance(current, RuntimeError) and current.args == (
            EVENT_LOOP_CLOSED_MESSAGE,
        ):
            return True
        args = getattr(current, "args", ())
        msg = getattr(current, "message", "")
        if EVENT_LOOP_CLOSED_MESSAGE in args or msg == EVENT_LOOP_CLOSED_MESSAGE:
            return True
        for link in (
            getattr(current, "__cause__", None),
            getattr(current, "__context__", None),
        ):
            if link is not None:
                stack.append(link)
    return False


@public.add
class AuthenticatedUser(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: str
    email: str
    client: httpx.AsyncClient

    @cached_property
    def brands(self) -> BrandEndpoints:
        return BrandEndpoints(self.client)


async def _collect_cleanup_errors(
    actors: list[AuthenticatedUser],
    supabase: AsyncClient,
) -> list[BaseException]:
    errors: list[BaseException] = []
    for actor in actors:
        try:
            await actor.client.aclose()
        except BaseException as e:
            errors.append(e)
    for actor in actors:
        try:
            await supabase.auth.admin.delete_user(actor.user_id)
        except BaseException as e:
            errors.append(e)
    return errors


@public.add
@pytest.fixture
async def create_actor():
    actors: list[AuthenticatedUser] = []

    async def _make_actor():
        email = fake.unique.email()
        password = fake.password(length=12)

        supabase_client = await create_async_client(SUPABASE_URL, SUPABASE_KEY)
        try:
            user_response = await supabase_client.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "email_confirm": True,
                    "user_metadata": {"is_test": True},
                }
            )
            user_id = user_response.user.id

            session_response = await supabase_client.auth.sign_in_with_password(
                {"email": email, "password": password},
            )
            token = (
                session_response.session.access_token
                if session_response.session
                else None
            )
        finally:
            aclose = getattr(supabase_client, "aclose", None)
            if callable(aclose):
                await aclose()

        client = httpx.AsyncClient(
            base_url="http://localhost:8000",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )

        actor = AuthenticatedUser(client=client, user_id=user_id, email=email)
        actors.append(actor)
        return actor

    yield _make_actor

    supabase_client = await create_async_client(SUPABASE_URL, SUPABASE_KEY)
    try:
        cleanup_errors = await _collect_cleanup_errors(actors, supabase_client)
    finally:
        aclose = getattr(supabase_client, "aclose", None)
        if callable(aclose):
            await aclose()
    unexpected_errors = [
        e for e in cleanup_errors if not _is_event_loop_closed_error(e)
    ]
    if unexpected_errors:
        raise ExceptionGroup(
            "actor cleanup failed",
            cast(Sequence[Exception], unexpected_errors),
        )
