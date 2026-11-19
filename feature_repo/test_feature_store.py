from pathlib import Path
import sys

import pandas as pd
from feast import FeatureStore

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "feature_repo"

sys.path.insert(0, str(REPO))

from entities import digit
from digit_features import digit_features


def main():

    store = FeatureStore(repo_path=str(REPO))

    source = pd.read_parquet(
        ROOT / "data" / "processed" / "features.parquet"
    )

    print("Total records:", len(source))

    store.apply([
        digit,
        digit_features
    ])

    print("Feast entity and feature view registered!")

    start = pd.Timestamp(
        "2023-12-31T00:00:00Z"
    ).to_pydatetime()

    end = pd.Timestamp(
        "2024-01-02T00:00:00Z"
    ).to_pydatetime()

    store.materialize(
        start_date=start,
        end_date=end
    )

    print("Features materialized successfully!")

    entity_rows = [
        {"digit_id": 0}
    ]

    result = store.get_online_features(
        features=[
            "digit_features:pixel_0",
            "digit_features:pixel_1",
            "digit_features:label"
        ],
        entity_rows=entity_rows
    ).to_dict()

    print("Feast online lookup:", result)

    assert result["digit_id"] == [0]

    assert result["label"][0] in range(10)

    assert result["pixel_0"][0] is not None

    assert result["pixel_1"][0] is not None


    print("Feast smoke test: PASSED")


if __name__ == "__main__":
    main()
