from model.model import Model
from controller.controller import Controller
model = Model()
controller = Controller(model=model)

controller.go()