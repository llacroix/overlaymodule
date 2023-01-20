import setuptools
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def find_in_path(module, path):
    def find_files(cur_path):
        files = []
        for path in cur_path.iterdir():
            if not path.is_dir():
                files.append(str(path))
            else:
                files += find_files(path)
        return files

    module_path = Path.cwd() / "src" / module / path

    return find_files(module_path)


setuptools.setup(
    name="overlaymodule",
    version="0.0.3",
    author="Loïc Faure-Lacroix",
    author_email="lamerstar@gmail.com",
    description="A Special Module Loader that can load modules with overlays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llacroix/overlaymodule",
    project_urls={
        "Bug Tracker": "https://github.com/llacroix/overlaymodule/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.4",
    install_requires=[
        # 'importlib',
    ],
    entry_points={
    }
)
