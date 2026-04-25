"""Vault client wrapper for reading secrets from namespaces."""

import os
from typing import Any

import hvac


class VaultClient:
    """Thin wrapper around hvac.Client scoped to a namespace."""

    def __init__(self, url: str, token: str, namespace: str | None = None) -> None:
        self.url = url
        self.namespace = namespace
        self._client = hvac.Client(
            url=url,
            token=token,
            namespace=namespace,
        )

    @classmethod
    def from_env(cls, namespace: str | None = None) -> "VaultClient":
        """Build a client from standard Vault environment variables."""
        url = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
        token = os.environ["VAULT_TOKEN"]
        return cls(url=url, token=token, namespace=namespace)

    def is_authenticated(self) -> bool:
        return self._client.is_authenticated()

    def read_secret(self, path: str, mount_point: str = "secret") -> dict[str, Any]:
        """Read a KV-v2 secret and return its data dict."""
        response = self._client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point=mount_point,
        )
        return response["data"]["data"]

    def list_secrets(self, path: str, mount_point: str = "secret") -> list[str]:
        """List secret keys under a path."""
        response = self._client.secrets.kv.v2.list_secrets(
            path=path,
            mount_point=mount_point,
        )
        return response["data"]["keys"]
