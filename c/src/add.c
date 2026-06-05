/* SPDX-License-Identifier: Apache-2.0 */
/* Copyright 2026 Alin-Petru Roșu */

#include "add/add.h"

#include <stddef.h>

add_status_t add_i64(int64_t a, int64_t b, int64_t *out) {
    if (out == NULL) {
        return ADD_ERR_NULL;
    }

#if defined(__GNUC__) || defined(__clang__)
    /* Compiler builtin: detects signed overflow without ever invoking UB.
     * Write through a temporary so that *out is left unmodified on overflow,
     * as the header contract promises (the builtin would otherwise store the
     * wrapped value into *out even when it reports overflow). */
    int64_t tmp;
    if (__builtin_add_overflow(a, b, &tmp)) {
        return ADD_ERR_OVERFLOW;
    }
    *out = tmp;
    return ADD_OK;
#else
    /* Portable fallback: check before adding so we never trigger signed
     * overflow (which is undefined behavior in C). */
    if ((b > 0 && a > INT64_MAX - b) || (b < 0 && a < INT64_MIN - b)) {
        return ADD_ERR_OVERFLOW;
    }
    *out = a + b;
    return ADD_OK;
#endif
}

double add_f64(double a, double b) {
    return a + b;
}

const char *add_version(void) {
    return ADDLIB_VERSION_STRING;
}
