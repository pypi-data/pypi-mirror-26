from setuptools import setup

setup(
    name='curobot',
    version='0.0.2',
    py_modules=["curobot", ],
    url='http://github.com/emre/qurobot',
    license='MIT',
    author='emre yilmaz',
    author_email='mail@emreyilmaz.me',
    description='Curation bot for steem network',
    entry_points={
        'console_scripts': [
            'curobot = curobot.curobot:main',
        ],
    },
    install_requires=["dataset", "steem==0.18.103"]
)
