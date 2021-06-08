from setuptools import setup, find_packages, Extension

setup(
    name='mykmeanssp',
    version='1.0',
    author="Michael Grabois and Amit Levy",
    description="A kmeans C-API",
    install_requires=['invoke', 'pandas', 'argparse', 'numpy', 'random', 'matplotlib', 'math', 'sys', 'sklearn'],
    python_requires='>=3.8, <4',
    packages=find_packages(),  # find_packages(where='.', exclude=())
                               #    Return a list of all Python packages found within directory 'where'
    license='GPL-2',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        # We need to tell the world this is a CPython extension
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    ext_modules=[
        Extension(
            # the qualified name of the extension module to build
            'mykmeanssp',
            # the files to compile into our module relative to ``setup.py``
            ['./kmeans.c'],
        ),
    ]
)