from setuptools import find_packages, setup


required = [
    'jax',
    'jaxlib',
    'numpy',
]

extras = {
    'dev': ['pytest']
}

setup(
    name='uncertain-math',
    description='''
    An engineering toolkit for taking measurements and propagating uncertainty
    ''',
    keywords='engineering uncertainty quantification',
    url='https://github.com/haydenshively/Uncertain-Math',
    license='MIT',
    author='Hayden Shively',
    author_email='haydenshively@gmail.com',
    packages=find_packages(),
    install_requires=required,
    extras_require=extras,
    python_requires='>=3.6',
)
