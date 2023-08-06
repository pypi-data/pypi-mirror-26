from setuptools import setup, find_packages

setup(
    name='django-file-picker',
    version='0.9.1',
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(exclude=['sample_project']),
    include_package_data=True,
    url='https://github.com/caktus/django-file-picker/',
    license='BSD',
    description='Pluggable file picker',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
    long_description=open('README.rst').read(),
    install_requires=[
        'sorl-thumbnail>=12.4a1',
        'Pillow>=3.1.0,<4.0',
    ],
    zip_safe=False,  # because we're including media that Django needs
)
