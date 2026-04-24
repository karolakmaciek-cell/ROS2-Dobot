from setuptools import find_packages, setup

package_name = 'lab2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lab2_launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='macwil',
    maintainer_email='maciej.wileczek@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'tower_maker = lab2.tower_maker:main',
        ],
    },
)