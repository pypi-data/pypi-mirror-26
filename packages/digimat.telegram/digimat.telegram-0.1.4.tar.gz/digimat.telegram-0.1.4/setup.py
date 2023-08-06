from setuptools import setup, find_packages

setup(
    name='digimat.telegram',
    version='0.1.4',
    description='Digimat Telegram Bot',
    namespace_packages=['digimat'],
    author='Frederic Hess',
    author_email='fhess@splust.ch',
    url='http://www.digimat.ch',
    license='PSF',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'Pillow',
        'python-telegram-bot',
        'setuptools'
    ],
    dependency_links=[
        ''
    ],
    zip_safe=False)
