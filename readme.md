# Mock Make

Quickly build a C application to test using
make.

## Isn't that just called make?

Kinda. Let's say we're building firmware for a
microcontroller, and we want to test it on our
PC. Make is a great tool for this bit, and Mock
Make can help:

- Find source files
- Build object files
- Link and stuff

By listing the source directories in the
`MOCK_SRC` variable, all the C files will be
automatically found and staged for building.

Normally, the firmware being tested will have
an involved 'main' function as well, with a
`while(1)` loop at the end, which makes the
firmware difficult to test. Mock Make offers
the ability to 'patch' some source files using
a patch script, so the blocking code can be
altered.

Useful? Possibly. Limited? Definitely.

## Limitations

-  folders / files cannot contain white space
   (bad things will happen, make limitation)

## Details

Variables to control Mock Make:

| Variable     | Description                   |
| --------     | ----------		       |
| MOCK_INCLUDE | Dirs to include (-I)          |
| MOCK_SOURCE  | Dirs to walk for souce files  |
| MOCK_OUTPUT  | Output directory path         |
| MOCK_EXE     | Output EXE name               |
| MOCK_PATCH   | Files to be patched           |
| MOCK_PSCRIPT | Path to the patch script      |

Provided Recipes:

| Recipe       | Description                   |
| ------       | ----------		               |
| mock_all     | Build and Run                 |
| mock_run     | Run the built executable      |
| mock_build   | Build the executable          |
| mock_clean   | Remove the mock output dir    |

### Building

Directories provided to `MOCK_SOURCE` will be
search recursively for C / S files. This
process is done in Python by the
`scripts/source_mk.py` script.

One the source files are found, the script will
write a `source.mk` make file to the
`MOCK_OUTPUT` directory. This contains recipes
to build each source file into an object file. 

The `mock.mk` file imports (includes) the
generated makefile and links the build objects
together into `MOCK_EXE`.

#### Why source.mk?

Finding source files automatically in make is
annoying. Python gives a little more control
over this.

### Patching?

Source files provided to the `MOCK_PATCH`
variable will be passed to the provided
`MOCK_PSCRIPT` before compiling.

Normally, a '.c' will be compiled into a '.o'
file using some C compiler.

    .c -> cc -> .o

Patched files will run through a patch script
first:

    .c -> patch -> .patch.c -> cc -> .o

By providing an extra recipe for these files in
source.mk, the patch will only be regenerated
when the source file changes. 

The patch script should be in Python, and
should accept two arguments:

1.  Path to the source file to modify
2.  Path to save the patched file to

How the patch file operates on the source file
is up to the calling project basically. 

## Example

Project Layout:

```
+libs/
|--mockmake/
|--driver/
+project/
|--src/...
|--Makefile
|--readme
```

Project Makefile:

``` make
MOCK_SOURCE := ./src ../libs/driver
MOCK_INCLUDE := ./src ../libs/driver
MOCK_OUTPUT := ./output/mock
MOCK_EXE := project.mock.exe

.PHONY: all

all: mock_all

include ../libs/mockmake/mock.mk
```

## Example: Patch Main Source

Project Layout:

```
+libs/
|--mockmake/
|--driver/
|--test/
+project/
|--src/main.c
|--Makefile
|--readme
|--patch.py
```

Project Makefile:

``` make
MOCK_SOURCE := ./src ../libs/driver ../libs/test
MOCK_INCLUDE := ./src ../libs/driver ../libs/test

MOCK_OUTPUT := ./output/mock
MOCK_EXE := project.mock.exe

MOCK_PATCH := ./src/main.c
MOCK_PSCRIPT := ./patch.py

.PHONY: all clean

all: mock_all
clean: mock_clean

include ../libs/mockmake/mock.mk
```
