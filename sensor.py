from stmpy import Driver, Machine
import keyboard

class Sensor:
    def __init__(self, driver, actuator, name='sensor'):
        self.name = name
        self.driver = driver
        self.actuator = actuator
        self.stm = Machine(
            name = self.name,
            transitions = [
                {'source' : 'initial', 'target' : 'idle', 'effect' : 'start()'},
            {'source' : 'idle', 'target' : 'active', 'trigger' : 'space_pressed', 'effect' : 'on_press()'},
            {'source' : 'idle', 'target' : 'idle', 'trigger' : 'space_released'},
            {'source' : 'active', 'target' : 'idle', 'trigger' : 'space_released', 'effect' : 'on_release()'},
            {'source' : 'active', 'target' : 'active', 'trigger' : 'space_pressed'}
            ],
            states=[{'name' : 'idle'} ,{ 'name' : 'pressed'}],
            obj=self)
        self.driver.add_machine(self.stm)

    def info(self, s):
        print(f'Sensor: {s}')
    def start(self):
        keyboard.on_press_key("ctrl", lambda _: self.stm.send('space_pressed'))
        keyboard.on_release_key("ctrl", lambda _: self.stm.send('space_released'))

    def on_press(self):
        self.actuator.stm.send('hand_in_front')
    def on_release(self):
        self.actuator.stm.send('hand_removed')

class Button(Sensor):
    def on_press(self):
        self.actuator.stm.send('button_pressed')
    def on_release(self):
        pass

