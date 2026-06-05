/* SPDX-License-Identifier: Apache-2.0 */
/* Copyright 2026 Alin-Petru Roșu */
/* Minimal dependency-free C test harness, run under CTest (and ASan/UBSan in CI). */

#include "add/add.h"

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int failures = 0;

#define CHECK(cond)                                                                    \
    do {                                                                               \
        if (!(cond)) {                                                                 \
            fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond);            \
            failures++;                                                                \
        }                                                                              \
    } while (0)

static void test_basic(void) {
    int64_t out = 0;
    CHECK(add_i64(2, 3, &out) == ADD_OK);
    CHECK(out == 5);
    CHECK(add_i64(-1, 1, &out) == ADD_OK);
    CHECK(out == 0);
    CHECK(add_i64(-7, -8, &out) == ADD_OK);
    CHECK(out == -15);
}

static void test_null_out(void) {
    CHECK(add_i64(1, 2, NULL) == ADD_ERR_NULL);
}

static void test_overflow(void) {
    int64_t out = 123; /* sentinel: must be left unchanged on overflow */
    CHECK(add_i64(INT64_MAX, 1, &out) == ADD_ERR_OVERFLOW);
    CHECK(out == 123);
    CHECK(add_i64(INT64_MIN, -1, &out) == ADD_ERR_OVERFLOW);
    CHECK(add_i64(INT64_MAX, INT64_MAX, &out) == ADD_ERR_OVERFLOW);
    CHECK(add_i64(INT64_MIN, INT64_MIN, &out) == ADD_ERR_OVERFLOW);
}

static void test_boundary_no_overflow(void) {
    int64_t out = 0;
    CHECK(add_i64(INT64_MAX, 0, &out) == ADD_OK && out == INT64_MAX);
    CHECK(add_i64(INT64_MIN, 0, &out) == ADD_OK && out == INT64_MIN);
    CHECK(add_i64(INT64_MAX - 1, 1, &out) == ADD_OK && out == INT64_MAX);
}

static void test_floats(void) {
    CHECK(add_f64(0.5, 0.25) == 0.75);
    CHECK(add_f64(-1.0, 1.0) == 0.0);
}

static void test_version(void) {
    CHECK(strcmp(add_version(), ADDLIB_VERSION_STRING) == 0);
}

int main(void) {
    test_basic();
    test_null_out();
    test_overflow();
    test_boundary_no_overflow();
    test_floats();
    test_version();

    if (failures != 0) {
        fprintf(stderr, "%d check(s) failed\n", failures);
        return 1;
    }
    printf("all C tests passed\n");
    return 0;
}
