# Copyright (c) 2021 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from chikkarpy.config import download_dictionary

from setuptools import find_packages, setup

setup(
    name="chikkarpy",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="Python version of chikkar, a library for using the Sudachi synonym dictionary",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WorksApplications/chikkarpy",
    license="Apache-2.0",
    author="Works Applications",
    author_email="sudachi@worksap.co.jp",
    packages=find_packages(include=["chikkarpy", "chikkarpy.*"]),
    package_data={"": ["resources/*"]},
    entry_points={
        "console_scripts": ["chikkarpy=chikkarpy.command_line:main"]
    },
    install_requires=[
        "dartsclone~=0.9.0",
        "sortedcontainers>=2.1.0"
    ]
)

# Downloads the Sudachi Synonym dictionary
download_dictionary()
