import matplotlib.pyplot as plt
def savePlot(ll):
    fig, ax = plt.subplots(nrows=1, ncols=1)  # create figure & 1 axis
    ax.bar([str(x) for x in range(10)], ll, color="#ff660d")
    plt.xlabel('Digits')
    plt.ylabel('Confidence in %')
    plt.title('Confidence Plot for the prediction')

    fig.patch.set_facecolor((240 / 255, 240 / 255, 240 / 255))
    ax.set_facecolor((240 / 255, 240 / 255, 240 / 255))
    plt.ylim(0, 100)
    xlocs = [i for i in range(10)]
    for i, v in enumerate(ll):
        if int(v) != 0:
            plt.text(xlocs[i] - 0.20, v + 0.3, str(v) + "%")
    plt.show()

savePlot([0,0,100,0,0,0,0,0,0,0])