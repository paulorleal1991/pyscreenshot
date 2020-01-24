import pygame, tempfile, sys
from entrypoint2 import entrypoint
from path import Path
from easyprocess import EasyProcess
from time import sleep

rectsize = 50
first = True
refimgpath = None


def run(refimgpath, size=None):

    pygame.display.init()
    pygame.mouse.set_visible(0)

    if size:
        disp = pygame.display.set_mode(size)
    else:
        disp = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    w, h = pygame.display.get_surface().get_size()
    i = 0
    for x in range(0, w, rectsize):
        for y in range(0, h, rectsize):
            r = x * 255 / w
            g = y * 255 / h
            b = (i % 5) * 255 / 5
            pygame.draw.rect(disp, (r, g, b), (x, y, rectsize, rectsize))
            i += 1

    pygame.display.update()

    if refimgpath:
        pygame.image.save(disp, refimgpath)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        clock.tick(1)
    pygame.quit()


import atexit


def init():
    global first, refimgpath
    if first:
        first = False
        d = tempfile.mkdtemp(prefix="fillscreen")  
        d = Path(d)
        atexit.register(d.rmdir)
        refimgpath = d / "ref.bmp"
        python = sys.executable
        cmd = [
            python,
            "-m",
            "fillscreen",
            "--saveimage",
            refimgpath,
        ]
        proc = EasyProcess(cmd).start()
        atexit.register(proc.stop)
        while not refimgpath.exists():
            sleep(0.2)
    return refimgpath


@entrypoint
def main(size=None, saveimage=""):
    if size:
        size = map(int, size.split(":"))
        size = tuple(size)

    run(saveimage, size)

