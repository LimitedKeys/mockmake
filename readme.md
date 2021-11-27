# Mock Make

Quickly build a C application using make.
Intended to be used to test an application with
out all the source files.

## How do I do it

1. Process main function to
    - rename main
    - remove infinite loops
    - ...
2. Compile source files
3. Compile mock source files
4. Compile test source
5. Link
6. Execute tests
7. Lint

``` bash
> make
```

## TODO

- finding source files
- basic implementation
- notes on calling from another make
