from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name = 'intriniorealtime',
    packages = ['intriniorealtime'],
    version = '2.0.0',
    author = 'Intrinio Python SDK for Real-Time Stock Prices',
    author_email = 'success@intrinio.com',
    url = 'https://intrinio.com',
    description = 'Intrinio Python SDK for Real-Time Stock Prices',
    long_description = readme(),
    install_requires = ['requests','websocket-client'],
    download_url = 'https://github.com/intrinio/intrinio-realtime-python-sdk/archive/v2.0.0.tar.gz',
    keywords = ['realtime','stock prices','intrinio','stock market','stock data','financial'],
    classifiers = [
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment'
    ]
)
