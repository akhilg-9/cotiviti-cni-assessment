"""
"FUTURE / MULTIMODAL (LMM)" — read a scanned note image directly with Claude.

A large *multimodal* model removes the classic OCR -> NLP two-stage pipeline:
the model perceives the page and extracts structured clinical concepts in one
step. We send the scanned PNG straight to Claude's vision input and reuse the
same extraction contract as the text path.

Offline (no API key): we skip the real vision call and read the source text the
image was rendered from, so the demo still completes end-to-end.
"""

import base64
import json

from . import icd10, llm_extract
from .config import get_client, model
from .models import validate_conditions


def extract(image_path: str | list[str], offline_text: str | None = None):
    client = get_client()
    if client is None:
        # No key: fall back to the text the scan was rendered from.
        if offline_text is None:
            return []
        return [
            {**c, "method": "lmm/vision (offline simulation)"}
            for c in llm_extract.extract(offline_text)
        ]

    paths = [image_path] if isinstance(image_path, str) else image_path
    image_blocks = []
    for p in paths:
        with open(p, "rb") as f:
            img_b64 = base64.standard_b64encode(f.read()).decode("utf-8")
        image_blocks.append(
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}}
        )

    msg = client.messages.create(
        model=model(),
        max_tokens=4000,
        output_config={"format": {"type": "json_schema", "schema": llm_extract.SCHEMA}},
        messages=[{
            "role": "user",
            "content": [
                *image_blocks,
                {"type": "text", "text": llm_extract.PROMPT.format(
                    note=f"(see attached scanned image, {len(image_blocks)} page(s))")},
            ],
        }],
    )
    text = next(b.text for b in msg.content if b.type == "text")
    data = json.loads(text)
    conditions = validate_conditions(data["conditions"])
    return icd10.annotate([{**c, "method": "lmm/vision (Claude)"} for c in conditions])
