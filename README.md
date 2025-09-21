# High-Level-Synthesis-Dataset
This repository provides part of the source code used for the generation and analysis of the GNΩSIS dataset

DATASET:
https://huggingface.co/datasets/aferikoglou/GNWSIS/tree/main

https://huggingface.co/datasets/aferikoglou/GNWSIS/resolve/main/GN%CE%A9SIS.csv

## Окружение

Использую Miniconda + Poetry.

### Установка окружения
bash
brew install --cask miniconda
conda create -n my_env python=3.13 pip
conda activate my_env
pip install poetry
poetry install --no-root

Запуск
python3 data_loader.py

Dataset Schema
The GNΩSIS dataset is organized as a CSV file, where each row corresponds to a distinct hardware design configuration for a specific application, targeting a particular FPGA and clock frequency. It includes both configuration parameters and associated performance and resource utilization metrics.

Configuration Parameters
These columns define the application context and the design parameters:

Application_Name: The name of the application being analyzed.
Version: Identifier for a specific version or configuration of the application.
Device: The target FPGA device (e.g., xczu7ev-ffvc1156-2-e, xcu200-fsgd2104-2-e).
Clock_Period_nsec: The clock period for the design, in nanoseconds.
Applied Directives
These fields indicate which design directives have been applied to specific action points within the kernel:

Array_1 to Array_22: Represent directives applied to array-related action points (e.g., complete_1).
OuterLoop_1 to OuterLoop_26 and InnerLoop_1_1 to InnerLoop_4_2: Capture loop-specific directives such as pipeline_1 or unroll_2.
QoR Metrics
Latency_msec: Kernel execution latency, measured in milliseconds.
Synthesis_Time_sec: Total time taken to synthesize the design, in seconds.
BRAM_Utilization_percentage, DSP_Utilization_percentage, FF_Utilization_percentage, LUT_Utilization_percentage: Resource usage reported as a percentage of the total available on the target FPGA device.
Speedup: Performance improvement factor compared to a baseline implementation.
BRAMs, DSPs, FFs, LUTs: Calculated absolute resource usage based on utilization percentage and the FPGA's total capacity.
