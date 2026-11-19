from pathlib import Path

from feast import FeatureView, Field, FileSource
from feast.types import Float32, Int64

from entities import digit

ROOT = Path(__file__).resolve().parents[1]

SOURCE = FileSource(
    path=str(
        ROOT / "data" / "processed" / "features.parquet"
    ),
    timestamp_field="event_timestamp",
)

pixel_fields = [
    Field(name=f"pixel_{i}", dtype=Float32)
    for i in range(64)
]

digit_features = FeatureView(
    name="digit_features",
    entities=[digit],
    schema=pixel_fields + [
        Field(name="label", dtype=Int64)
    ],
    source=SOURCE,
    ttl=None,
    online=True,
    tags={"project": "handwritten-digits"},
)
