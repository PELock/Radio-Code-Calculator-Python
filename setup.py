import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='radio_code_calculator',

    version='1.0.2',

    description='Radio Code Calculator is an online service along with Web API and SDK for generating car radio unlock codes for popular vehicle brands.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    keywords="radio code navigation calculator generator vehicle car automotive radiocode radiocodes api",

    url='https://www.pelock.com/products/radio-code-calculator',

    author='Bartosz Wójcik',
    author_email='support@pelock.com',

    license='Apache-2.0',

    packages=['radio_code_calculator'],

    install_requires=[
              'requests',
    ],

    zip_safe=False,

    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security",
          "Topic :: Multimedia :: Sound/Audio",
          "Natural Language :: English",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3"
      ],
)