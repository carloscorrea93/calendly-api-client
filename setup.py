from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='calendly-api-client',
    version='0.0.1',
    author='Carlos Correa',
    author_email='carlosx-34@hotmail.com',
    description='Python package to use the Calendly API V2',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/carloscorrea93/calendly-api-client',
    keywords=['calendly', 'api client', 'calendly api v2', 'calendly api'],
    python_requires='>=3.7',
    install_requires=['requests>=2.25', 'typing-extensions>=3.7'],
)
