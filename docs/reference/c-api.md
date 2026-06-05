# C API reference

The stable C ABI. The single source of truth is
[`c/include/add/add.h`](https://github.com/rosualinpetru/addlib/blob/main/c/include/add/add.h);
this page summarizes it. (A real project would bridge in Doxygen output here.)

## Status codes

```c
typedef enum add_status {
    ADD_OK           = 0,  // success; output written
    ADD_ERR_NULL     = 1,  // a required output pointer was NULL
    ADD_ERR_OVERFLOW = 2   // the true result is out of range
} add_status_t;
```

Values are part of the ABI — never renumbered, only appended.

## Functions

### `add_i64`

```c
add_status_t add_i64(int64_t a, int64_t b, int64_t *out);
```

Adds `a + b` with overflow checking. On success writes the sum to `*out` and
returns `ADD_OK`. On overflow returns `ADD_ERR_OVERFLOW` and **leaves `*out`
unmodified**. Returns `ADD_ERR_NULL` if `out` is `NULL`. Never invokes undefined
behavior on any input.

### `add_f64`

```c
double add_f64(double a, double b);
```

Returns the IEEE-754 double-precision sum. Infinities and NaN propagate; no
exception is raised.

### `add_version`

```c
const char *add_version(void);
```

Returns the version string (e.g. `"0.2.0"`) with static storage duration; do not
free it.

## Versioning macros

```c
#define ADDLIB_VERSION_MAJOR  0
#define ADDLIB_VERSION_MINOR  2
#define ADDLIB_VERSION_PATCH  0
#define ADDLIB_VERSION_STRING "0.2.0"
```
