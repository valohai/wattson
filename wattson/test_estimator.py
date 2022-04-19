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


def test_complete_estimate() -> None:
    instance_type = "a1.large"
    region = "ap-northeast-1"
    hours = 3
    load = 50

    result = estimate_carbon_emissions(
        instance_type=instance_type,
        hours=hours,
        load_percentage=load,
        region=region,
    )

    # Cross-validate with a known example from Teads calculator
    assert round(result.scope_2_co2eq + result.scope_3_co2eq, 1) == 22.8
