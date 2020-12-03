import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="requestChecker",
    version="0.0.1",
    python_requires='>=3.6',
    install_requires=[
          'Flask==1.1.2',
          'Flask-RESTful==0.3.8',
          'Flask-JWT-Extended==3.25.0'
    ]
)
