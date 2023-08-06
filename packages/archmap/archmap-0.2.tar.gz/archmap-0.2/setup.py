from setuptools import setup


# Find all of the tests in the 'tests' directory and return them.
def test_suite():
    import unittest
    suite = unittest.TestLoader().discover('tests')
    return suite


setup(
    name='archmap',
    version='0.2',
    description='ArchMap GeoJSON/KML generator',
    url='https://github.com/guyfawcus/ArchMap',
    license='Unlicense',
    py_modules=['archmap'],
    entry_points={'console_scripts': ['archmap=archmap:main']},
    install_requires=['bs4', 'geojson', 'simplekml'],
    test_suite='setup.test_suite'
)
