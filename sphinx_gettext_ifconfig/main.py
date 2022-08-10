"""
    sphinx-gettext-ifconfig
    ~~~~~~~~~~~~~~~~~~~~~~~

    Modifies the ``.. ifconfig::`` directive so that its content can be included in the .pot files
    irrespective of the expression evaluation.
    
    Usage::

        .. ifconfig:: releaselevel in ('alpha', 'beta', 'rc')

           This stuff is only included in the built docs for unstable versions.

    The argument for ``ifconfig`` is a plain Python expression, evaluated in the
    namespace of the project configuration (that is, all variables from
    ``conf.py`` are available.)

    :copyright: Copyright 2007-2022 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes
import sphinx
from sphinx.application import Sphinx
from sphinx.ext.ifconfig import ifconfig


def process_ifconfig_nodes(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    ns = {confval.name: confval.value for confval in app.config}
    ns.update(app.config.__dict__.copy())
    ns['builder'] = app.builder.name
    for node in doctree.findall(ifconfig):
        if (ns['builder'] != 'gettext'):
            try:
                res = eval(node['expr'], ns)
            except Exception as err:
                # handle exceptions in a clean fashion
                from traceback import format_exception_only
                msg = ''.join(format_exception_only(err.__class__, err))
                newnode = doctree.reporter.error('Exception occurred in '
                                                 'ifconfig expression: \n%s' %
                                                 msg, base_node=node)
                node.replace_self(newnode)
            else:
                if not res:
                    node.replace_self([])
                else:
                    node.replace_self(node.children)
        else:
            node.replace_self(node.children)