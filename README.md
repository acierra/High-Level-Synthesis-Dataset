# High-Level-Synthesis-Dataset
This repository provides part of the source code used for the generation and analysis of the GNΩSIS dataset

## DATASET:
https://huggingface.co/datasets/aferikoglou/GNWSIS/tree/main

https://huggingface.co/datasets/aferikoglou/GNWSIS/resolve/main/GN%CE%A9SIS.csv

Модульный ETL-пакет для обработки и анализа данных о проектах High-Level Synthesis (FPGA/HLS), включая этапы загрузки, валидации, преобразования и выгрузки данных в PostgreSQL и Parquet.
Проект реализует полный цикл работы с данными:

Extract – загрузка и валидация исходного CSV.

Transform – базовые преобразования и очистка данных.

Validate – проверка корректности данных.

Load – выгрузка в PostgreSQL и Parquet.

Main – объединение всех шагов через CLI-интерфейс.

EDA и визуализация – исследование и представление данных.

## Окружение

Использую Miniconda + Poetry.

## Установка окружения
bash
brew install --cask miniconda
conda create -n my_env python=3.13 pip
conda activate my_env
pip install poetry
poetry install --no-root
pip install pandas numpy sqlalchemy psycopg2-binary pyarrow matplotlib seaborn jupyter

## Запуск
python -m etl.main \
  --csv notebook/newdata/gnwsis_clean.csv \
  --creds creds.db \
  --table kuchieva \
  --rawdir data/raw \
  --outdir data/processed \
  --limit 100


![docs/Screenshot 2025-09-22 at 01.22.42.png](https://github.com/acierra/High-Level-Synthesis-Dataset/blob/main/docs/Screenshot%202025-09-22%20at%2001.22.42.png)
![docs/Screenshot%202025-09-30%20at%2011.29.08.png](https://github.com/acierra/High-Level-Synthesis-Dataset/blob/main/docs/Screenshot%202025-09-30%20at%2011.29.08.png)

## Dataset Schema
The GNΩSIS dataset is organized as a CSV file, where each row corresponds to a distinct hardware design configuration for a specific application, targeting a particular FPGA and clock frequency. It includes both configuration parameters and associated performance and resource utilization metrics.

## Configuration Parameters
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

## EDA и визуализации

- Ноутбук: `notebook/EDA.ipynb`
- Статические графики: папка `docs/plots/` (автогенерация скриптом `viz_seaborn.py`)
- Датасет: FPGA HLS (сводная таблица синтезов). Поля:
  - `Speedup` — ускорение реализации на ПЛИС относительно базовой реализации (больше — лучше)
  - `Latency_msec` — задержка исполнения, мс (меньше — лучше)
  - `Clock_Period_nsec` — целевой тактовый период синтеза, нс
  - `LUTs`, `FFs`, `DSPs`, `BRAMs` — потребление базовых ресурсов ПЛИС
  - `*_Utilization_percentage` — доля использования ресурса, %
  - `Application_Name`, `Version`, `Device` — метаданные проекта и чипа

### Быстрый рендер графиков
```bash
python3 viz_seaborn.py --csv notebook/newdata/gnwsis_clean.csv --out docs/plots

