import numpy as np
import matplotlib.pyplot as plt
import pymunk
from environments.base import Environment

class BouncingBall(Environment):
    """
    Bouncing Ball Environment

    Parameters:
    -----------

        steps:      int;
                    number of time steps (default: 500)
        dt:         float;
                    time steps size (default 0.02)
        epochs:     int;
                    number of epochs (default: 3000)
        CONTACT:    str;
                    contact type (default: nomax)
        mass:       float;
                    mass of the ball (default: 1.0)
        g:          float;
                    accelaration constant (default: -9.81)
        height:     float;
                    drop height
        e:          np.array;
                    Newton restitution coefficient
        horizon:    int;
                    prediction time window
        SIGMA:      float;
                    variance of gaussian white noise
        SEED:       int;
                    random seed
    """

    def __init__(
            self, steps=500, dt=0.02, epochs=3000, CONTACT='nomax', mass=1, g=-9.81,
            height=10, e=1., horizon=10, SIGMA=0., SEED=0):
        DATA = 'bouncing_ball' if e == 1. else 'bouncing_ball_zenos_paradox'
        super().__init__(DATA, CONTACT, steps, dt, horizon, SIGMA, SEED, epochs)
        self.e = e
        self.height = height
        self.mass = mass
        self.g = g

    def plot(self):
        """Plot generated data"""
        plt.plot(self.X[:, 0])
        plt.xlabel('steps')
        plt.ylabel('height')
        plt.show()

    def generate(self):
        """Generate data based on parameters set in init function"""
        space = pymunk.Space()
        space.gravity = (0.0, self.g)

        radius = 0.01
        inertia = pymunk.moment_for_circle(self.mass, 0, radius, (0, 0))
        body = pymunk.Body(self.mass, inertia)
        body.position = (0, self.height)
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = self.e
        shape.friction = 0

        space.add(body, shape)
        ball = shape

        static_body = space.static_body
        static_lines = [pymunk.Segment(static_body, (-10, -1), (10, -1), 1)]

        for line in static_lines:
            # line.elasticity = 0.95
            line.friction = 0
            line.elasticity = 1
        space.add(static_lines)

        trajectory = []
        for _ in range(self.steps + 1):
            trajectory.append((ball.body.position[1], ball.body.velocity[1]))
            space.step(self.dt)
        self.trajectory = np.array(trajectory)

        X, y = self.prepare_output()
        self.X = X
        self.y = y

        return trajectory, X, y