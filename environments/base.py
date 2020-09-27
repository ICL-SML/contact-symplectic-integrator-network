import numpy as np


class Environment:
    """
    Environment Base Class
    ----------------------

    Environment objects contain all the information required to simulate a system.
    This includes the methods to generate data as well as all paramteres needed in the system.
    
    """

    def __init__(self, DATA, CONTACT, steps=500, dt=0.01, horizon=10, SIGMA=0., SEED=0, epochs=3000):
        self.dt = dt
        self.steps = steps
        self.horizon = horizon
        self.SIGMA = SIGMA
        self.SEED = SEED
        self.epochs = epochs
        self.DATA = DATA
        self.CONTACT = CONTACT
        self.trajectory = None

    def get_filename(self, name, suffix='pdf', folder='images'):
        if folder is None:
            folder = '.'
        return '{}/{}-{}-{}-{}-{}.{}'.format(folder, self.SEED, self.DATA, self.CONTACT, self.epochs, name, suffix)

    def generate(self):
        raise NotImplementedError('Please implement this method.')

    def plot(self):
        raise NotImplementedError('Please implement this method.')
    
    def prepare_output(self):
        X = []
        y = []
        c = []
        np.random.seed(self.SEED)
        nt_ps = self.trajectory[:, :-1] + np.random.normal(0, self.SIGMA, [self.trajectory.shape[0], self.trajectory.shape[1]-1])
        nt = np.hstack([nt_ps, self.trajectory[:, -1:]])
        for i in range(nt.shape[0] - self.horizon - 1):
            X.append(nt[i:i + 1, :-1].flatten())
            y.append(nt[i + 1:i + self.horizon + 1, :-1].flatten())
            c.append(nt[i + 1:i+ self.horizon + 1, -1:].flatten())
        self.X, self.y, self.c = np.array(X), np.array(y), np.array(c)
        return self.X, self.y, self.c
