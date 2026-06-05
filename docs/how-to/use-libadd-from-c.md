# How to use `libadd` from C/C++

The C core is a first-class artifact. You can link it without touching Python.

## Build and install

```bash
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build build
cmake --install build      # installs lib, headers, CMake config, pkg-config
```

## From a CMake project

```cmake
find_package(addlib CONFIG REQUIRED)
target_link_libraries(myapp PRIVATE addlib::add)
```

## From a plain Makefile (pkg-config)

```bash
cc myapp.c $(pkg-config --cflags --libs libadd) -o myapp
```

## Minimal program

```c
#include <add/add.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
    int64_t out;
    switch (add_i64(20, 22, &out)) {
        case ADD_OK:           printf("%lld\n", (long long)out); break;
        case ADD_ERR_OVERFLOW: fprintf(stderr, "overflow\n");    return 1;
        case ADD_ERR_NULL:     fprintf(stderr, "null out\n");    return 1;
    }
    return 0;
}
```

A runnable copy is in [`examples/use_libadd.c`](https://github.com/rosualinpetru/addlib/blob/main/examples/use_libadd.c).

## ABI stability

`libadd`'s ABI is versioned by its `SOVERSION` (currently `0`), separate from the
release version. Breaking it (changing a signature, renumbering `add_status_t`)
is a MAJOR-level event for C consumers — see
[versioning](../explanation/versioning.md).
