from setuptools import setup, find_packages

setup(
    name='product_scrapers',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='alifarslan',
    author_email='huwaiguest@gmail.com',
    description='',
    package_data={'splash_crawlera_example': ['scripts/*.lua', ]},
    entry_points={'scrapy': ['settings = splash_crawlera_example.settings']},
)
