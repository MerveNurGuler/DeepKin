from setuptools import setup, find_packages

setup(
    name='deep_mismatch',
    version='1.0.0',
    description='Tool for mismatch calculation and prediction using CNN for genetic data.',
    author='Merve N Güler',
    author_email='merveglr2626@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'scikit-learn',
    ],
    package_data={
        'deep_mismatch': ['models/*.pt'],
    },
    entry_points={
        'console_scripts': [
            'deep_mismatch=deep_mismatch.main:main',
        ],
    },
)