import importlib
from importlib.abc import MetaPathFinder
from pathlib import Path

from .loaders import OverlayLoader

import pdb


class OverlayFinder(MetaPathFinder):
    def __init__(self, base_module, base_path, overlays):
        self.base_module = base_module
        self.base_path = Path(base_path)
        self.overlays = overlays
        self.source_loader = OverlayLoader(
            self.base_module,
            self.base_path,
            self.overlays
        )

    def get_source_path(self, base_path, module):
        module_path = base_path / "/".join(module) / '__init__.py'

        if not module_path.exists():
            module_path = (
                module_path.parent.parent / f"{module_path.parent.name}.py"
            )

            if not module_path.exists():
                return

        return module_path

    def find_spec(self, fullname, path=None, target=None):
        module = fullname.split('.')

        if module[0] != self.base_module:
            return None

        module_path = self.get_source_path(self.base_path, module[1:])

        if module_path:
            return importlib.util.spec_from_file_location(
                fullname,
                str(module_path),
                loader=self.source_loader
            )

        parent_module_name = ".".join(module[0:-1])
        parent_module = importlib.import_module(parent_module_name)

        lookup_paths = [
            Path(path)
            for path in parent_module.__path__
        ]

        for path in lookup_paths:
            module_path = self.get_source_path(path, [module[-1]])
            if module_path:
                break
            else:
                return

        if module_path.name == '__init__.py':
            search_location = [str(module_path.parent)]
        else:
            search_location = None

        return importlib.util.spec_from_file_location(
            fullname,
            str(module_path),
            loader=self.source_loader,
            submodule_search_locations=search_location
        )
