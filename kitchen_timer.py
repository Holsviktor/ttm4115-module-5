from stmpy import Driver, Machine
from sensor import Button

class Kitchen:
    def __init__(self, stm):
        self.stm = stm
    def set_leds(self, a, b, c, d):
        s = '\r\033[K['
        if a:
            s += '\033[34m*'
        else:
            s += ' '
        if b:
            s += '\033[32m*'
        else:
            s += ' '
        if c:
            s += '\033[33m*'
        else:
            s += ' '
        if d:
            s += '\033[31m*'
        else:
            s += ' '
        s += '\033[0m]'
        print(s, end='')

if __name__ == '__main__':
    kitchen_timer_states = [
        {
            'name' : 's0',
            'entry' : 'set_leds(0,0,0,0)'
        },
        {
            'name' : 's1',
            'entry' : 'set_leds(1,0,0,0); start_timer("t", 1000)'
        },
        {
            'name' : 's2',
            'entry' : 'set_leds(1,1,0,0); start_timer("t", 1000)'
        },
        {
            'name' : 's3',
            'entry' : 'set_leds(1,1,1,0); start_timer("t", 1000)'
        },
        {
            'name' : 's4',
            'entry' : 'set_leds(1,1,1,1); start_timer("t", 1000)'
        }
    ]
    initial_transition = [{
            'source' : 'initial',
            'target' : 's0'
    }]
    kitchen_timer_timer_transitions = [
        {
            'trigger':'t',
            'source':'s0',
            'target':'s0'
        },
        {
            'trigger':'t',
            'source':'s1',
            'target':'s0'
        },
        {
            'trigger':'t',
            'source':'s2',
            'target':'s1'
        },
        {
            'trigger':'t',
            'source':'s3',
            'target':'s2'
        },
        {
            'trigger':'t',
            'source':'s4',
            'target':'s3'
        }
    ]
    button_press_transitions = [
        {
            'trigger':'button_pressed',
            'source':'s0',
            'target':'s1'
        },
        {
            'trigger':'button_pressed',
            'source':'s1',
            'target':'s2'
        },
        {
            'trigger':'button_pressed',
            'source':'s2',
            'target':'s3'
        },
        {
            'trigger':'button_pressed',
            'source':'s3',
            'target':'s4'
        },
        {
            'trigger':'button_pressed',
            'source':'s4',
            'target':'s0'
        }

    ]
    kitchen_timer_transitions = initial_transition + kitchen_timer_timer_transitions + button_press_transitions
    driver = Driver()
    kitchen_timer = Machine(name='kitchen_timer', transitions = kitchen_timer_transitions, states=kitchen_timer_states, obj=Kitchen(None))
    driver.add_machine(kitchen_timer)
    Button(driver, Kitchen(kitchen_timer))
    driver.start()
    #driver.send('button_pressed','kitchen_timer')
    driver.wait_until_finished()

