""" Task definitions for invoke command line utility for python bindings
    overview article. """
#import cffi
import invoke
#import pathlib


@invoke.task
def clean(c):
    """ Remove any built objects """
    for pattern in ["*.o", "*.so"]:
        c.run("rm -rf {}".format(pattern))


def print_banner(msg):
    print("==================================================")
    print("= {} ".format(msg))

@invoke.task
def build_radix(c):
    """ Build the shared library for the sample C code """
    cfile_name = "radix"
    print_banner("Building C Library")
    invoke.run("gcc -c -Wall -Werror -fpic " + cfile_name + ".c -I /usr/include/python3.8")
    invoke.run("gcc -shared -o lib" + cfile_name + ".so " + cfile_name + ".o")
    print("* Complete")

@invoke.task
def build_lcs(c):
    """ Build the shared library for the sample C code """
    cfile_name = "lcs"
    print_banner("Building C Library")
    invoke.run("gcc -c -Wall -Werror -fpic " + cfile_name + ".c -I /usr/include/python3.8")
    invoke.run("gcc -shared -o lib" + cfile_name + ".so " + cfile_name + ".o")
    print("* Complete")

