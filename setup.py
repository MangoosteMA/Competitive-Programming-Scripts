from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as readmeFile:
    readme = readmeFile.read()

setup(
    name='competitive_programming_scripts',
    version='0.1',
    author='Alexey Mikhnenko',
    description=('Scripts for competitive programming'),
    keywords='competitive programming scripts',
    url='https://github.com/MangoosteMA/Competitive-Programming-Scripts/',
    include_package_data=True,
    packages=find_packages(),
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[
        'setuptools',
        'beautifulsoup4',
        'requests',
    ],
    python_requires='>=3.1',
    entry_points = {
        'console_scripts': [
            'stress_test=cpscripts.stress_test:main',
            'interact=cpscripts.interact:main',
            'drun=cpscripts.test:main',
            'bld=cpscripts.test:bld',
            'fbld=cpscripts.test:fbld',
            'cmpl=cpscripts.test:cmpl',
            'fcmpl=cpscripts.test:fcmpl',
            'setup_problem=cpscripts.setup_problem:main',
            'setup_contest=cpscripts.setup_contest:main',
        ],
    },
    data_files=['cpscripts/settings.json']
)
