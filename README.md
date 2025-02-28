# polymorphism-compare
Benchmarking Runtime vs Compile-Time Polymorphism for Different Compute Functions in C++

## Background
When discussing **compile-time vs runtime polymorphism** in C++, it’s often stated that compile-time polymorphism can be faster due to factors like function inlining, elimination of virtual table lookups, and better compiler optimizations. However, these discussions are frequently followed by a caveat: The actual performance difference depends on many factors, and profiling is necessary to determine whether compile-time polymorphism provides a meaningful advantage in any given use case.

As I thought about this, I started wondering: what specific comparisons had actually been reported? I expected to find the web, GitHub, and academic literature filled with benchmark results from developers evaluating whether compile-time polymorphism would benefit their specific use case. But after searching, I realized that **hard numbers were surprisingly difficult to find**. Most discussions acknowledge the potential differences, but very few provide concrete performance data.

## What This Project Does

### Compares Runtime vs Compile-Time Polymorphism Performance

This project benchmarks runtime vs compile-time polymorphism in C++ for two compute functions:
- **Simple Computation** – Fused Multiply-Add (FMA):
```
inline double ComputeFMA(double x) { return x * 1.414 + 2.718; }
```
- **Complex Computation** inolving Sin, Log and a Square Root:
```
inline double ComputeExpensive(double x) {
    return std::sin(x) * std::log(x + 1) + std::sqrt(x);
}
```
Each function is tested using:
- **Runtime polymorphism** via virtual function calls.
- **Compile-time polymorphism** using the Curiously Recurring Template Pattern (CRTP).
- **C++20 Concepts**  which enable compile-time type enforcement and selection, achieving behavior similar to polymorphism without inheritance.

### Provides a Template for Benchmarking Other Compute Functions

This project is designed with modularity and ease of modification in mind, making it a useful starting point for benchmarking compile-time vs. runtime polymorphism with other compute functions. The codebase provides a structured comparison framework that can be easily adapted to test additional operations.


## Getting Started

### Requirements

#### For Basic Execution Time Comparisons

- C++ compiler compatible with C++20 standard
- git
- cmake

#### For Detailed Profiling

- A Linux system with `perf` installed is required to perform the same profiling that is demonstrated in later sections.



### Building

#### Standard Build

Clone this repository and change working directory:

```shell
https://github.com/duanegoodner/polymorphism-compare
cd polymorphism-compare
```

Create the build directory:
```shell
mkdir build
```

Then generate the build system and compile:
```shell
cmake -B build
cmake --build build
```

#### CMake Configuration Options

The default compiler flags specified by `CMakeLists.txt` are `-O3 -march=native`. The following CMake confiuration options are also available.


| -D Option         | Compiler Flags |
|-------------------|---------------------------------|
| `ENABLE_DEBUG`      | `-O0 -g`                        |
| `ENABLE_NO_INLINE`  | `-O3 -march=native -fno-inline` |
| `ENABLE_LOW_OPT`    | `-O1 -march=native`             |
| `ENABLE_PROFILING`  | `-O3 -march=native -pg`         |
| `RESET_DEFAULTS`    | `-O3 -march=native`             |

For example, in the build command sequence shown above, if replace this:
```shell
cmake -B build
```
with this:
```shell
cmake -B build -DENABLE_PROFILING=ON
```
the compiler flags will be `-O3 -march=native -pg`.


### Running

#### Command Line Help

For help, run:
```shell
./build/bin/benchmark --help
```
Output:
```
Usage: ./build/bin/benchmark [polymorphism_category] [computation] [-n iterations] [-s]
 - No arguments: Runs all tests with the default iteration count.
 - With two arguments: Runs a specific test with the default iteration count.
 - With '-n iterations': Runs all tests with a custom iteration count.
 - With '-s': Saves execution time data.

Valid arguments:
 ------------------------
 Polymorphism Categories:
 ------------------------
  - concepts
  - crtp
  - runtime

 Compute Functions:
 ------------------
  - expensive
  - fma

Other Options:
  --help              Show this help message
  -n [iterations]     Specify a custom iteration count
  -s                  Save execution time data
```


#### Run All Tests

To run all possible combinations of polymorphism type and compute function, and save the execution time data, run: 
```shell
./build/bin/benchmark -s
```

