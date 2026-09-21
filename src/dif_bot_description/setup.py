import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dif_bot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Registra el paquete en el índice de recursos de ament
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        
        # Copia el manifiesto package.xml
        ('share/' + package_name, ['package.xml']),
        
        # Instala todos los archivos de lanzamiento (.launch.py)
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        
        # Instala todos los archivos de descripción robotica (.xacro / .urdf)
        (os.path.join('share', package_name, 'urdf'), glob(os.path.join('urdf', '*.xacro'))),
        
        # Instala los archivos de configuración de parámetros (bridge_config.yaml, etc.)
        (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*'))),
        
        # Instala los perfiles de visualización de RViz (.rviz)
        (os.path.join('share', package_name, 'rviz'), glob(os.path.join('rviz', '*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='josthinc',
    maintainer_email='tu_correo@ejemplo.com',
    description='Paquete de descripcion y simulacion para el robot diferencial completo',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
