import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sqrt


# ============================================================
# CONFIGURATION
# ============================================================

FIELD_WIDTH = 100
FIELD_HEIGHT = 100

NUM_SENSORS = 80
NUM_SAMPLING_POINTS = 25

COMMUNICATION_RANGE = 35
BAND_ANGLE = 60

RANDOM_SEED = 42


# ============================================================
# CREATE SENSOR NODES
# ============================================================

np.random.seed(RANDOM_SEED)

sensor_x = np.random.uniform(
    0,
    FIELD_WIDTH,
    NUM_SENSORS
)

sensor_y = np.random.uniform(
    0,
    FIELD_HEIGHT,
    NUM_SENSORS
)


# ============================================================
# MOBILE SINK PATH
# ============================================================

sampling_x = np.linspace(
    10,
    90,
    NUM_SAMPLING_POINTS
)

sampling_y = np.linspace(
    10,
    90,
    NUM_SAMPLING_POINTS
)


# ============================================================
# CREATE FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(10, 8)
)

ax.set_xlim(
    0,
    FIELD_WIDTH
)

ax.set_ylim(
    0,
    FIELD_HEIGHT
)

ax.set_xlabel(
    "X Coordinate"
)

ax.set_ylabel(
    "Y Coordinate"
)

ax.set_title(
    "Band-Based Directional Broadcast - Live Simulation",
    fontsize=15,
    fontweight="bold"
)

ax.grid(
    True,
    alpha=0.3
)


# ============================================================
# SENSOR NODES
# ============================================================

sensor_plot = ax.scatter(
    sensor_x,
    sensor_y,
    s=45,
    label="Sensor Nodes"
)


# ============================================================
# SAMPLING PATH
# ============================================================

ax.plot(
    sampling_x,
    sampling_y,
    linestyle="--",
    linewidth=1.5,
    label="Mobile Sink Path"
)


# ============================================================
# MOBILE SINK
# ============================================================

sink_plot = ax.scatter(
    [sampling_x[0]],
    [sampling_y[0]],
    s=180,
    marker="*",
    label="Mobile Sink"
)


# ============================================================
# ACTIVE SENSOR MARKERS
# ============================================================

active_plot = ax.scatter(
    [],
    [],
    s=80,
    marker="o",
    label="Active Sensors"
)


# ============================================================
# DIRECTIONAL LINES
# ============================================================

direction_lines = []


# ============================================================
# TEXT INFORMATION
# ============================================================

info_text = ax.text(
    2,
    96,
    "",
    fontsize=11,
    verticalalignment="top"
)


# ============================================================
# UPDATE FUNCTION
# ============================================================

def update(frame):

    global direction_lines

    # Remove old directional lines
    for line in direction_lines:

        line.remove()

    direction_lines = []

    # Current sink position
    sink_x = sampling_x[frame]
    sink_y = sampling_y[frame]

    # Update sink
    sink_plot.set_offsets(
        [[sink_x, sink_y]]
    )

    active_x = []
    active_y = []

    active_count = 0

    # Determine movement direction
    if frame < NUM_SAMPLING_POINTS - 1:

        next_x = sampling_x[frame + 1]
        next_y = sampling_y[frame + 1]

    else:

        next_x = sink_x
        next_y = sink_y

    direction_x = next_x - sink_x
    direction_y = next_y - sink_y

    magnitude = sqrt(
        direction_x ** 2 +
        direction_y ** 2
    )

    if magnitude > 0:

        direction_x /= magnitude
        direction_y /= magnitude

    # ========================================================
    # CHECK SENSOR NODES
    # ========================================================

    for x, y in zip(
        sensor_x,
        sensor_y
    ):

        dx = sink_x - x
        dy = sink_y - y

        distance = sqrt(
            dx ** 2 +
            dy ** 2
        )

        if distance <= COMMUNICATION_RANGE:

            if distance > 0:

                vector_x = dx / distance
                vector_y = dy / distance

                alignment = (
                    vector_x * direction_x +
                    vector_y * direction_y
                )

            else:

                alignment = 1

            # Directional band
            if alignment >= np.cos(
                np.radians(BAND_ANGLE / 2)
            ):

                active_x.append(x)
                active_y.append(y)

                active_count += 1

                # Draw communication line
                line = ax.plot(
                    [x, sink_x],
                    [y, sink_y],
                    linewidth=0.8,
                    alpha=0.5
                )[0]

                direction_lines.append(
                    line
                )

    # Update active sensors
    if active_x:

        active_plot.set_offsets(
            np.column_stack(
                (active_x, active_y)
            )
        )

    else:

        active_plot.set_offsets(
            np.empty((0, 2))
        )

    # Update information
    info_text.set_text(
        f"Sampling Point: {frame + 1}/{NUM_SAMPLING_POINTS}\n"
        f"Mobile Sink: ({sink_x:.1f}, {sink_y:.1f})\n"
        f"Active Sensors: {active_count}\n"
        f"Communication Range: {COMMUNICATION_RANGE}"
    )

    return (
        sink_plot,
        active_plot,
        info_text
    )


# ============================================================
# ANIMATION
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    frames=NUM_SAMPLING_POINTS,
    interval=700,
    repeat=True
)


# ============================================================
# LEGEND
# ============================================================

ax.legend(
    loc="lower right"
)


plt.tight_layout()

plt.show()