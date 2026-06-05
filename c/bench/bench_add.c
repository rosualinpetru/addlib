/* SPDX-License-Identifier: Apache-2.0 */
/* Copyright 2026 Alin-Petru Rosu */
/* A tiny wall-clock microbenchmark for the C core. CI tracks trends from the
 * Python benchmarks (pytest-benchmark); this one is for local C-level profiling. */

#include "add/add.h"

#include <stdint.h>
#include <stdio.h>
#include <time.h>

int main(void) {
    const long iters = 200000000L;
    int64_t out = 0;
    volatile int64_t sink = 0;

    struct timespec t0;
    struct timespec t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (long i = 0; i < iters; i++) {
        (void)add_i64((int64_t)i, 1, &out);
        sink += out;
    }
    clock_gettime(CLOCK_MONOTONIC, &t1);

    double total_ns =
        (double)(t1.tv_sec - t0.tv_sec) * 1e9 + (double)(t1.tv_nsec - t0.tv_nsec);
    printf("add_i64: %.3f ns/op over %ld iters (sink=%lld)\n", total_ns / (double)iters,
           iters, (long long)sink);
    return 0;
}
