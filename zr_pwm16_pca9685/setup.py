from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/pwm16_embd.py','scripts/pwm16_pc.py'],
    packages=['zr_pwm16_pca9685'],
    package_dir={'': 'scripts'}
)
