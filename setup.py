import os
from distutils.command.build import build

from django.core import management
from setuptools import setup, find_packages


try:
    with open(
        os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8'
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ''


class CustomBuild(build):
    def run(self):
        management.call_command('compilemessages', verbosity=1, interactive=False)
        build.run(self)


cmdclass = {'build': CustomBuild}


setup(
    name='pretalx-pages',
    version='0.1.0',
    description="Static pages for pretalx, e.g. information, venue listings, a code of conduct, etc.",
    long_description=long_description,
    url='https://github.com/pretalx/pretalx-pages',
    author='Moshe Nahmias',
    author_email='moshegrey+pretalx_pages@gmail.com',
    license='Apache Software License',
    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretalx.plugin]
pretalx_pages=pretalx_pages:PretalxPluginMeta
""",
)
