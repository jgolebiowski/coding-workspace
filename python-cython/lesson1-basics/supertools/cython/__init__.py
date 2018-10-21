import os
import numpy as np
import pyximport


def compile(workdir: str = None) -> None:
    """
    Specify all compilation parameters and compile cython packages.
    This function imports all cython modules and compiles them in the process

    :param workdir: location of the build directory
    """
    if workdir is None:
        workdir = os.path.dirname(os.path.realpath(__file__))

    pyimporter, pyximporter = pyximport.install(
        setup_args=dict(
            libraries=[],
            include_dirs=[np.get_include()]
        ),
        pyimport=True,
        build_dir=os.path.join(workdir, "build"),
        inplace=True,
        language_level=3
    )

    import supertools.cython.utilities


compile()