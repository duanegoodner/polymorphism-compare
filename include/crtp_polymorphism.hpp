// Declarations and templates for CRTP-based polymorphism.

#pragma once

#include "benchmark_utils.hpp"
#include "math_functions.hpp"

namespace crtp_polymorphism {

template <typename Derived>
class CRTPBase {
 public:
  double Compute(double x) const {
    return static_cast<const Derived*>(this)->ComputeImpl(x);
  }
};

 class PolyFMA : public CRTPBase<PolyFMA> {
  public:
   double ComputeImpl(double x) const { return ComputeFMA(x); }
 };

class PolyExpensive : public CRTPBase<PolyExpensive> {
 public:
  double ComputeImpl(double x) const { return ComputeExpensive(x); }
};

template <typename T>
void TestCRTPPolymorphism(const std::string &label, size_t n, T &obj) {
  RunBenchmark(label + " CRTP Polymorphism", n, [&](double x) {
    return obj.Compute(x);
  });
}

} // namespace crtp_polymorphism
