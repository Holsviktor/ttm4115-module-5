from stmpy import Driver, Machine
from sensor import Sensor
import keyboard

class HeadLamp:
    def __init__(self,driver, name = 'headlamp'):
        self.name = name
        self.driver = driver
        self.states = [
            {
                'name' : 'light_off'
            },
            {
                'name' : 'light_off_primed'
            },
            {
                'name' : 'light_on'
            },
            {
                'name' : 'light_on_primed'
            }
        ]
        initial_transition = [{
                'source' : 'initial',
                'target' : 'light_off',
                'effect' : 'do_light(False)'
        }]
        headlamp_timer_transitions = [
            {
                'trigger':'t',
                'source':'light_off',
                'target':'light_off'
            },
            {
                'trigger':'t',
                'source':'light_off_primed',
                'target':'light_off',
            },
            {
                'trigger':'t',
                'source':'light_on_primed',
                'target':'light_on'
            },
            {
                'trigger':'t',
                'source':'light_on',
                'target':'light_on'
            }
        ]
        button_press_transitions = [
            {
                'trigger':'hand_in_front',
                'source':'light_off',
                'target':'light_off_primed',
                'effect':'start_timer("t",500)'
            },
            {
                'trigger':'hand_removed',
                'source':'light_off',
                'target':'light_off'
            },
            {
                'trigger':'hand_removed',
                'source':'light_off_primed',
                'target':'light_on',
                'effect' : 'do_light(True)'
            },
            {
                'trigger':'hand_in_front',
                'source':'light_on',
                'target':'light_on_primed',
                'effect':'start_timer("t",500)'
            },
            {
                'trigger':'hand_removed',
                'source':'light_on',
                'target':'light_on'
            },
            {
                'trigger':'hand_removed',
                'source':'light_on_primed',
                'target':'light_off',
                'effect' : 'do_light(False)'
            }

        ]
        self.transitions = initial_transition + headlamp_timer_transitions + button_press_transitions
        self.stm = Machine(name=self.name, transitions = self.transitions, states=self.states, obj=self)
        driver.add_machine(self.stm)

    def do_light(self,on):
        print(f'\r\033[K[{on * "\033[33m*\033[0m"}{(not on) * " "}] <- headlamp', end='')


if __name__ == '__main__':
    driver = Driver()
    headlamp = HeadLamp(driver)
    Sensor(driver, headlamp)
    driver.start()
    driver.wait_until_finished()

