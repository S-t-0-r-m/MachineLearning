import matplotlib.pyplot as plt
import numpy as np
def print_normalised_plot(self, name, dependent_feature):

    f, ax = plt.subplots(1)

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)

    slope = self.feature_dict[name].get_parameter()
    intercept = self.feature_dict[dependent_feature].get_parameter()

    print(f"Intercept: {round(intercept, 4)}")
    print(f"slope: {round(slope, 4)}")

    x = np.linspace(-1, 1)
    y = slope * x + intercept
    ax.plot(x, y, "r")

    ax.scatter(
        self.y_feature.get_normalised_series(),
        self.x_feature_dict[name].get_normalised_series(),
    )

    plt.show()
