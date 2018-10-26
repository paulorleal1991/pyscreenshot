from PIL import ImageChops
from easyprocess import EasyProcess
from nose.tools import eq_, with_setup
import pyscreenshot
from pyvirtualdisplay import Display
import time

from config import bbox_ls
from image_debug import img_debug


long_txt = '''# file GENERATED by distutils, do NOT edit
LICENSE.txt
README.rst
TODO.rst
pavement.py
requirements.txt
setup.py
versioneer.py
docs/api.rst
docs/conf.py
docs/examples.rst
docs/help.rst
docs/index.rst
docs/links.rst
docs/readme.rst
docs/speed.rst
docs/struct.rst
pyscreenshot/__init__.py
pyscreenshot/_version.py
pyscreenshot/loader.py
pyscreenshot/check/__init__.py
pyscreenshot/check/speedtest.py
pyscreenshot/check/versions.py
pyscreenshot/check/virtualtest.py
pyscreenshot/examples/__init__.py
pyscreenshot/examples/show.py
pyscreenshot/examples/showall.py
pyscreenshot/plugins/__init__.py
pyscreenshot/plugins/gtkpixbuf.py
pyscreenshot/plugins/imagemagick.py
pyscreenshot/plugins/mac_screencapture.py
pyscreenshot/plugins/pil.py
pyscreenshot/plugins/qtgrabwindow.py
pyscreenshot/plugins/scrot.py
pyscreenshot/plugins/wxscreen.py
'''


def check_ref(backend, bbox):
    ref = 'scrot'
    img_ref = pyscreenshot.grab(bbox=bbox, backend=ref, childprocess=True)
    im = pyscreenshot.grab(bbox=bbox, backend=backend, childprocess=True)

    img_ref = img_ref.convert('RGB')
    im = im.convert('RGB')

    eq_('RGB', img_ref.mode)
    eq_('RGB', im.mode)

    img_debug(img_ref, ref + str(bbox))
    img_debug(im, backend + str(bbox))

    img_diff = ImageChops.difference(img_ref, im)
    diff_bbox = img_diff.getbbox()
    if diff_bbox:
        img_debug(img_diff, 'img_diff' + str(diff_bbox))
    eq_(diff_bbox, None, 'different image data %s!=%s bbox=%s diff_bbox=%s' %
        (ref,        backend, bbox, diff_bbox))


def backend_ref(backend):
    with Display(visible=0, size=(400, 500)):
        with EasyProcess('xlogo'):
            with EasyProcess('xmessage -center "%s"' % long_txt):
                time.sleep(2)
                for bbox in bbox_ls:
                    print('bbox: {}'.format(bbox))
                    print('backend: %s' % backend)
                    check_ref(backend, bbox)
