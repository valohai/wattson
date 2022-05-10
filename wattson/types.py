import dataclasses
from typing import Dict


@dataclasses.dataclass(frozen=True)
class EmissionsEstimation:
    data_license: str
    region: str
    hours: float
    avg_load: float
    instance_type: str
    scope_2_co2eq: float
    scope_3_co2eq: float
    compensated: bool
    details: str


@dataclasses.dataclass(frozen=True)
class RegionData:
    region: str
    co2eq_g_per_kwh: float
    pue: float


@dataclasses.dataclass(frozen=True)
class InstanceData:
    instance_type: str
    load_to_kwh: Dict[int, float]
    manufacture_co2eq_g_per_hour: float
