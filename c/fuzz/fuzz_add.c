/* SPDX-License-Identifier: Apache-2.0 */
/* Copyright 2026 Alin-Petru Roșu */
/*
 * libFuzzer target for add_i64. Build with:
 *   cmake -S . -B build -DADDLIB_BUILD_FUZZERS=ON -DCMAKE_C_COMPILER=clang
 *   cmake --build build --target fuzz_add
 *   ./build/fuzz_add -max_total_time=60
 *
 * This is the attacker-reachable-input analogue from the roadmap (Phase 3.2):
 * deserialization is where crypto CVEs live, so we fuzz the function that turns
 * raw bytes into a result, with a differential oracle (128-bit arithmetic that
 * cannot itself overflow) checking that the status and output are always
 * consistent with the true mathematical sum.
 */

#include "add/add.h"

#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 16) {
        return 0;
    }

    int64_t a;
    int64_t b;
    memcpy(&a, data, sizeof(a));
    memcpy(&b, data + 8, sizeof(b));

    int64_t out = 0;
    add_status_t status = add_i64(a, b, &out);

    /* Oracle: __int128 addition of two int64 values never overflows. */
    __int128 wide = (__int128)a + (__int128)b;

    if (status == ADD_OK) {
        assert((__int128)out == wide);
    } else if (status == ADD_ERR_OVERFLOW) {
        assert(wide > (__int128)INT64_MAX || wide < (__int128)INT64_MIN);
    } else {
        /* out is non-NULL, so ADD_ERR_NULL must never occur. */
        assert(0 && "unexpected status from add_i64");
    }
    return 0;
}
