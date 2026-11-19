from feast import Entity

digit = Entity(
    name="digit_id",
    join_keys=["digit_id"],
    description="Unique row identifier for one handwritten digit example",
)
