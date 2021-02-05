from setuptools import setup
import os 
from glob import glob

package_name = 'template_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    # Files we want to install, specifically launch files
    data_files=[
        # Install marker file in the package index
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
        (os.path.join('share', package_name, 'videos'), glob(os.path.join(package_name,'data','videos', '*.*'))),
        (os.path.join('share', package_name, 'images'), glob(os.path.join(package_name,'data','images', '*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='andrea',
    maintainer_email='ruccimanuel7@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
		'template_pkg_subscriber_node = template_pkg.template_pkg_subscriber:main',
        'template_pkg_publisher_node = template_pkg.template_pkg_publisher:main',
        'template_pkg_service_node = template_pkg.template_pkg_service:main',
        ],
    },
)
