from setuptools import setup, find_packages

setup(
    name="offking-tool",
    version="1.0.0",
    description="Educational Web Security Toolkit dedicated to talent 😘",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests>=2.25.0',
        'beautifulsoup4>=4.9.0',
    ],
    entry_points={
        'console_scripts': [
            'offking=offking:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)
