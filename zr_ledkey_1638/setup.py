from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/ledkey_embd.py','scripts/ledkey_pc.py'],
    packages=['zr_ledkey_1638'],
    package_dir={'': 'scripts'}
)
