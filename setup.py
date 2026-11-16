from setuptools import setup, find_packages

setup(
    name="python_microfinance_banking_engine",
    version="1.0.0",
    description="Python Microfinance Banking Engine - Production Grade Python Engine",
    author="Shyamkumar Pandey",
    author_email="shyampandey1104@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=["pytest>=7.0.0"]
)
