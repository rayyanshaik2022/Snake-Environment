from environment import Environment

env = Environment()


def snake_logic(env):
    pass


env.new()
env.set_protocol(snake_logic)
env.run()