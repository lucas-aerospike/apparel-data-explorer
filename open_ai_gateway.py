import json
import time
from openai import OpenAI


SYSTEM = """You are a vintage fashion recommender for women's dresses.
    Task: pick the THREE closest matches in 'inventory' to the 'exemplar'.
    Judging criteria (in order):
    1) Silhouette/subcategory affinity (minidress ~ bodycon/shift > mumu/trapeze).
    2) Era proximity (1980s closest to late-70s/early-90s).
    3) Pattern match (solid vs plaid/striped/floral).
    4) Color family (exact or near jewel-tone match gets a bonus).
    5) Fabric/handfeel (smooth/stretchy cotton-blend ~ satin/poly jerseys > wool/flannel).
    6) Size tolerance: vintage can be tailored; +/-1–2 numeric or adjacent tee sizes are acceptable.
    Return STRICT JSON only with keys:
    - top3: array of 3 objects [{itemId, score (0..1), why}]
    - notes: one short paragraph explaining the trade-offs.
    """


def recommend(exemplar_id, catalog):
    client = OpenAI(
        api_key="")
    """
    Given a list of dress dictionaries and an exemplar itemId,
    call OpenAI to recommend the top-3 similar dresses.

    Returns: dict { "top3": [...], "notes": "..." }
    """
    exemplar = next((i for i in catalog if i["itemId"] == exemplar_id), None)
    if not exemplar:
        raise ValueError(f"Exemplar with itemId={exemplar_id} not found")

    inventory = [i for i in catalog if i["itemId"] != exemplar_id]

    USER = {"exemplar": exemplar, "inventory": inventory}

    schema = {
        "type": "object",
        "properties": {
            "top3": {
                "type": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "properties": {
                        "itemId": {"type": "integer"},
                        "score": {"type": "number"},
                        "why": {"type": "string"},
                    },
                    "required": ["itemId", "score", "why"],
                    "additionalProperties": False,
                },
            },
            "notes": {"type": "string"},
        },
        "required": ["top3", "notes"],
        "additionalProperties": False,
    }

    print("Making RAR (retrieval-augmented recommendation) call to OpenAI...")
    start = time.perf_counter( )

    resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": json.dumps(USER)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "Recommendations", "schema": schema},
        },
    )

    end = time.perf_counter( )
    print(f"OpenAPI call complete. Round trip time = {(end - start):.3f} sec.")

    return json.loads(resp.choices[0].message.content)
