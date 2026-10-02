import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


# ============================================================
# CONFIGURATION
# ============================================================

FIELD_WIDTH = 100
FIELD_HEIGHT = 100

NUM_SENSORS = 120
NUM_SAMPLING_POINTS = 30

INITIAL_ENERGY = 100.0

# Communication parameters
BASE_ENERGY = 0.05
DISTANCE_ENERGY = 0.001

# Directional broadcast parameters
BAND_WIDTH = 25

RANDOM_SEED = 30


# ============================================================
# SENSOR NODE
# ============================================================

class SensorNode:

    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y

        self.initial_energy = INITIAL_ENERGY
        self.energy = INITIAL_ENERGY

        self.data_packets = 0
        self.transmissions = 0
        self.successful_transmissions = 0

    def distance_to(self, x, y):
        return sqrt(
            (self.x - x) ** 2 +
            (self.y - y) ** 2
        )

    def transmit(self, distance):
        """
        Energy consumed for one transmission.
        """
        energy_cost = BASE_ENERGY + DISTANCE_ENERGY * (distance ** 2)

        self.energy -= energy_cost

        if self.energy < 0:
            self.energy = 0

        self.transmissions += 1

        return energy_cost


# ============================================================
# MOBILE SINK
# ============================================================

class MobileSink:

    def __init__(self, field_width, field_height):
        self.width = field_width
        self.height = field_height

        self.path = self.generate_path()

    def generate_path(self):

        """
        Generates a serpentine movement path.
        """

        points = []

        y_values = np.linspace(
            10,
            self.height - 10,
            NUM_SAMPLING_POINTS
        )

        for i, y in enumerate(y_values):

            if i % 2 == 0:
                x = 10
            else:
                x = self.width - 10

            points.append((x, y))

        return points


# ============================================================
# CREATE SENSOR NETWORK
# ============================================================

def create_sensor_network():

    np.random.seed(RANDOM_SEED)

    sensors = []

    for i in range(NUM_SENSORS):

        x = np.random.uniform(
            0,
            FIELD_WIDTH
        )

        y = np.random.uniform(
            0,
            FIELD_HEIGHT
        )

        sensors.append(
            SensorNode(i, x, y)
        )

    return sensors


# ============================================================
# NORMAL BROADCAST
# ============================================================

def normal_broadcast(
    sensors,
    sink
):

    total_energy = 0
    successful_packets = 0
    total_packets = 0

    energy_history = []

    for sink_x, sink_y in sink.path:

        # Sensors close enough to sampling point
        for sensor in sensors:

            distance = sensor.distance_to(
                sink_x,
                sink_y
            )

            # Communication range
            if distance <= 35:

                total_packets += 1

                energy = sensor.transmit(
                    distance
                )

                total_energy += energy

                sensor.data_packets += 1

                successful_packets += 1

        remaining_energy = sum(
            sensor.energy
            for sensor in sensors
        )

        energy_history.append(
            remaining_energy
        )

    delivery_ratio = (
        successful_packets / total_packets * 100
        if total_packets > 0
        else 0
    )

    return (
        total_energy,
        successful_packets,
        total_packets,
        delivery_ratio,
        energy_history
    )


# ============================================================
# BAND-BASED DIRECTIONAL BROADCAST
# ============================================================

