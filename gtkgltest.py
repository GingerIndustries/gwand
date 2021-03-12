from OpenGL.GL import *
from OpenGL.GLU import *
import time

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()



class MyGLArea(Gtk.GLArea):
	def __init__(self):
		Gtk.GLArea.__init__(self, has_depth_buffer = True)
		self.connect("realize", self.on_realize)
		self.connect("render", self.render)
	
	
	def on_realize(self, area):
		ctx = self.get_context()
		ctx.make_current()
		err = self.get_error()
		if err:
			print("The error is {}".format(err))
		GLib.timeout_add(1000, self.emit, "render", self.get_context())
	
	def render(self, area, ctx):
		print("render")
		ctx.make_current()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glRotatef(1, 3, 0, 0)
		Cube()
		glFlush()
		return True

window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

display = (800,600)
window.set_size_request(*display)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glTranslatef(0.0,5.0, -5)

gl = MyGLArea()
window.add(gl)

window.show_all()
Gtk.main()
