#include "utils.hpp"
#include "crtp_polymorphism.hpp"

namespace crtp_polymorphism {

template <typename T>
void TestCRTPPolymorphism(const std::string &label, size_t n) {
  RunBenchmark(label + " CRTP Polymorphism", n, [](double x) {
    return T().Compute(x);
  });
}

// Explicit template instantiations
template void TestCRTPPolymorphism<PolyFMA>(const std::string &, size_t);
template void TestCRTPPolymorphism<PolyExpensive>(const std::string &, size_t);

} // namespace crtp_polymorphism
