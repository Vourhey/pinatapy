import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pinatapy-vourhey",
    version="0.1.3",
    author="Vadim Manaenko",
    author_email="vadim.razorq@gmail.com",
    description="Non-official Pinata.cloud library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vourhey/pinatapy",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
