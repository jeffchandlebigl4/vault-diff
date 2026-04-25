"""Core diffing logic for comparing secrets between two Vault namespaces."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SecretDiff:
    path: str
    added: dict[str, Any] = field(default_factory=dict)
    removed: dict[str, Any] = field(default_factory=dict)
    changed: dict[str, tuple[Any, Any]] = field(default_factory=dict)
    unchanged: dict[str, Any] = field(default_factory=dict)

    @property
    def has_diff(self) -> bool:
        return bool(self.added or self.removed or self.changed)


def diff_secrets(
    path: str,
    source: dict[str, Any],
    target: dict[str, Any],
) -> SecretDiff:
    """Compare two secret dicts and return a structured SecretDiff."""
    result = SecretDiff(path=path)

    all_keys = source.keys() | target.keys()

    for key in all_keys:
        in_source = key in source
        in_target = key in target

        if in_source and not in_target:
            result.removed[key] = source[key]
        elif in_target and not in_source:
            result.added[key] = target[key]
        elif source[key] != target[key]:
            result.changed[key] = (source[key], target[key])
        else:
            result.unchanged[key] = source[key]

    return result


def diff_many(
    paths: list[str],
    source_secrets: dict[str, dict[str, Any]],
    target_secrets: dict[str, dict[str, Any]],
) -> list[SecretDiff]:
    """Diff multiple secret paths at once. Missing paths count as empty dicts."""
    return [
        diff_secrets(
            path=p,
            source=source_secrets.get(p, {}),
            target=target_secrets.get(p, {}),
        )
        for p in paths
    ]
