__version__ = "0.0.1"

from typing import Any, Dict, List

import sphinx
from sphinx.application import Sphinx

def setup(app: Sphinx) -> Dict[str, Any]:

    from sphinx_gettext_ifconfig.main import process_ifconfig_nodes
    
    for listeners in app.events.listeners.values():
        for listener in listeners[:]:
            if (listener.handler.__name__ == 'process_ifconfig_nodes'):
                listeners.remove(listener)
        
    app.connect('doctree-resolved', process_ifconfig_nodes)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
