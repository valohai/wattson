import csv
import io
from dataclasses import replace
from typing import Dict

import black

from wattson.types import InstanceData, RegionData


def get_regions() -> list[dict[str, str]]:
    with open("data/aws_regions_intensity.csv") as f:
        regions_data = list(csv.DictReader(f))
    return regions_data


def get_instances() -> list[dict[str, str]]:
    with open("data/aws_instances_dataset.csv") as f:
        instances_data = list(csv.DictReader(f))
    return instances_data


def convert_to_float(value: str) -> float:
    return float(value.replace(",", "."))


def convert_region_data() -> Dict[str, RegionData]:
    regions = get_regions()
    region_data = {}
    for region in regions:
        name = region["Region"]
        region_data[name] = RegionData(
            region=name,
            co2eq_g_per_kwh=convert_to_float(region["CO2e (metric gram/kWh)"]),
            pue=convert_to_float(region["PUE"]),
        )
    return region_data


INSTANCE_LOAD_KEYS = {
    "Instance @ Idle": 0,
    "Instance @ 10%": 10,
    "Instance @ 50%": 50,
    "Instance @ 100%": 100,
}


def convert_instance_data() -> Dict[str, InstanceData]:
    instances = get_instances()
    instance_data = {}
    for instance in instances:
        name = instance["Instance type"]
        instance_data[name] = InstanceData(
            instance_type=name,
            load_to_kwh={
                load: convert_to_float(instance[key])
                for key, load in INSTANCE_LOAD_KEYS.items()
                if key in instance
            },
            manufacture_co2eq_g_per_hour=convert_to_float(
                instance["Instance Hourly Manufacturing Emissions (gCO₂eq)"]
            ),
        )
    return instance_data


def main():
    out = io.StringIO()
    print(
        """
# This file is generated by wattson_datagen/generate.py.
# Do not edit this file directly.

# fmt: on

from wattson.types import InstanceData, RegionData

data_license = "Teads Engineering, CC BY 4.0"
    """.strip(),
        file=out,
    )
    print("region_data=", convert_region_data(), file=out)
    print("instance_data=", convert_instance_data(), file=out)
    res = black.format_str(out.getvalue(), mode=black.FileMode(line_length=120))
    with open("wattson/data.py", "w") as f:
        f.write(res.replace("# fmt: on", "# fmt: off"))


if __name__ == "__main__":
    main()
