#include <pybind11/pybind11.h>

#include <goofit/BinnedDataSet.h>
#include <goofit/PDFs/basic/SmoothHistogramPdf.h>
#include <goofit/Variable.h>

using namespace GooFit;
namespace py = pybind11;

void init_SmoothHistogramPdf(py::module &m) {
    py::class_<SmoothHistogramPdf, GooPdf>(m, "SmoothHistogramPdf")
        .def(py::init<std::string, BinnedDataSet *, Variable>(), py::keep_alive<1, 3>(), py::keep_alive<1, 4>());
}
