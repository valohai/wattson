import pytest

from wattson.data import instance_data, region_data
from wattson.estimator import (
    calculate_scope_2,
    calculate_scope_3,
    compute_load_to_kwh,
    estimate_carbon_emissions,
)

SAMPLE_INSTANCE = instance_data["db.m4.10xlarge"]
SAMPLE_REGION = region_data["eu-north-1"]


def test_calculate_scope_2() -> None:
    with_PUE = 245.6 * 1.2
    expected_result = with_PUE / 1000 * 1 * 8
    result = calculate_scope_2(
        instance=SAMPLE_INSTANCE, region=SAMPLE_REGION, hours=1, load=50
    )
    assert result == expected_result
    # Cross-validate with a known example from Teads calculator
    assert round(result, 1) == 2.4


def test_calculate_scope_3() -> None:
    result = calculate_scope_3(instance=SAMPLE_INSTANCE, hours=1)
    # Cross-validate with a known example from Teads calculator
    assert result == 34.5


def test_lerp() -> None:
    assert round(compute_load_to_kwh(SAMPLE_INSTANCE.load_to_kwh, 25)) == 190


@pytest.mark.parametrize(
    ("region", "has_compensation", "expected_emissions"),
    [
        ("ca-central-1", True, 14.1),
        ("eu-north-1", False, 11.3),
        ("ap-northeast-1", False, 22.8),
    ],
)
def test_complete_estimate(
    region: str, has_compensation: bool, expected_emissions: float
) -> None:
    instance_type = "a1.large"
    hours = 3
    load = 50

    result = estimate_carbon_emissions(
        instance_type=instance_type,
        hours=hours,
        load_percentage=load,
        region=region,
    )

    # Cross-validate with a known example from Teads calculator
    assert round(result.scope_2_co2eq + result.scope_3_co2eq, 1) == expected_emissions
    assert (
        "has been compensated by renewable energy credits" in result.details
    ) == has_compensation
    assert result.compensated == has_compensation


# fmt: off
@pytest.mark.parametrize("value_set", [
    dict(region="xx-mars", instance_type="db.m4.10xlarge", hours=1),
    dict(region="eu-north-1", instance_type="deep.thought", hours=1),
    dict(region="eu-north-1", instance_type="db.m4.10xlarge", hours=-1),
    dict(region="eu-north-1", instance_type="db.m4.10xlarge", hours=1, load_percentage=1500),  # noqa: E501
])
# fmt: on
def test_nonsensical_values(value_set: dict) -> None:  # type: ignore[type-arg]
    with pytest.raises(ValueError):
        estimate_carbon_emissions(**value_set)
