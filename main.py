from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import math
from direct.task import Task
from direct.showbase.ShowBaseGlobal import globalClock
from random import randint
import simplepbr
from direct.gui.DirectGui import *

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
        self.scale=scale
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

    def distance_to(self, other):
        diff = other.getPos() - self.getPos()
        r = diff.length()
        return diff, r

    def force(self, other):
        diff=other.getPos()-self.getPos()
        r= self.distance_to(other)[1]
        if r == 0:
            return Vec3(0,0,0)
        force=(G)*self.mass*other.mass/(r*r)
        force_vector=(diff/r)*force
        return force_vector
    def applyForce(self, force, dt):
        self.acceleration = force/self.mass
        self.velocity += self.acceleration * dt
        self.setPos(self.getPos() + self.velocity * dt)
    def is_colliding(self, other):
        if self.distance_to(other)[1] < self.scale + other.scale:
#            print("collision")
            return True
        else:
#            print("no collision")
            return False
    def apply_collision(self, other):
        normal = (other.getPos() - self.getPos()).normalized()

        self_normal_speed = self.velocity.dot(normal)
        self_tangential = self.velocity - normal * self_normal_speed

        other_normal_speed = other.velocity.dot(normal)
        other_tangential = other.velocity - normal * other_normal_speed

        new_self_normal_speed = ((self.mass - other.mass) * self_normal_speed
                                + 2 * other.mass * other_normal_speed) / (self.mass + other.mass)
        new_other_normal_speed = ((other.mass - self.mass) * other_normal_speed
                                + 2 * self.mass * self_normal_speed) / (self.mass + other.mass)

        new_self_velocity = normal * new_self_normal_speed + self_tangential
        new_other_velocity = normal * new_other_normal_speed + other_tangential

        self.velocity = new_self_velocity
        other.velocity = new_other_velocity


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)


        # simplepbr.init(enable_shadows=True)
        # directional = DirectionalLight("directional")
        # directional.setColor((4.0, 3.8, 3.4, 1))
        # directional.setShadowCaster(True, 2048, 2048)  
        # directional_np = self.render.attachNewNode(directional)
        # directional_np.setHpr(45, -60, 0)
        # self.render.setLight(directional_np)
        # ambient = AmbientLight("ambient")
        # ambient.setColor((0.15, 0.15, 0.18, 1))  # dim, slightly cool fill
        # ambient_np = self.render.attachNewNode(ambient)
        # self.render.setLight(ambient_np)
                
    #    self.model = self.loader.loadModel("models/misc/sphere")
    #    self.model.reparentTo(self.render)
    #    self.model.setScale(2)
    #    self.model.setPos(0, 10, 0)
    #    self.geom = self.model.find("**/+GeomNode").node()
    #    self.model.setColor(0.6, 0.6, 1.0, 1.0)
    #    self.sphere = Sphere(2, (0.6, 0.6, 1.0, 1.0), (0, 10, 0))
    #    self.sphere.reparentTo(self.render)
    #    self.sphere = self.loader.loadModel("models/misc/sphere")
    #    self.sphere.reparentTo(self.render)
    #    self.sphere.setScale(2)
    #    self.sphere.setPos(10, 10, 10)
    #    self.sphere.setColor(0.1, 0.8, 1.0, 1.0)
    #    self.mass1=100000000000.0
    #    self.mass2=100000000000.0
    #    self.velocity=Vec3(0,0,0)  
    #    self.acceleration=Vec3(0,0,0) 
        self.slider = DirectSlider(range=(0,5), value=1, pageSize=1,
    pos=(-0.8, 0, 0.8),
    scale=0.3,
    frameColor=(0.15, 0.15, 0.18, 0.9),   # dark translucent track
    thumb_frameColor=(0.4, 0.7, 1.0, 1),  # accent-colored thumb/handle
    thumb_relief=DGG.FLAT,)

        self.bodies = [

        Body(self.loader, self.render, mass=1e14, scale=3, colour=(1.0, 0.9, 0.6, 1.0), position=(0, 0, 0), velocity=Vec3(0, 0, 0)),
        Body(self.loader, self.render, mass=1e5, scale=1, colour=(0.3, 0.6, 1.0, 1.0), position=(10, 0, 0), velocity=Vec3(0, 0, 25.83))
        ]

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()*self.slider['value']
        forces = []
        for body in self.bodies:
            F=Vec3(0,0,0)
            for other in self.bodies:
                if body is not other:
                    F+=Body.force(body, other)
#                    Body.is_colliding(body, other)
            forces.append(F)
        for body, F in zip(self.bodies, forces):
            Body.applyForce(body, F, dt)
        for i in range(len(self.bodies)):
            for j in range(i+1, len(self.bodies)):
                if Body.is_colliding(self.bodies[i], self.bodies[j]):
                    Body.apply_collision(self.bodies[i], self.bodies[j])
            

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
