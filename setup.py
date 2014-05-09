from setuptools import setup

setup(
    name='pysource',
    version='0.1',
    author='Dan Kilman',
    author_email='dankilman@gmail.com',
    packages=['pysource'],
    scripts=['pysource.sh'],
    description='Execute python functions from bash',
    zip_safe=False,
    install_requires=[
        'argh',
        'python-daemon'
    ],
)
