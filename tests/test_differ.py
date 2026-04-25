"""Tests for vault_diff.differ module."""

import pytest

from vault_diff.differ import SecretDiff, diff_many, diff_secrets


def test_no_diff_returns_unchanged():
    src = {"key": "value", "other": "123"}
    tgt = {"key": "value", "other": "123"}
    result = diff_secrets("app/config", src, tgt)
    assert not result.has_diff
    assert result.unchanged == src


def test_added_key():
    result = diff_secrets("app/config", {"a": "1"}, {"a": "1", "b": "2"})
    assert result.added == {"b": "2"}
    assert result.has_diff


def test_removed_key():
    result = diff_secrets("app/config", {"a": "1", "b": "2"}, {"a": "1"})
    assert result.removed == {"b": "2"}
    assert result.has_diff


def test_changed_key():
    result = diff_secrets("app/config", {"a": "old"}, {"a": "new"})
    assert result.changed == {"a": ("old", "new")}
    assert result.has_diff


def test_mixed_diff():
    src = {"keep": "same", "remove": "gone", "update": "v1"}
    tgt = {"keep": "same", "add": "new", "update": "v2"}
    result = diff_secrets("app/mixed", src, tgt)
    assert result.unchanged == {"keep": "same"}
    assert result.removed == {"remove": "gone"}
    assert result.added == {"add": "new"}
    assert result.changed == {"update": ("v1", "v2")}


def test_both_empty():
    result = diff_secrets("app/empty", {}, {})
    assert not result.has_diff


def test_diff_many_missing_path_treated_as_empty():
    results = diff_many(
        paths=["app/only-in-source", "app/only-in-target"],
        source_secrets={"app/only-in-source": {"x": "1"}},
        target_secrets={"app/only-in-target": {"y": "2"}},
    )
    assert len(results) == 2
    source_diff = next(r for r in results if r.path == "app/only-in-source")
    target_diff = next(r for r in results if r.path == "app/only-in-target")
    assert source_diff.removed == {"x": "1"}
    assert target_diff.added == {"y": "2"}
