from setuptools import setup, find_namespace_packages

setup(
    name='seekret.apitest',
    version='0.1.0',
    author='Seekret Software Ltd.',
    author_email='info@seekret.com',
    description="Seekret's library for API testing runtime",
    long_description="""
    # Seekret API testing runtime

    The `seekret.apitest` package contains runtime functions and tools intended to ease API testing.
    """,
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=('seekret.apitest', 'seekret.apitest.*')),
    install_requires=['python-box~=5.3.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    project_urls={
        'Bug Tracker': 'https://github.com/seek-ret/tests-rtl/issues'
    },
    url='https://github.com/seek-ret/tests-rtl'
)
