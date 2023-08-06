import os
import tempfile
from typing import AnyStr, Union
import xml.etree.ElementTree as eT

from stem.pkg import PROJECT_DIR, UTF8


def read_file(filename) -> AnyStr:
    with open(filename, "r", encoding="utf-8") as fh:
        text = fh.read()
    return text


def dump_xml_tree(tree: Union[eT.ElementTree, eT.Element],
                  namespace: str = None) -> str:
    if isinstance(tree, eT.Element):
        tree = eT.ElementTree(tree)

    with tempfile.TemporaryFile() as tmp:
        tree.write(tmp,
                   xml_declaration=True,
                   default_namespace=namespace,
                   method='xml',
                   encoding=UTF8)

        tmp.seek(0)
        output = tmp.read().decode(UTF8)

    # clean trailing blank or newline characters.
    output = "\n".join([i.strip() for i in output.split("\n") if i.strip()])

    return output


def load_xml(xml_path: str) -> str:
    """ Load any xml file under project directory. """
    _xml_path = xml_path
    if not xml_path.startswith("/"):
        _xml_path = path_join((PROJECT_DIR, xml_path))

    return read_file(_xml_path)


def path_join(paths: tuple) -> str:
    """ Load any xml file under project directory. """
    return os.path.join(*paths)
