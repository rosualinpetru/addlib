/* SPDX-License-Identifier: Apache-2.0 */
/* A standalone C consumer of libadd. Build after installing the library:
 *
 *   cc examples/use_libadd.c $(pkg-config --cflags --libs libadd) -o use_libadd
 *   ./use_libadd
 *
 * or, from a CMake project:  target_link_libraries(app PRIVATE addlib::add)
 */
#include <add/add.h>

#include <stdint.h>
#include <stdio.h>

int main(void) {
    int64_t out;
    switch (add_i64(20, 22, &out)) {
        case ADD_OK:
            printf("20 + 22 = %lld\n", (long long)out);
            break;
        case ADD_ERR_OVERFLOW:
            fprintf(stderr, "overflow\n");
            return 1;
        case ADD_ERR_NULL:
            fprintf(stderr, "null output pointer\n");
            return 1;
    }

    printf("0.5 + 0.25 = %g\n", add_f64(0.5, 0.25));
    printf("libadd version: %s\n", add_version());
    return 0;
}
