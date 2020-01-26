from entrypoint2 import entrypoint

import pyscreenshot
from pyscreenshot.imcodec import codec


@entrypoint
def main(filename="", bbox="", backend="", show=False):
    """Copy the contents of the screen to file. 
    Full screen is selected if bounding box coordinates are zero: 0,0,0,0

    :param filename: output file
    :param show: show image
    :param bbox: bounding box coordinates x1:y1:x2:y2
    :param backend: back-end can be forced if set (example:scrot, wx,..),
                    otherwise back-end is automatic
    """
    backend = backend if backend else None
    if bbox:
        x1, y1, x2, y2 = map(int, bbox.split(":"))

    bbox = None
    if x1 or y1 or x2 or y2:
        bbox = x1, y1, x2, y2

    im = pyscreenshot.grab(bbox=bbox, childprocess=False, backend=backend)
    if filename:
        b = codec[0](im)
        with open(filename, "wb") as f:
            f.write(b)
    if show:
        im.show()
