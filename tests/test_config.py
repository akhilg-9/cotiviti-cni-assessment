"""Config + prompt loading + schema (runs fully offline)."""

import pytest

from src import config
from src.models import Condition


def test_prompts_load_v1():
    p = config.prompts("v1")
    assert p["version"] == "v1"
    assert "{note}" in p["extraction"]["system"]


def test_model_is_a_string():
    assert isinstance(config.model(), str) and config.model()


def test_condition_validates_and_rejects_bad_confidence():
    c = Condition(name="Type 2 diabetes mellitus", icd10="E11.9",
                  status="active", evidence="diabetes", confidence=0.9)
    assert c.icd10 == "E11.9"
    with pytest.raises(Exception):
        Condition(name="x", icd10="y", status="active", evidence="z", confidence=2.0)
