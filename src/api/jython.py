from jython_generator import Generator


def generate_jython_client():

    g = Generator("microservice-example", "CS.gui.toast.send")

    g.add_config_example_if_missing()
    g.generate_client()
    g.generate_routes()
    g.generate_tests()
    g.generate_utility()
