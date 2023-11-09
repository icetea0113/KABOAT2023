import glob
import os
from setuptools import setup

package_name = 'autonomous'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob.glob("launch/*.launch.py"),
        ),
        (os.path.join("share", package_name, "param"), glob.glob("param/*.yaml")),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='icetea0113',
    maintainer_email='v2msyo@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gogo = autonomous.gogo:main',
            'lidar_gogo = autonomous.lidar_gogo:main',
        ],
    },
)
