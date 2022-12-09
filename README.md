OverlayModule
=============

This module finder makes it possible to load modules with overlays. This
can be useful in cases you try to customize some kind of application in places
at moment that is out of your control.

For example, it is useful when you want to customize an application that make
extensive uses of global. This module will allow you to load an overlay over
a module that is being loaded right after the module has been loaded.

Let say you have this module `a.b`. You'd want to customize the class `a.b:Application`.
To make sure that something that inherits later from `a.b:Application` will in fact
inherit from `o.overlay.a.b:Application`.

When the module is being loaded it will first load `a.b` then it will execute the module
`o.overlay.a.b` on top of the module `a.b`.

In short, this is more or less monkey patching on steroid.

How to use:
-----------

For the script using it:

    import importlib
    from overlaymodule import OverlayFinder

    module_spec = importlib.util.find_spec('a')
    module_path = odoo_spec.submodule_search_locations[0]

    sys.meta_path.insert(
        0,
        OverlayFinder(
            'a',
            module_path,
            overlays=[
                "o.overlay",
            ]
        )
    )

    from a.b import Application, OldApplication


A module overlay `o.overlay.a.b`

    # since a.b is already loaded, it's possible to import it within itself!
    from a.b import Application as OldApplication

    class Application(OldApplication):
        pass
