# coding=utf-8
# from distutils.core import setup, Extension
from setuptools import find_packages, setup, Extension
from glob import glob
from distutils.command.build_ext import build_ext
from distutils.command.build_clib import build_clib
import distutils.sysconfig
import platform
import os
import sys
import shutil
import subprocess
import tempfile
import sysconfig
# from Cython.Build import cythonize
from _version import __version__

_DEBUG = False
_DEBUG_LEVEL = 0

# --------------------- Initialization ------------------------------

extensions = []
extra_compile_args = []
extra_link_args = ["-lm"]
numpy_headers = []


if _DEBUG:
    extra_compile_args += ["-g", "-O0", "-D_DEBUG=%s" % _DEBUG_LEVEL, "-UNDEBUG"]
else:
    extra_compile_args += ["-DNDEBUG", "-O3"]

# print(sysconfig.get_config_var('CFLAGS').split())
# --------------------- Get OpenMP compiler flag --------------------

# If this C test program compiles the compiler supports OpenMP
# http://stackoverflow.com/questions/16549893/programatically-testing-for-openmp-support-from-a-python-setup-script
omp_test = \
    r"""
    #include <omp.h>
    #include <stdio.h>
    int main()
    {
        #pragma omp parallel
        printf("Hello from thread %d, nthreads %d\n", omp_get_thread_num(), omp_get_num_threads());
        return 0;
    }
    """


def get_compiler_openmp_flag():
    openmp_flag = ''
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)
    filename = r'omp_test.c'

    with open(filename, 'w') as file:
        file.write(omp_test)
        file.flush()

    try:
        cc = os.environ['CC']
    except KeyError:
        cc = 'cc'

    # Compile omp_test.c program using different OpenMP compiler flags.
    # If the code below fails continue without OpenMP support.
    with open(os.devnull, 'w') as fnull:
        exit_code = 1
        try:
            exit_code = subprocess.call([cc, '-fopenmp', filename], stdout=fnull, stderr=fnull)
        except:
            pass
        if exit_code == 0:
            openmp_flag = '-fopenmp'
        else:
            try:
                exit_code = subprocess.call([cc, '-openmp', filename], stdout=fnull, stderr=fnull)
            except:
                pass
            if exit_code == 0:
                openmp_flag = '-openmp'

    # clean up
    os.chdir(curdir)
    shutil.rmtree(tmpdir)
    return openmp_flag


def getGlibFlag():
    try:
        glib_cflag = subprocess.check_output("pkg-config --cflags glib-2.0", shell=True).decode().strip()
        extra_compile_args.extend(glib_cflag.split())
    except Exception as e:
        print(e)


def getGlibLibrary():
    try:
        glib_lib = subprocess.check_output("pkg-config --libs glib-2.0 --libs gthread-2.0", shell=True).decode().strip()
        extra_link_args.extend(glib_lib.split())
    except Exception as e:
        print(e)


def setPlatformRelatedConfig():
    if sys.platform == 'darwin':
        from distutils import sysconfig
        vars = sysconfig.get_config_vars()
        vars['LDSHARED'] = vars['LDSHARED'].replace('-bundle', '-dynamiclib')
        extra_link_args.append('-dynamiclib')
        # extra_compile_args.append('-dynamiclib')
        os.environ["CC"] = "clang"
        os.environ["CXX"] = "clang"


def getNumpyHeader():
    try:
        import numpy
        numpy_headers.append(numpy.get_include())
    except Exception as e:
        print(e)




getGlibFlag()
getGlibLibrary()
getNumpyHeader()
setPlatformRelatedConfig()
# openmp_flag = get_compiler_openmp_flag()
# print('get_compiler_openmp_flag(): ' + openmp_flag)

# extra_compile_args.append(openmp_flag)
# extra_link_args.append(openmp_flag)


print('all compile flags: ' + str(extra_compile_args))
print('all link flasgs: ' + str(extra_link_args))

# --------------------- parda module ---------------------------
# extensions.append(Extension(
#     "mimircache.profiler.libparda",
#     glob("mimircache/profiler/parda/src/*.c"),
#     include_dirs=["mimircache/profiler/parda/src/h/"],
#     extra_compile_args=extra_compile_args,
#     extra_link_args=extra_link_args,
#     language="c"
# ))

# # --------------------- vscsi module ---------------------------
# extensions.append(Extension(
#     "mimircache.cacheReader.libvscsi",
#     glob("mimircache/cacheReader/vscsi/src/*.c"),
#     include_dirs=["mimircache/cacheReader/vscsi/src/"],
#     language="c"
# ))

