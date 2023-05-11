from setuptools import setup, find_packages

setup(
    version="0.0.1",
    name="distrax",
    description="a fast and scalable deployment tool to create quick and efficient \
                 storage systems onto high-performance computing (HPC) \
                 compute nodes utilising the compute nodes system memory/storage.",
    url="https://github.com/rosalindfranklininstitute/distrax",
    author="Gabryel Mason-Williams",
    author_email="gabryel.mason-williams@rfi.ac.uk",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"distrax": ["py.typed"]},
    test_suite="tests",
    classifiers=[
        "License :: OSI Approved :: Apache License, Version 2.0",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
    ],
    license="Apache License, Version 2.0",
    zip_safe=False,
    install_requires=[],
)
