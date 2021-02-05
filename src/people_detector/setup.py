from setuptools import setup
import os 
from glob import glob

package_name = 'people_detector'
python_version =  'python3.8' # site package-folder
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
        (os.path.join('share', package_name, 'models','yolo'), glob(os.path.join(package_name, 'src','models','yolo/*.*'))),
        (os.path.join('lib', python_version,'site-packages', package_name, "src"), glob(os.path.join(package_name, 'src/*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='manuel',
    maintainer_email='ruccimanue7@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
			'people_detector_node = people_detector.people_detector:main',
        ],
    },
)
