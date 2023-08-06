from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-edgegrid',
    description='Edgegrid plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='1.0.6',
    python_requires=">=2.7.10",
    author='Kirsten Hunter',
    author_email='khunter@akamai.com',
    license='Apache 2.0',
    url='https://github.com/akamai-open/httpie-edgegrid',
    download_url='https://github.com/akamai-open/httpie-edgegrid',
    py_modules=['httpie_edgegrid'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_oauth1 = httpie_edgegrid:EdgeGridPlugin'
        ]
    },
    install_requires=[
        'httpie >= 0.9.2',
	'edgegrid-python >= 1.0.9',
        'pyOpenSSL >= 0.13'
    ],
)
