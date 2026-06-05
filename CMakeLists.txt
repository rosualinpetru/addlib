# SPDX-License-Identifier: Apache-2.0
# Top-level build for the standalone libadd C library.
#
# The Python package does NOT use this file — it compiles the C core via CFFI
# (see python/src/addlib/_build_ffi.py). This CMake build exists so that C/C++
# consumers can use libadd as a first-class, independently reusable artifact,
# exactly as the roadmap's "separate the C ABI layer explicitly" refinement
# recommends.
#
#   cmake -S . -B build -DADDLIB_BUILD_TESTS=ON
#   cmake --build build
#   ctest --test-dir build --output-on-failure
cmake_minimum_required(VERSION 3.15)

project(addlib
    VERSION 0.1.0
    DESCRIPTION "Tiny checked-addition C core for addlib"
    HOMEPAGE_URL "https://github.com/rosualinpetru/addlib"
    LANGUAGES C)

option(ADDLIB_BUILD_TESTS "Build libadd C tests" OFF)
option(ADDLIB_BUILD_FUZZERS "Build libadd fuzz targets (requires clang)" OFF)
option(ADDLIB_BUILD_BENCH "Build libadd benchmarks" OFF)

if(ADDLIB_BUILD_TESTS)
    enable_testing()
endif()

add_subdirectory(c)