extensions.append(Extension(
    'mimircache.c_cacheReader',
    glob("mimircache/CExtension/cacheReader/*.c") + 
    ["mimircache/CExtension/pyBindings/pyReader.c"], 
    include_dirs=["mimircache/CExtension/headers"] + 
    ["mimircache/CExtension/cacheReader/include"] + numpy_headers,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c"))

extensions.append(Extension(
    'mimircache.c_LRUProfiler',
    ["mimircache/CExtension/profiler/LRUProfiler.c", "mimircache/CExtension/profiler/splay.c"] +
    glob('mimircache/CExtension/cacheReader/*.c') +
    glob('mimircache/CExtension/utils/*.c') + 
    ["mimircache/CExtension/pyBindings/pyLRUProfiler.c"], 
    include_dirs=["mimircache/CExtension/headers"] + 
    ["mimircache/CExtension/cache/include"] + 
    ["mimircache/CExtension/cacheReader/include"] + 
    ["mimircache/CExtension/profiler/include"] + 
    ["mimircache/CExtension/utils/include/"] + 
    ["mimircache/CExtension/pyBindings/headers"] + 
    ['mimircache/CExtension/headers/cache'] + numpy_headers, 
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c"))

extensions.append(Extension(
    'mimircache.c_generalProfiler',
    glob("mimircache/CExtension/profiler/*.c") +
    glob("mimircache/CExtension/cache/*.c") +
    glob('mimircache/CExtension/cacheReader/*.c') +
    glob('mimircache/CExtension/utils/*.c') +
    glob('mimircache/CExtension/wrapper/*.c') + 
    ["mimircache/CExtension/pyBindings/pyGeneralProfiler.c"] + 
    ["mimircache/CExtension/pyBindings/python_wrapper.c"], 
    include_dirs=["mimircache/CExtension/headers"] + 
    ["mimircache/CExtension/cache/include"] + 
    ["mimircache/CExtension/cacheReader/include"] + 
    ["mimircache/CExtension/profiler/include"] + 
    ["mimircache/CExtension/utils/include/"] + 
    ["mimircache/CExtension/pyBindings/headers"] + 
    ['mimircache/CExtension/headers/cache'] + numpy_headers, 
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c"))

extensions.append(Extension(
    'mimircache.c_heatmap',
    glob("mimircache/CExtension/profiler/*.c") +
    glob("mimircache/CExtension/cache/*.c") +
    glob('mimircache/CExtension/cacheReader/*.c') +
    glob('mimircache/CExtension/utils/*.c') +
    glob('mimircache/CExtension/wrapper/*.c') + 
    ["mimircache/CExtension/pyBindings/python_wrapper.c"] +  
    ["mimircache/CExtension/pyBindings/pyHeatmap.c"], 
    include_dirs=["mimircache/CExtension/headers"] + 
    ["mimircache/CExtension/cache/include"] + 
    ["mimircache/CExtension/cacheReader/include"] + 
    ["mimircache/CExtension/profiler/include"] + 
    ["mimircache/CExtension/utils/include/"] + 
    ["mimircache/CExtension/pyBindings/headers"] + 
    ['mimircache/CExtension/headers/cache'] + numpy_headers, 
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c"))

extensions.append(Extension(
    'mimircache.c_eviction_stat',
    glob("mimircache/CExtension/profiler/*.c") +
    glob("mimircache/CExtension/cache/*.c") +
    glob('mimircache/CExtension/cacheReader/*.c') +
    glob('mimircache/CExtension/utils/*.c') +
    glob('mimircache/CExtension/wrapper/*.c') + 
    ["mimircache/CExtension/pyBindings/python_wrapper.c"] +  
    ["mimircache/CExtension/pyBindings/pyEviction_stat.c"], 
    include_dirs=["mimircache/CExtension/headers"] + 
    ["mimircache/CExtension/cache/include"] + 
    ["mimircache/CExtension/cacheReader/include"] + 
    ["mimircache/CExtension/profiler/include"] + 
    ["mimircache/CExtension/utils/include/"] + 
    ["mimircache/CExtension/pyBindings/headers"] + 
    ['mimircache/CExtension/headers/cache'] + numpy_headers, 
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    language="c"))





# extensions.append(cythonize("mimircache/cache/RR.pyx"))



# print("find packages: " + str(
#     find_packages(exclude=(['mimircache.bin', 'mimircache.test', 'mimircache.data', 'mimircache.A1a1a11a']))))

print("Extension: " + str(extensions))
# long_description = read('README.md', 'CHANGES')


setup(
    name="mimircache",
    version=__version__,
    # package_dir = {'':'src'},
    packages = ['mimircache', 'mimircache.cache', 'mimircache.cacheReader', 'mimircache.profiler', 'mimircache.profiler.abstract', 'mimircache.utils', 'mimircache.top'],
    # packages=find_packages(exclude=(['mimircache.bin', 'mimircache.test', 'mimircache.data', 'mimircache.A1a1a11a'])),
    # modules = 
    # package_data={'plain': ['mimircache/data/trace.txt'],
    #               'csv': ['mimircache/data/trace.csv'],
    #               'vscsi': ['mimircache/data/trace.vscsi'],
    #               'conf': ['mimircache/conf']},
    # include_package_data=True,
    author="Juncheng Yang",
    author_email="peter.waynechina@gmail.com",
    description="mimircache platform for analyzing cache traces, developed by Juncheng Yang in Ymir group @ Emory University",
    license="GPLv3",
    keywords="mimircache cache Ymir",
    url="http://mimircache.info",

    # libraries = [libparda, libvscsi],
    # cmdclass = {'build_clib' : build_clib},
    # cmdclass = {'build_ext': build_ext_subclass, 'build_clib' : build_clib_subclass},

    ext_modules=extensions,
    classifiers=[
        'Development Status :: 3 - Alpha',

        # 'Topic :: Operating System :: cache analysis'

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['heapdict', 'mmh3']      # 'numpy', 'matplotlib', 'scipy',
    # long_description=long_description
)



# python3 setup.py sdist upload -r pypitest

# could also try this: 
# from distutils.ccompiler import new_compiler

# # Create compiler with default options
# c = new_compiler()
# workdir = "."

# # Optionally add include directories etc.
# # c.add_include_dir("some/include")

# # Compile into .o files
# objects = c.compile(["a.c", "b.c"])

# # Create static or shared library
# c.create_static_lib(objects, "foo", output_dir=workdir)
# c.link_shared_lib(objects, "foo", output_dir=workdir)
