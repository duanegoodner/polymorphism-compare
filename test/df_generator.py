from pathlib import Path

import pandas as pd
import re


def parse_benchmark_results(output):
    benchmark_summary = {}

    # Extract test name and iteration count from first part
    benchmark_pattern = re.compile(
        r"Running: (?P<test_name>.*?)\n"
        r"Iteration Count: (?P<iteration_count>\d+)"
    )
    matches = benchmark_pattern.findall(output)

    if matches:
        test_name, iteration_count = matches[0]
        benchmark_summary["Test Name"] = test_name
        benchmark_summary["Mean Iteration Count"] = int(iteration_count)

    # Extract mean time from the last part
    time_pattern = re.search(r"(\d+\.\d+) \+\- (\d+\.\d+) seconds time elapsed", output)
    if time_pattern:
        benchmark_summary["Mean Time (seconds)"] = (float(time_pattern.group(1)), float(time_pattern.group(2)))

    return benchmark_summary


def parse_performance_counters(output):
    perf_results = {}

    # Extract the performance counter section only
    perf_section_match = re.search(r"Performance counter stats for .*?:\n(.*?)(?:\n\n|$)", output, re.DOTALL)
    if not perf_section_match:
        return {}
    perf_section = perf_section_match.group(1)

    perf_pattern = re.compile(
        r"(?P<value>[\d,]+)\s+(?P<metric>[\w\./_\-]+)\s+(?:\( \+\-\s*(?P<error>-?\d+\.\d+)% \))?"
    )

    for match in perf_pattern.finditer(perf_section):
        value = match.group("value").replace(",", "")
        error = match.group("error")
        perf_results[match.group("metric")] = (
        int(value) if value.isdigit() else None, float(error) if error is not None else None)

    return perf_results


def perf_output_to_series(file_path: Path):
    with file_path.open(mode="r") as file:
        output = file.read()

    benchmark_summary = parse_benchmark_results(output)
    perf_results = parse_performance_counters(output)

    combined_results = {**benchmark_summary, **perf_results}
    return pd.Series(combined_results)


if __name__ == "__main__":
    my_file_path = (
        Path(__file__).parent.parent
        / "data"
        / "perf"
        / "2025-03-15_17-16-44"
        / "crtp_fma_perf_summary.txt"
    )

    my_series = perf_output_to_series(my_file_path)

