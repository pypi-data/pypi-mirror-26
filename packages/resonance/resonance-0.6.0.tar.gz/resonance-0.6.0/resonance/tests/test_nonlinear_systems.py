import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from ..nonlinear_systems import SingleDoFNonLinearSystem


class SimplePendulum(SingleDoFNonLinearSystem):
    pass

sys = SimplePendulum()

sys.constants['mass'] = 1.0  # kg
sys.constants['length'] = 1.0  # m
sys.constants['acc_due_to_grav'] = 9.81  # m/s**2

sys.coordinates['angle'] = np.deg2rad(15.0)  # rad
sys.speeds['angle_vel'] = 0.0  # rad/s

assert list(sys.states.keys()) == ['angle', 'angle_vel']
assert list(sys.states.values()) == [np.deg2rad(15.0), 0.0]


def equations_of_motion(state, time, length, acc_due_to_grav):

    l = length
    g = acc_due_to_grav

    theta = state[0]
    omega = state[1]

    thetad = omega
    omegad = -g / l * np.sin(theta)

    return [thetad, omegad]

# function that computes the right hand side of the equations of motion in
# first order form
sys.equations_of_motion = equations_of_motion


def height(angle, length):
    """The Y coordinate points in the opposite of gravity, i.e. up. The X
    coordinate points to the right."""
    return -length * np.cos(angle)

sys.add_measurement('height', height)


def sway(angle, length):
    """The X coordinate points to the right."""
    return length * np.sin(angle)

sys.add_measurement('sway', sway)


def potential_energy(length, height, mass, acc_due_to_grav):
    return mass * acc_due_to_grav * (length + height)

sys.add_measurement('potential_energy', potential_energy)


def kinetic_energy(mass, length, angle_vel):
    return mass * (length * angle_vel)**2 / 2.0

sys.add_measurement('kinetic_energy', kinetic_energy)


def total_energy(kinetic_energy, potential_energy):
    return kinetic_energy + potential_energy

sys.add_measurement('total_energy', total_energy)

sample_rate = 30
trajectories = sys.free_response(5.0, sample_rate=sample_rate)


def plot_config(mass, length, sway, height, time, sway__hist, height__hist,
                time__hist, potential_energy__hist):
    fig, axes = plt.subplots(1, 2)

    circle_radius = mass / 2.0 / 10.0

    axes[0].set_xlim((-length - circle_radius, length + circle_radius))
    axes[0].set_ylim((-length - circle_radius, length + circle_radius))
    axes[0].set_title('Pendulum')
    axes[0].set_aspect('equal')
    xlabel = axes[0].set_xlabel('Time: {:.3f}'.format(time))

    path_lines = axes[0].plot(sway__hist, height__hist, color='red')
    rod_lines = axes[0].plot([0, sway], [0, height])

    circle = Circle((sway, height), radius=circle_radius)
    axes[0].add_patch(circle)

    axes[1].set_ylim((0, 0.4))
    axes[1].set_xlim((0, 5))
    axes[1].set_xlabel('Time [s]')
    axes[1].set_ylabel('Potential Energy [J]')
    pe_lines = axes[1].plot(time__hist, potential_energy__hist)

    plt.tight_layout()

    return fig, circle, rod_lines, path_lines, pe_lines, xlabel

sys.config_plot_func = plot_config


def update_plot(sway, height, time, time__hist, sway__hist, height__hist,
                potential_energy__hist, circle, rod_lines, path_lines,
                pe_lines, xlabel):
    circle.center = sway, height
    rod_lines[0].set_data([0, sway], [0, height])
    path_lines[0].set_data(sway__hist, height__hist)
    pe_lines[0].set_data(time__hist, potential_energy__hist)
    xlabel.set_text('Time: {:.3f}'.format(time))

    return circle, rod_lines, path_lines, pe_lines, xlabel

sys.config_plot_update_func = update_plot
