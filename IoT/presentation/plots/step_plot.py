import matplotlib.pyplot as plt
import numpy as np
plt.style.use('seaborn-darkgrid')

x = range(8)
y = np.linspace(1.1, 5.0, 8)

ylabel = map(lambda num: bin(num)[2:], x)
xlabel = map(lambda num: "{0:.2f}".format(num), y)

plt.step(x, y)
plt.yticks(y, ylabel)
plt.xticks(x, xlabel, rotation=45)
plt.ylabel("Binary Output")
plt.xlabel("Analog Input")
plt.savefig("adc.png", transparent=True)
