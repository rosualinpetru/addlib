/* SPDX-License-Identifier: Apache-2.0 */
/* Copyright 2026 Alin-Petru Rosu */

/**
 * @file add.h
 * @brief Public C ABI for libadd — the stable contract the Python layer binds to.
 *
 * This header is the *only* surface the Python (CFFI) bindings depend on. Treat
 * it as a first-class deliverable: changing a signature or a struct layout here
 * is an ABI break (a MAJOR-level event for C consumers), independent of the
 * Python API. See docs/explanation/design.md (the "C-ABI contract" section).
 *
 * Stability tier: STABLE. The functions below follow the project's SemVer and
 * ABI-stability promises once the library reaches 1.0.
 */

#ifndef ADDLIB_ADD_H
#define ADDLIB_ADD_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/** Library version, available at compile time for consumers. */
#define ADDLIB_VERSION_MAJOR 0
#define ADDLIB_VERSION_MINOR 2
#define ADDLIB_VERSION_PATCH 0
#define ADDLIB_VERSION_STRING "0.2.0"

/**
 * @brief Status codes returned by checked operations.
 *
 * Values are part of the ABI; never renumber an existing code. Append new
 * codes at the end.
 */
typedef enum add_status {
    ADD_OK = 0,          /**< Success; output written. */
    ADD_ERR_NULL = 1,    /**< A required output pointer was NULL. */
    ADD_ERR_OVERFLOW = 2 /**< The true mathematical result is out of range. */
} add_status_t;

/**
 * @brief Add two signed 64-bit integers with overflow checking.
 *
 * Computes @p a + @p b. On success, writes the sum to @p *out and returns
 * ::ADD_OK. If the true mathematical sum lies outside the range of int64_t,
 * @p *out is left unmodified and ::ADD_ERR_OVERFLOW is returned. If @p out is
 * NULL, returns ::ADD_ERR_NULL.
 *
 * This function does not branch on the *values* in a secret-dependent way that
 * matters here (there are no secrets), but it is written to be total: it never
 * exhibits undefined behavior on any input, which is the property fuzzing
 * verifies.
 *
 * @param a   First addend.
 * @param b   Second addend.
 * @param out Destination for the sum (must be non-NULL).
 * @return ::ADD_OK, ::ADD_ERR_OVERFLOW, or ::ADD_ERR_NULL.
 */
add_status_t add_i64(int64_t a, int64_t b, int64_t *out);

/**
 * @brief Add two IEEE-754 double-precision floats.
 *
 * Returns @p a + @p b with the platform's default rounding. Follows IEEE-754
 * semantics for infinities and NaN (no exception is raised). The result is
 * approximate: callers must reason about floating-point error, not exact
 * equality.
 *
 * @param a First addend.
 * @param b Second addend.
 * @return The sum @p a + @p b.
 */
double add_f64(double a, double b);

/**
 * @brief Return the library version as a static, NUL-terminated string.
 *
 * The returned pointer has static storage duration; the caller must not free
 * it. Equal to ::ADDLIB_VERSION_STRING for a matching build.
 *
 * @return Version string, e.g. "0.2.0".
 */
const char *add_version(void);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* ADDLIB_ADD_H */
