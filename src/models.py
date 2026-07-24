"""
Typed schema for an extracted condition (pydantic), and the JSON schema handed
to Claude's structured-output mode. Keeping these together means the prompt
contract and the validation contract can't drift apart.
"""

from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["active", "historical", "negated", "uncertain"]


class Condition(BaseModel):
    name: str
    icd10: str
    status: Status
    evidence: str
    confidence: float = Field(ge=0.0, le=1.0)


def validate_conditions(raw_conditions: list) -> list[dict]:
    """Parse raw LLM output through the pydantic model — defense in depth
    behind the API-side schema (e.g. confidence must land in [0, 1])."""
    return [Condition(**c).model_dump() for c in raw_conditions]


# JSON schema for the Anthropic structured-output `output_config.format`.
# (Hand-written rather than derived, so we control additionalProperties/required
# exactly as the API requires.)
EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "conditions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "icd10": {"type": "string"},
                    "status": {"type": "string", "enum": list(Status.__args__)},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["name", "icd10", "status", "evidence", "confidence"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["conditions"],
    "additionalProperties": False,
}
