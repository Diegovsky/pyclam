import setuptools

setuptools.setup(
    name='PyClam',
    version='1.3.5',
    packages=setuptools.find_packages(),
    author="Diegovsky",
    license="None",
    scripts=["PyClam"],
    description="Shell-like system caller",
    long_description="A thin wrapper around Popen that aims to look like a shell",
    url="https://github.com/Diegovsky/pyclam",
)
