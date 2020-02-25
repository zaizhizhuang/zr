from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/cmd_srv_server.py','scripts/cmd_srv_client.py'],
    packages=['zr_hw_cmd'],
    package_dir={'': 'scripts'}
)
