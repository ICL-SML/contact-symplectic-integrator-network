"""
Bouncing Ball Experiment
------------------------

This is the setup used as shown in the thesis
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from environments import BouncingBall
from models import CDLNetwork_Simple, ResNet
from utils import TRAIN, PREDICT

env = None
cdl_model = None
resnet = None


def run():
    global env, cdl_model, resnet, cdl_data, resnet_data

    env = BouncingBall(steps=500, dt=0.02, epochs=3000, e=1.)
    env.generate()

    # CD-LAGRANGE
    cdl_model = TRAIN(env, CDLNetwork_Simple, name='CDL')

    # RESNET
    resnet = TRAIN(env, ResNet, name='ResNet')

    cdl_data = PREDICT(env, cdl_model)
    resnet_data = PREDICT(env, resnet)


def plot_trajectory(save_fig=False):
    plt.figure(figsize=(12,8))

    plt.title('Phase Space'); plt.xlabel('q'); plt.ylabel('p')
    plt.plot(cdl_data[:, 0], cdl_data[:, 1], 'x--', label='CD-Lagrange')
    plt.plot(resnet_data[:, 0], resnet_data[:, 1], 'x--', label='ResNet')
    plt.plot(env.trajectory[:, 0], env.trajectory[:, 1], 'xk', label='Ground truth')
    plt.legend()
    if save_fig:
        plt.savefig(env.get_filename('trajectory'))
    plt.show()

def plot_potential(save_fig=False):
    t = np.arange(cdl_data.shape[0]) * env.dt

    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.title('Gradient of Potential')
    plt.plot(t, cdl_model.grad_potential(tf.reshape(cdl_data[:, 0], (cdl_data.shape[0], 1,1)))[:, 0,0], label='CD-Lagrange')
    plt.plot(t, -9.81 * np.ones_like(t), '--k', label='Ground truth')
    plt.legend()
    plt.xlabel('Time in s')
    plt.subplot(1, 2, 2)
    plt.title('Contact function')
    plt.plot(t[1:], cdl_model.contact(tf.concat([cdl_data[1:, 0:1], cdl_data[:-1, 1:2]], 1)), label='CD-Lagrange')

    plt.plot(t[:-1], (env.trajectory[:, 0] <= 0.01), 'kx', label='Ground truth')
    plt.legend()
    plt.xlabel('Time in s')
    if save_fig:
        plt.savefig(env.get_filename('potential'))
    plt.show()