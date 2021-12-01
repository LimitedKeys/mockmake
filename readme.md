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

## Using Mock Make

Creat a Makefile and define a few variables:

``` make
MOCK_INCLUDE = ./src ../libs
MOCK_SOURCE = ./src ../libs/driver ../libs/test
MOCK_OUTPUT = ./output/mock
MOCK_PATCH = main.c
MOCK_EXE = test.mock.out

.PHONY: all

all: mock_build mock_run
```

Variables to control Mock Make:

| Variable     | Description                   |
| --------     | ----------		       |
| MOCK_INCLUDE | Dirs to include (-I)          |
| MOCK_SOURCE  | Dirs to walk for souce files  |
| MOCK_OUTPUT  | Output directory path         |
| MOCK_PATCH   | TBD: Files to be patched      |
| MOCK_EXE     | Output EXE name               |

Provided Recipes:

| Recipe       | Description                   |
| ------       | ----------		       |
| mock_run     | Run the built executable      |
| mock_build   | Build the executable          |
| mock_clean   | Remove the mock output dir    |

## Limitations

-  folders / files cannot contain white space (bad things will happen)
-  built source files must have unique names.
   Two reasons:
   1. All objects are put into the same output
      directory. 
   2. The patch file will find the source files
      to patch based on the file name

## Example