def directional_broadcast(
    sensors,
    sink
):

    total_energy = 0
    successful_packets = 0
    total_packets = 0

    energy_history = []

    for index, (sink_x, sink_y) in enumerate(
        sink.path
    ):

        # Determine movement direction
        if index < len(sink.path) - 1:

            next_x, next_y = sink.path[index + 1]

        else:

            next_x, next_y = sink_x, sink_y

        direction_x = next_x - sink_x
        direction_y = next_y - sink_y

        magnitude = sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        if magnitude != 0:

            direction_x /= magnitude
            direction_y /= magnitude

        for sensor in sensors:

            dx = sink_x - sensor.x
            dy = sink_y - sensor.y

            distance = sqrt(
                dx ** 2 +
                dy ** 2
            )

            # Communication range
            if distance > 35:
                continue

            total_packets += 1

            # Normalize sensor -> sink vector
            if distance != 0:

                vector_x = dx / distance
                vector_y = dy / distance

            else:

                vector_x = 0
                vector_y = 0

            # Dot product determines directional alignment
            alignment = (
                vector_x * direction_x +
                vector_y * direction_y
            )

            # Directional band
            if alignment >= 0.35:

                energy = sensor.transmit(
                    distance * 0.75
                )

                total_energy += energy

                successful_packets += 1

            else:

                # Small probability of successful
                # forwarding outside the primary band
                if np.random.random() < 0.25:

                    energy = sensor.transmit(
                        distance
                    )

                    total_energy += energy

                    successful_packets += 1

        remaining_energy = sum(
            sensor.energy
            for sensor in sensors
        )

        energy_history.append(
            remaining_energy
        )

    delivery_ratio = (
        successful_packets / total_packets * 100
        if total_packets > 0
        else 0
    )

    return (
        total_energy,
        successful_packets,
        total_packets,
        delivery_ratio,
        energy_history
    )


# ============================================================
# DRAW SENSOR FIELD
# ============================================================

def plot_sensor_field(
    sensors,
    sink
):

    plt.figure(
        figsize=(10, 8)
    )

    x = [
        sensor.x
        for sensor in sensors
    ]

    y = [
        sensor.y
        for sensor in sensors
    ]

    plt.scatter(
        x,
        y,
        s=35,
        label="Sensor Nodes"
    )

    path_x = [
        point[0]
        for point in sink.path
    ]

    path_y = [
        point[1]
        for point in sink.path
    ]

    plt.plot(
        path_x,
        path_y,
        linewidth=2,
        label="Mobile Sink Path"
    )

    plt.scatter(
        path_x,
        path_y,
        s=60,
        marker="x",
        label="Sampling Points"
    )

    plt.scatter(
        path_x[-1],
        path_y[-1],
        s=150,
        marker="*",
        label="Mobile Sink"
    )

    plt.title(
        "Mobile Sampling Sensor Field"
    )

    plt.xlabel(
        "X Coordinate"
    )

    plt.ylabel(
        "Y Coordinate"
    )

    plt.xlim(
        0,
        FIELD_WIDTH
    )

    plt.ylim(
        0,
        FIELD_HEIGHT
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "network_simulation.png",
        dpi=300
    )

    plt.close()


# ============================================================
# COMPARISON GRAPH
# ============================================================