Output:
```
Running: polymorphism_tests::TestRuntimeFMA
Iteration Count: 1000000000
FMA Computation: Runtime Polymorphism Time = 1.52441 seconds

Running: polymorphism_tests::TestRuntimeExpensive
Iteration Count: 1000000000
Expensive Computation: Runtime Polymorphism Time = 6.38158 seconds

Running: polymorphism_tests::TestCRTPFMA
Iteration Count: 1000000000
FMA Computation: CRTP Polymorphism Time = 0.378618 seconds

Running: polymorphism_tests::TestCRTPExpensive
Iteration Count: 1000000000
Expensive Computation: CRTP Polymorphism Time = 0.378513 seconds

Running: polymorphism_tests::TestConceptsFMA
Iteration Count: 1000000000
FMA Computation: C++20 Concepts Polymorphism Time = 0.378408 seconds

Running: polymorphism_tests::TestConceptsExpensive
Iteration Count: 1000000000
Expensive Computation: C++20 Concepts Polymorphism Time = 0.389357 seconds

Test results saved to: data/run_all_tests_results/2025-02-27-21-06-49-524.txt
```

#### Run a Single Test

To run a single test, we need to provide arguments identifying the polymorphism type and the compute function:

For example:
```
./build/bin/benchmark crtp expensive
```
Output:
```
Running: polymorphism_tests::TestCRTPExpensive
Iteration Count: 1000000000
Expensive Computation: CRTP Polymorphism Time = 0.391168 seconds
```

## Profiling with `perf`


### Build and Compile with Profiling On

```shell
cmake -B build -DENABLE_PROFILING=ON
cmake --build build
```

### Run Testing Shell Script

From the repo root, run:
```
./test/run_perf_tests.sh
```
This 



### Results

#### Execution Time Comparison


| Polymorphism Type | Compute Function | Execution Time (s) | Error (%) |
|-------------------|-----------------|--------------------|-----------|
| Runtime          | FMA             | 1.51796           | 0.19      |
| Runtime          | Expensive       | 6.41900           | 0.02      |
| CRTP             | FMA             | 0.379645          | 0.01      |
| CRTP             | Expensive       | 0.38203           | 0.53      |
| Concepts        | FMA             | 0.38525           | 0.29      |
| Concepts        | Expensive       | 0.379779         | 0.02      |

**Observations**
- Minimal performance difference between CRTP and Concepts
- CRTP and Concepts are ~4x faster than Runtime polymorphism for FMA and ~17x faster  for the Expensive computation

---

#### CPU Instructions and Branching Analysis

| Polymorphism Type | Compute Function | Instructions Retired (B) | Branches (B) | Branch Misses (K) |
|-------------------|-----------------|--------------------------|--------------|------------------|
| Runtime          | FMA             | 13.01                    | 3.00         | 25.12           |
| Runtime          | Expensive       | 154.02                   | 22.00        | 44.29           |
| CRTP             | FMA             | 4.00                     | 1.00         | 22.80           |
| CRTP             | Expensive       | 4.08                     | 1.02         | 28.36           |
| Concepts        | FMA             | 4.00                     | 1.00         | 22.84           |
| Concepts        | Expensive       | 4.00                     | 1.00         | 24.67           |

**Observations**
- Runtime polymorphism executes significantly more instructions than CRTP/Concepts
- Runtime polymorphism branch mispredictions are slightly higher than CRTP/Concepts for FMA and nearly ~2x higher for Expensive computation.
- For the FMA computation, CRTP and Conepts have ~same number of branch misses; but for Expensive computation, CRTP has ~15% more misses than Concepts.

---

#### Top-Down Performance Breakdown

| Polymorphism Type | Compute Function | Retiring (%) | Frontend Bound (%) | Backend Bound (%) |
|-------------------|-----------------|--------------|--------------------|-------------------|
| Runtime          | FMA             | 29.0         | 58.9               | 12.1              |
| Runtime          | Expensive       | 78.0         | 21.7               | 0.3               |
| CRTP             | FMA             | 25.0         | 2.4                | 72.6              |
| CRTP             | Expensive       | 25.0         | 2.5                | 72.4              |
| Concepts        | FMA             | 24.6         | 16.3               | 59.1              |
| Concepts        | Expensive       | 25.1         | 2.3                | 72.7              |

---

**Observations**
- Runtime is more frontend bound, especially for FMA (fetch latency issues) 
- CRTP and Concepts shift most execution to the backend (efficient execution unit use)

## Key Takeaways from `perf` Tests

<!-- ### **Observations**
- **Execution Time:** CRTP and Concepts approaches are significantly faster than runtime polymorphism.
- **Instruction Count:** CRTP and Concepts retire far fewer instructions compared to runtime.
- **Frontend Bound:** Runtime FMA has a high frontend-bound percentage (58.9%), while other methods see a lower impact.
- **Backend Bound:** CRTP and Concepts have a high backend-bound percentage (~72%), indicating execution stalls due to execution resource limitations. -->









