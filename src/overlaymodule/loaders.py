from pathlib import Path
import importlib
from importlib import _bootstrap
from importlib._bootstrap_external import SourceFileLoader
import pdb


class OverlayLoader(SourceFileLoader):

    def __init__(self, base_module, base_path, overlays):
        self.base_module = base_module
        self.base_path = base_path
        self.overlays = overlays
        self._overlayed_modules = {}
        self._looked_up_overlays = False
        self.modules = {}

    def get_filename(self, fullname):
        if fullname in self.modules:
            module = self.modules[fullname]
            if Path(module.__file__).exists():
                return module.__file__

        module = fullname.split('.')
        module_path = None

        if module[0] == self.base_module:
            module_path = self.base_path / "/".join(module[1:])

            if module_path.is_dir():
                module_path = module_path / '__init__.py'
            else:
                module_path = module_path.parent / f"{module_path.name}.py"

            if not module_path.exists():
                raise ModuleNotFoundError(f"Couldn't load source for {fullname}")
        else:
            spec = importlib.util.find_spec(fullname)

            if not spec or not spec.origin:
                raise ModuleNotFoundError(f"Couldn't load source for {fullname}")

            module_path = Path(spec.origin)

        return str(module_path)

    def overlayed_modules(self, module):
        if not self._looked_up_overlays:
            for overlay in self.overlays:
                spec = importlib.util.find_spec(str(overlay))

                if not spec:
                    continue

                for location in spec.submodule_search_locations:
                    path = Path(location)
                    for file in path.glob("**/*.py"):
                        module_path = file.relative_to(path)

                        if module_path.name == '__init__.py':
                            module_path = module_path.parent
                        else:
                            module_path = module_path.parent / module_path.name[0:-3]

                        module_name = ".".join(str(module_path).split('/'))

                        module_name_fqn = f"{spec.name}.{module_name}"

                        if module_name not in self._overlayed_modules:
                            self._overlayed_modules[module_name] = [module_name_fqn]
                        else:
                            self._overlayed_modules[module_name].append(module_name_fqn)

            self._looked_up_overlays = True

        return self._overlayed_modules.get(module.__name__, [])

    def exec_module(self, module):
        self.modules[module.__name__] = module

        super().exec_module(module)

        for overlay in self.overlayed_modules(module):
            code = self.get_code(overlay)
            _bootstrap._call_with_frames_removed(exec, code, module.__dict__)
