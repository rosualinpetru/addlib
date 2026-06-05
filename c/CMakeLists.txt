# SPDX-License-Identifier: Apache-2.0
# libadd — the C performance core.
include(GNUInstallDirs)

add_library(add src/add.c)
add_library(addlib::add ALIAS add)

target_include_directories(add
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

set_target_properties(add PROPERTIES
    C_STANDARD 11
    C_STANDARD_REQUIRED ON
    C_EXTENSIONS OFF
    OUTPUT_NAME add
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}      # ABI version, distinct from release version
    PUBLIC_HEADER "${CMAKE_CURRENT_SOURCE_DIR}/include/add/add.h")

if(MSVC)
    target_compile_options(add PRIVATE /W4)
else()
    target_compile_options(add PRIVATE -Wall -Wextra -Wpedantic)
endif()

# --- Install + CMake package export ------------------------------------------
install(TARGETS add
    EXPORT addlibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/add)

install(EXPORT addlibTargets
    FILE addlibTargets.cmake
    NAMESPACE addlib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/addlib)

include(CMakePackageConfigHelpers)
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/addlibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/addlibConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/addlib)
write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/addlibConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/addlibConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/addlibConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/addlib)

# pkg-config, for plain Makefile / autotools consumers.
configure_file(libadd.pc.in ${CMAKE_CURRENT_BINARY_DIR}/libadd.pc @ONLY)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/libadd.pc
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/pkgconfig)

# --- Tests / fuzzers / benchmarks (opt-in) -----------------------------------
if(ADDLIB_BUILD_TESTS)
    add_executable(test_add tests/test_add.c)
    target_link_libraries(test_add PRIVATE addlib::add)
    add_test(NAME test_add COMMAND test_add)
endif()

# Requires a clang with the libFuzzer runtime. On macOS, Apple clang lacks it —
# configure with Homebrew LLVM, e.g.
#   cmake -S . -B build -DADDLIB_BUILD_FUZZERS=ON \
#         -DCMAKE_C_COMPILER="$(brew --prefix llvm)/bin/clang"
if(ADDLIB_BUILD_FUZZERS)
    add_executable(fuzz_add fuzz/fuzz_add.c)
    target_link_libraries(fuzz_add PRIVATE addlib::add)
    target_compile_options(fuzz_add PRIVATE -g -O1 -fsanitize=fuzzer,address,undefined)
    target_link_options(fuzz_add PRIVATE -fsanitize=fuzzer,address,undefined)
endif()

if(ADDLIB_BUILD_BENCH)
    add_executable(bench_add bench/bench_add.c)
    target_link_libraries(bench_add PRIVATE addlib::add)
endif()
