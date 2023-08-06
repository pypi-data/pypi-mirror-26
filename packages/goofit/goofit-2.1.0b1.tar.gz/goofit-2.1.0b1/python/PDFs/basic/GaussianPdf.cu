#include <pybind11/pybind11.h>

#include <goofit/PDFs/basic/GaussianPdf.h>
#include <goofit/Variable.h>

using namespace GooFit;
namespace py = pybind11;

void init_GaussianPdf(py::module &m) {
    py::class_<GaussianPdf, GooPdf>(m, "GaussianPdf")
        .def(py::init<std::string, Observable, Variable, Variable>(),
             py::keep_alive<1, 3>(),
             py::keep_alive<1, 4>(),
             py::keep_alive<1, 5>());
}