def plot_energy_comparison(
    normal_energy,
    directional_energy
):

    methods = [
        "Normal\nBroadcast",
        "Band-Based\nDirectional"
    ]

    values = [
        normal_energy,
        directional_energy
    ]

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        methods,
        values
    )

    plt.ylabel(
        "Energy Consumption"
    )

    plt.title(
        "Energy Consumption Comparison"
    )

    for i, value in enumerate(values):

        plt.text(
            i,
            value + 5,
            f"{value:.2f}",
            ha="center"
        )

    plt.tight_layout()

    plt.savefig(
        "energy_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# TRANSMISSION COMPARISON
# ============================================================

def plot_transmissions(
    normal_transmissions,
    directional_transmissions
):

    methods = [
        "Normal\nBroadcast",
        "Band-Based\nDirectional"
    ]

    values = [
        normal_transmissions,
        directional_transmissions
    ]

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        methods,
        values
    )

    plt.ylabel(
        "Number of Transmissions"
    )

    plt.title(
        "Transmission Comparison"
    )

    for i, value in enumerate(values):

        plt.text(
            i,
            value + 50,
            str(value),
            ha="center"
        )

    plt.tight_layout()

    plt.savefig(
        "transmissions_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# DELIVERY RATIO
# ============================================================

def plot_delivery(
    normal_delivery,
    directional_delivery
):

    methods = [
        "Normal\nBroadcast",
        "Band-Based\nDirectional"
    ]

    values = [
        normal_delivery,
        directional_delivery
    ]

    plt.figure(
        figsize=(8, 6)
    )

    plt.bar(
        methods,
        values
    )

    plt.ylabel(
        "Delivery Ratio (%)"
    )

    plt.title(
        "Data Deliverability Comparison"
    )

    plt.ylim(
        0,
        110
    )

    for i, value in enumerate(values):

        plt.text(
            i,
            value + 2,
            f"{value:.2f}%",
            ha="center"
        )

    plt.tight_layout()

    plt.savefig(
        "delivery_comparison.png",
        dpi=300
    )

    plt.close()


# ============================================================
# ENERGY OVER TIME
# ============================================================

def plot_energy_history(
    normal_history,
    directional_history
):

    plt.figure(
        figsize=(10, 6)
    )

    plt.plot(
        normal_history,
        label="Normal Broadcast",
        linewidth=2
    )

    plt.plot(
        directional_history,
        label="Band-Based Directional",
        linewidth=2
    )

    plt.xlabel(
        "Sampling Point"
    )

    plt.ylabel(
        "Remaining Network Energy"
    )

    plt.title(
        "Network Energy Over Sampling Points"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "energy_over_time.png",
        dpi=300
    )

    plt.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)

    print(
        " MOBILE SAMPLING OF SENSOR FIELD DATA"
    )

    print(
        " Band-Based Directional Broadcast Simulation"
    )

    print("=" * 60)

    print()

    print(
        f"Sensors          : {NUM_SENSORS}"
    )

    print(
        f"Sampling Points  : {NUM_SAMPLING_POINTS}"
    )

    print()

    # --------------------------------------------------------
    # Create sensor network
    # --------------------------------------------------------

    sensors_normal = create_sensor_network()

    sensors_directional = create_sensor_network()

    # --------------------------------------------------------
    # Mobile sink
    # --------------------------------------------------------

    sink = MobileSink(
        FIELD_WIDTH,
        FIELD_HEIGHT
    )

    # --------------------------------------------------------
    # Normal broadcast
    # --------------------------------------------------------

    (
        normal_energy,
        normal_success,
        normal_total,
        normal_delivery,
        normal_history
    ) = normal_broadcast(
        sensors_normal,
        sink
    )

    # --------------------------------------------------------
    # Directional broadcast
    # --------------------------------------------------------

    (
        directional_energy,
        directional_success,
        directional_total,
        directional_delivery,
        directional_history
    ) = directional_broadcast(
        sensors_directional,
        sink
    )

    # --------------------------------------------------------
    # Calculate results
    # --------------------------------------------------------

    energy_reduction = (
        (
            normal_energy -
            directional_energy
        )
        /
        normal_energy
    ) * 100

    normal_transmissions = sum(
        sensor.transmissions
        for sensor in sensors_normal
    )

    directional_transmissions = sum(
        sensor.transmissions
        for sensor in sensors_directional
    )

    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print("-" * 60)

    print(
        f"Normal energy consumed   : "
        f"{normal_energy:.2f}"
    )

    print(
        f"Directional energy used  : "
        f"{directional_energy:.2f}"
    )

    print(
        f"Energy reduction         : "
        f"{energy_reduction:.2f}%"
    )

    print()

    print(
        f"Normal transmissions     : "
        f"{normal_transmissions}"
    )

    print(
        f"Directional transmissions: "
        f"{directional_transmissions}"
    )

    print()

    print(
        f"Normal delivery ratio    : "
        f"{normal_delivery:.2f}%"
    )

    print(
        f"Directional delivery     : "
        f"{directional_delivery:.2f}%"
    )

    print("-" * 60)

    # --------------------------------------------------------
    # Generate graphs
    # --------------------------------------------------------

    plot_sensor_field(
        sensors_normal,
        sink
    )

    plot_energy_comparison(
        normal_energy,
        directional_energy
    )

    plot_transmissions(
        normal_transmissions,
        directional_transmissions
    )

    plot_delivery(
        normal_delivery,
        directional_delivery
    )

    plot_energy_history(
        normal_history,
        directional_history
    )

    print()

    print(
        "Simulation completed successfully."
    )

    print(
        "Graphs saved in the project folder."
    )


if __name__ == "__main__":
    main()

