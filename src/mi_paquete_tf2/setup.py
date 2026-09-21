import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'mi_paquete_tf2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='josthinc',
    maintainer_email='tu_email@example.com',
    description='Paquete TF2 avanzado con marcos personalizados',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turtle_tf2_broadcaster = mi_paquete_tf2.turtle_tf2_broadcaster:main',
            'turtle_tf2_listener = mi_paquete_tf2.turtle_tf2_listener:main',
            'fixed_frame_tf2_broadcaster = mi_paquete_tf2.fixed_frame_tf2_broadcaster:main',
        ],
    },
)
