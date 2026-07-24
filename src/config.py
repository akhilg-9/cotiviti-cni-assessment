"""
Central configuration: environment + versioned prompt config + Claude client.

Loads `.env` (if present) and `prompts/<version>.yaml`, and exposes the model
id, the Anthropic client, and a "are we live or offline?" check. Mirrors the
config.py / prompts/*.yaml split of the reference project.
"""

import functools
import os
from pathlib import Path

import yaml

try:  # optional, but recommended (pip install python-dotenv)
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = Path(os.environ.get("CNI_PROMPTS_DIR", ROOT / "prompts"))
PROMPT_VERSION = os.environ.get("CNI_PROMPT_VERSION", "v1")


@functools.lru_cache(maxsize=None)
def prompts(version: str = PROMPT_VERSION) -> dict:
    with open(PROMPTS_DIR / f"{version}.yaml") as f:
        return yaml.safe_load(f)


def model() -> str:
    """Model id, overridable via CNI_MODEL."""
    return os.environ.get("CNI_MODEL") or prompts()["model"]["extraction_model"]


def have_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def get_client():
    """Return an Anthropic client, or None if the SDK/key isn't available.

    Retries and a hard timeout are set here so every call site inherits
    them — a transient overload or network blip must not crash a demo run.
    """
    if not have_api_key():
        return None
    try:
        import anthropic
    except ImportError:
        return None
    return anthropic.Anthropic(max_retries=4, timeout=60.0)
