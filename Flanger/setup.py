from setuptools import  setup, find_packages

setup(
    name='Flanger',
    version='0.0.1',
    packages=find_packages(),
    description='Flask Restful',
    include_package_data=True,
    license='MIT',
    keywords='python',
    author='xupeng',
    author_email='None',
    url='None',
    install_requires=[
        'Flask>=1.1.1',
        'Flask-RESTful>=0.3.7',
        'Flask-SQLAlchemy>=2.4.1',
    ]
)
