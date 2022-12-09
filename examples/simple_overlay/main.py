import sys
from overlaymodule import OverlayFinder
from pathlib import Path


sys.meta_path.insert(
    0,
    OverlayFinder(
        'a',
        Path.cwd() / 'a',
        overlays=[
            "o.overlay"
        ]
    )
)

from a.b import hello

hello()
