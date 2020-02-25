from distutils.core import setup

setup(
    version='0.0.1',
    scripts=['scripts/info_srv_server.py','scripts/info_srv_client.py'],
    packages=['zr_hw_info'],
    package_dir={'': 'scripts'}
)
