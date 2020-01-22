import matplotlib.pyplot as plt
import sys

# def makeDict(clouds):
#     dict = {}
#     for i in range(len(clouds)):
#        line = clouds[i].split()
#        dict[int(line[0])] = [float(line[1]), float(line[2])]
#     return dict


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: plot.py <measurement>")
        exit()

    measurement = sys.argv[1]

    t = []
    dhi = []
    dni = []
    if measurement in ['humidity', 'temp', 'angle']:
        f = open("results/" + measurement + ".txt", "r")
        for line in f:
            t.append(int(line.split()[0]))
            dhi.append(float(line.split()[1]))
            dni.append(float(line.split()[2]))
    elif measurement == 'clouds':
        f = open("results/" + measurement + ".txt", "r")
        for line in f:
            t.append(line.split()[0])
            dhi.append(float(line.split()[2]))
            dni.append(float(line.split()[3]))
    else:
        print("unknown")
        exit()

    fig, ax = plt.subplots()
    if measurement in ['clouds', 'temp']:
        ax.plot(t, dhi, label="dhi", marker='o', color='#2ca02c')
        ax.plot(t, dni, label="dni", marker='o', color='#d62728')
    else:
        ax.plot(t, dhi, label="dhi")
        ax.plot(t, dni, label="dni")
    ax.legend()
    plt.show()
