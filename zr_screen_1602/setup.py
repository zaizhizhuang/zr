from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/screen_1602_pub.py','scripts/screen_1602_embd.py','scripts/screen_1602_pc.py'],
    packages=['zr_screen_1602'],
    package_dir={'': 'scripts'}
)
