from typing import Dict

from wattson.data import data_license, instance_data, region_data
from wattson.types import EmissionsEstimation, InstanceData, RegionData


def compute_load_to_kwh(
    load_to_kwh: Dict[int, float],
    load_percentage: float,
) -> float:
    # if load in instance.load_to_kwh, return it directly
    if int(load_percentage) in load_to_kwh:
        return load_to_kwh[int(load_percentage)]
    # otherwise, linearly interpolate it from  the nearest values
    sorted_loads = sorted(load_to_kwh)
    for i, load in enumerate(sorted_loads):
        if load < load_percentage < sorted_loads[i + 1]:
            return lerp_load_to_kwh(
                load_to_kwh, load_percentage, load, sorted_loads[i + 1]
            )
    raise ValueError(
        f"Load percentage {load_percentage} not valid for data {load_to_kwh}"
    )


def lerp_load_to_kwh(
    load_to_kwh: Dict[int, float],
    load_percentage: float,
    low_load: int,
    high_load: int,
) -> float:
    low_kwh = load_to_kwh[low_load]
    high_kwh = load_to_kwh[high_load]
    # linearly interpolate between min_load and max_load
    return low_kwh + (high_kwh - low_kwh) * (load_percentage - low_load) / (
        high_load - low_load
    )


def calculate_scope_2(
    instance: InstanceData,
    region: RegionData,
    hours: float,
    load: float,
) -> float:
    """
    Calculates the scope 2 carbon emissions.

    :return: The estimated carbon emissions in grams CO2eq.
    """
    electricity_consumption_per_hour = compute_load_to_kwh(instance.load_to_kwh, load)
    electricity_consumption_with_PUE = electricity_consumption_per_hour * region.pue
    return electricity_consumption_with_PUE / 1000 * hours * region.co2eq_g_per_kwh


def calculate_scope_3(instance: InstanceData, hours: float) -> float:
    return instance.manufacture_co2eq_g_per_hour * hours


def estimate_carbon_emissions(
    region: str, hours: float, instance_type: str, load_percentage: float = 50
) -> EmissionsEstimation:
    """
    Estimates the carbon emissions of a given region and instance type.
    :param region: AWS region used.
    :param hours: Execution time in hours.
    :param instance_type: The instance type used.
    :param load_percentage: The instance average CPU load % 0-100.
    :return: The estimated carbon emissions in eCO2eq.
    """

    instance = instance_data.get(instance_type)
    region_details = region_data.get(region)

    if not instance:
        raise ValueError(f"Instance type {instance_type} not found.")

    if not region_details:
        raise ValueError(f"Region {region} not found.")

    if not 0 <= load_percentage <= 100:
        raise ValueError(f"Load percentage {load_percentage} not valid.")

    return EmissionsEstimation(
        region=region,
        hours=hours,
        instance_type=instance_type,
        avg_load=load_percentage,
        scope_2_co2eq=calculate_scope_2(
            instance=instance,
            region=region_details,
            hours=hours,
            load=load_percentage,
        ),
        scope_3_co2eq=calculate_scope_3(instance=instance, hours=hours),
        data_license=data_license,
    )
