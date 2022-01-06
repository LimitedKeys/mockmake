# Mock Make Examples

Simple toy examples on how to use the 'mock.mk'
file. Each example is built using make from the
example directory.

Examples:

- [Hello World](#hello-world)
- [Source Tree](#source-tree)
- [Includes](#includes)
- [Simple Patch](#simple-patch)

## Hello World

Build the Hello World C file, which prints
"hello, world" to the console.

## Source Tree

Build an application using multiple source
files, in which all of the source files can be
found from a single directory. The application
should print "abc" to the console.

## Includes

Build an application using multiple source
files, in which each source file has a separate
include path. The application should print
"abc" to the console.

## Simple Patch

Build [Source Tree](#source-tree) but patch the
main file. The "patch" copies the main file
without modifying it.

## Firmware

Build an application, in which all the source
files are kept in a directory separate from the
main file. The main file is modified to remove
the forever loop, so that the code can be
executed.
