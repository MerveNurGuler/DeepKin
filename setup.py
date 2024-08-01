from setuptools import setup, find_packages

setup(
    name='DeepKin',
    version='1.0.0',
    description='Tool for mismatch calculation and relatedness prediction using CNN for genetic data.',
    author='Merve N Güler, Ardan Yılmaz, Büşra Katırcıoğlu',
    author_email='merveglr2626@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'scikit-learn',
    ],
    package_data={
        'DeepKin': ['models/*.pt'],
    },
    entry_points={
        'console_scripts': [
            'DeepKin=DeepKin.main:main',
        ],
    },
)
