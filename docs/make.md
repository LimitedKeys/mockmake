# Notes on Make

Some information that I have found helpful while
developing mock.mk:

- [GNU Make Manual](https://www.gnu.org/software/make/manual/html_node/index.html)
- [Recursive Wildcard](https://stackoverflow.com/questions/2483182/recursive-wildcards-in-gnu-make)
- [Makefile Tutorial](https://makefiletutorial.com/#the-vpath-directive)

hopefully helpful notes for myself for later

## Make and finding objects

Make works a bit backwards. I normally think:

1. Source files
2. Object files
3. Executable

Make works from the executable towards the
source files:

1. What is needed to make the executable?
2. What is needed to make the objects?
3. Where are the source files?

Other things to keep in mind:

- paths can not contain spaces
- paths should use '/' (Windows ...)

## Pattern Match Recipes

Let's say we have a bunch of source files kept 
in a 'src' directory, and we want to build the 
'obj' files in a directory tree that matches
the source:

``` make
SRC:=./src/main.c ...
OBJ:=$(addprefix ./output/,$(SRC:.c=.o))

output/target.out: $(OBJ)
    $(CC) $^ -o $@

output/%.o: %.c
    mkdir -p $(@D)
    $(CC) -c $< -o $@
```

Make finds the source files needed by matching 
the object path represented by the '%' with a 
source file relative to the current directory.
In this example:

- source files are listed with the path from the
  current dir
- source files should be located below the 
  Makefile (../ files would be bad)

## vpath

The vpath is the directories that source files 
will be searched in to match an object file. By
default, it's just '.'.

It is noted in a bunch of places that this 
should NOT be used to locate object files, 
just source files.

The previous Makefile can be written as follows,
with a slight changes in behavior: output
objects are built in the output dir in a "flat”
way:

``` make
SRC:=./src/main.c ...
OBJ:=$(addprefix ./output/, \
                 $(notdir $(SRC:.c=.o)))

vpath %.c $(dir $(SRC))

output/target.out: $(OBJ)
    $(CC) $^ -o $@

output/%.o: %.c
    mkdir -p $(@D)
    $(CC) -c $< -o $@
```

This adds a limitation to Make: source file 
names must be unique.
