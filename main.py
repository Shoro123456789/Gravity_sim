from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import math
from direct.task import Task
from direct.showbase.ShowBaseGlobal import globalClock
from random import randint
G=6.67*(10**(-11))
#class Sphere:
 #   def __init__(self, scale, colour, position):
#        self.model = ShowBase.loader.loadModel("models/misc/sphere")
 #       self.model.setScale(scale)
   #     self.model.setPos(position)
  #      self.model.setColor(colour)
    #def reparentTo(self, parent):
     #   self.model.reparentTo(parent)

class Body:
    def __init__(self, loader, render, mass, scale, colour, position, velocity=None, acceleration=None):
        self.model = loader.loadModel("models/misc/sphere")
        self.model.reparentTo(render)
        self.model.setScale(scale)
        self.model.setPos(position)
        self.model.setColor(*colour)

        self.mass=mass
        self.velocity=velocity if velocity is not None else Vec3(0, 0, 0)
        self.acceleration=acceleration if acceleration is not None else Vec3(0, 0, 0)
        
    def getPos(self):
        return self.model.getPos()
        
    def setPos(self, position):
        self.model.setPos(position)
    def force(self, other):
        diff=other.getPos()-self.getPos()
        r= diff.length()
        if r == 0:
            return Vec3(0,0,0)
        force=(G)*self.mass*other.mass/(r*r)
        force_vector=(diff/r)*force
        return force_vector
    def applyForce(self, force, dt):
        self.acceleration = force/self.mass
        self.velocity += self.acceleration * dt
        self.setPos(self.getPos() + self.velocity * dt)


class MyApp(ShowBase):

    def __init__(self):
        
        ShowBase.__init__(self)
#        self.model = self.loader.loadModel("models/misc/sphere")
#        self.model.reparentTo(self.render)
#        self.model.setScale(2)
#        self.model.setPos(0, 10, 0)
#        self.geom = self.model.find("**/+GeomNode").node()
 #       self.model.setColor(0.6, 0.6, 1.0, 1.0)
#        self.sphere = Sphere(2, (0.6, 0.6, 1.0, 1.0), (0, 10, 0))
#        self.sphere.reparentTo(self.render)
#        self.sphere = self.loader.loadModel("models/misc/sphere")
#        self.sphere.reparentTo(self.render)
#        self.sphere.setScale(2)
#        self.sphere.setPos(10, 10, 10)
#        self.sphere.setColor(0.1, 0.8, 1.0, 1.0)
#        self.mass1=100000000000.0
#        self.mass2=100000000000.0
#        self.velocity=Vec3(0,0,0)  
#        self.acceleration=Vec3(0,0,0)      
        self.bodies = [
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(0.6, 0.6, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30))),
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(0.1, 0.8, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30))),
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(1.0, 0.0, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30))),
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(1.0, 0.0, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30))),
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(1.0, 0.0, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30))),
            Body(self.loader, self.render, mass=1e11, scale=2, colour=(1.0, 0.0, 1.0, 1.0), position=(randint(0, 30), randint(0, 30), randint(0, 30)))
        ]

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        forces = []
        for body in self.bodies:
            F=Vec3(0,0,0)
            for other in self.bodies:
                if body is not other:
                    F+=Body.force(body, other)
            forces.append(F)
        for body, F in zip(self.bodies, forces):
            Body.applyForce(body, F, dt)

#        diff=-self.sphere.getPos()+self.model.getPos()
#        self.r= diff.length()
#        if self.r == 0:
#            return Task.cont
#        print(self.r)
#        self.force=(G)*self.mass1*self.mass2/(self.r*self.r)
#        print(self.force)
#        self.force_vector=(diff/self.r)*self.force
#        print(self.force_vector)
#        self.acceleration=self.force_vector/self.mass2
#        self.velocity += self.acceleration * dt
#        self.sphere.setPos(self.sphere.getPos() + self.velocity * dt)
#        print(self.velocity)

        return Task.cont


app = MyApp()
app.run()
