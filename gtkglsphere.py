

import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class GridWindow(Gtk.ApplicationWindow):
  def __init__(self, app):
    Gtk.Window.__init__(self, application = app,
                        default_width=1000,
                        default_height=200,
                        border_width=2,
                        name = "MyWindow")

    # Main drawing area
    self.area = DrawArea()
    self.area.set_size_request(1000,800)
    # To attach everything
    grid = Gtk.Grid()

    grid.attach(self.area,1,0,1,1)
    self.add(grid)

class DrawArea(Gtk.GLArea):
    def __init__(self):
        Gtk.GLArea.__init__(self)
        self.connect("realize", self.on_realize)
        self.connect("render", self.render)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(600, 800)
        glutCreateWindow(b'my OpenGL window')
        glutDisplayFunc(self.render)
        glutMainLoop()

    def on_realize(self, area):
        ctx = self.get_context()
        ctx.make_current()
        err = self.get_error()
        if err:
            print("The error is {}".format(err))

    def render(self):
        glClearColor(.7,.70,.70,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        color = [1.0,0.,0.,1.]
        glutSolidSphere(20,20,20)
        glutSwapBuffers()
        glutPostRedisplay()
        return True

class draw(Gtk.Application):
  def __init__(self):
    Gtk.Application.__init__(self)
  def do_activate(self):
    win = GridWindow(self)
    win.show_all()


app = draw()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
