# Valohai Wattson 🔌⚡

![PyPI](https://img.shields.io/pypi/v/valohai-wattson)
![PyPI - MIT License](https://img.shields.io/pypi/l/valohai-wattson)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/valohai/wattson/CI)
![Codecov](https://img.shields.io/codecov/c/github/valohai/wattson)

## About

Wattson is a Python library for estimating cloud compute carbon emissions.

It currently supports estimating emissions for a range of Amazon EC2 instances in a variety of regions.

## Usage
You can install this package with pip by running `pip install valohai-wattson`.

If you are currently using AWS instances, you can calculate the carbon emissions for your instances using the following code:
```
from wattson import estiamte_carbon_emissions

training_emissions = estimate_carbon_emissions(
    instance_type='c4.2xlarge',
    region='us-east-1',
    hours=1,
    load_percentage=0.5,
)
```
The returned value will be of the type `wattson.EmissionsEstimation` and have the following information:
- `data_license`: The license of the data used to estimate the emissions.
- `region`: The region the original computation was performed in.
- `instance_type`: The instance type of the original computation.
- `avg_load`: The average CPU load during the original computation (defaults to 50% if not specified).
- `scope_2_co2eq`: The estimated CO2 emissions for the electricity used in the original computation.
- `scope_3_co2eq`: The estimated CO2 emissions for manufacturing of the device used in the original computation, assuming a 4-year usage.
- `compensated`: Were any of the emissions of the original computation compensated using e.g. carbon emissions compensation or renewable energy credits.
- `details`: Any additional details about e.g. the compensation methodology.

## Acknowledgements

This project uses the [EC2 Carbon Emissions Dataset by Teads Engineering](https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/).

## Licenses

- The library code is **Copyright (c) 2022 Valohai, licensed under the MIT License.**
- The Teads Engineering EC2 Carbon Emissions Dataset is **licensed under the Creative Commons Attribution 4.0 International License.**
