from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/led8_embd.py','scripts/led8_pc.py'],
    packages=['zr_led8_595'],
    package_dir={'': 'scripts'}
)
