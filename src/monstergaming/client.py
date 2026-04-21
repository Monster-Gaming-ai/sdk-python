# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Luxedeum, LLC d/b/a Monster Gaming

"""Monster Gaming API client."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx


class MonsterGamingError(Exception):
    """Raised when the Monster Gaming API returns an error."""

    def __init__(self, message: str, status: int, body: Any = None):
        super().__init__(message)
        self.status = status
        self.body = body


@dataclass
class _ChatCompletions:
    _client: MonsterGaming

    def create(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        stop: str | list[str] | None = None,
    ) -> dict[str, Any]:
        """Create a chat completion.

        Args:
            model: Model ID (e.g. 'monster-gpt', 'claude-sonnet', 'gpt-4o').
            messages: List of message dicts with 'role' and 'content' keys.
            temperature: Sampling temperature (0-2).
            max_tokens: Maximum tokens to generate.
            top_p: Nucleus sampling parameter.
            stop: Stop sequence(s).

        Returns:
            OpenAI-compatible chat completion response dict.
        """
        payload: dict[str, Any] = {"model": model, "messages": messages}
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if stop is not None:
            payload["stop"] = stop

        return self._client._post("/v1/chat/completions", payload)


@dataclass
class _Chat:
    completions: _ChatCompletions


@dataclass
class _Models:
    _client: MonsterGaming

    def list(self) -> dict[str, Any]:
        """List available models.

        Returns:
            OpenAI-compatible model list response dict.
        """
        return self._client._get("/v1/models")


@dataclass
class MonsterGaming:
    """Client for the Monster Gaming API.

    Example::

        from monstergaming import MonsterGaming

        client = MonsterGaming(api_key="mg_your_api_key")
        response = client.chat.completions.create(
            model="monster-gpt",
            messages=[{"role": "user", "content": "Generate a Godot player controller"}],
        )
        print(response["choices"][0]["message"]["content"])
    """

    api_key: str
    base_url: str = "https://api.monstergaming.ai"
    timeout: float = 120.0
    chat: _Chat = field(init=False)
    models: _Models = field(init=False)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        completions = _ChatCompletions(_client=self)
        self.chat = _Chat(completions=completions)
        self.models = _Models(_client=self)

    def _request(self, method: str, path: str, json: Any = None) -> dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as http:
            resp = http.request(
                method,
                f"{self.base_url}{path}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=json,
            )

        if resp.status_code >= 400:
            body = None
            try:
                body = resp.json()
            except Exception:
                pass
            raise MonsterGamingError(
                f"Monster Gaming API error: {resp.status_code} {resp.reason_phrase}",
                status=resp.status_code,
                body=body,
            )

        return resp.json()

    def _get(self, path: str) -> dict[str, Any]:
        return self._request("GET", path)

    def _post(self, path: str, json: Any) -> dict[str, Any]:
        return self._request("POST", path, json=json)