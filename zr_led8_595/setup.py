from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/led8_pub.py','scripts/led8_sub.py'],
    packages=['zr_led8_595'],
    package_dir={'': 'scripts'}
)
