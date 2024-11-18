import numpy as np
import matplotlib as mpl

mpl.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider


def draw_board_features(Board):

    fig = plt.figure()

    color_dicts = {
        "H": ["black", "white"],
        "PP": ["lightgreen","green", "darkgreen"],
        "D": ["lightblue", "blue", "royalblue", "darkblue"],
        "VS": ["red", "white"]
    }
    label_dict = {
        "H": "Household Income (H)",
        "PP": "Property Price (PP)",
        "D": "Desirability (D)",
        "VS": "Vacancy Status (VS)"
    }
    []

    axes = []
    imgs = []
    for i, feature in enumerate(["H", "PP", "D", "VS"]):
        axes.append(fig.add_subplot(2, 2, i + 1))
        subplot_title = label_dict[feature]
        axes[-1].set_title(subplot_title)
        img=draw_board_feature(board = Board, feature = feature, color_dict = color_dicts[feature])
        imgs.append(img)

        

    fig.suptitle('State Variables at t = 0')    
        
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.1)

    axframe = plt.axes([0.25, 0.01, 0.65, 0.03])
    print(len(Board.history))
    sframe = Slider(axframe, 'Time', 0, len(Board.history)-1, valinit=0,valstep =1, valfmt='%d')

    def update(val):
        index = int(round(np.floor(sframe.val)))

        for i, feature in enumerate(["H", "PP", "D", "VS"]):
            print(axes[i])
            draw_board_feature(board = Board, feature = feature, color_dict = color_dicts[feature], history_index=index, subplot=imgs[i] )
        fig.suptitle(f'State Variables at t = {index}')

        plt.draw()

        
        

    sframe.on_changed(update)

    plt.show(block=True)

    return sframe

def draw_board_feature(board, feature, heatmap = False, color_dict=[], bounds = None, show=False, history_index = 0, subplot=None):
    legend_dict = {
        "H": ["Low Income", "High Income"],
        "PP": ["Low Price", "Medium Price", "High Price"],
        "D": "Desirability (0-3)",
        "VS": "Vacancy Status (0.0 - 1.0)"
    }
    img = None
    if feature in ["D", "VS"]:
        custom_cmap = mpl.colors.LinearSegmentedColormap.from_list(feature, color_dict)
        norm = mpl.colors.Normalize(vmin=0, vmax=len(color_dict) - 1)

        if(subplot is None):
            img = plt.imshow(board.get_cells_feature(feature), cmap=custom_cmap, interpolation='nearest', norm = norm)
        else:
            subplot.set_data(board.get_cells_feature(feature, history_index))

        if subplot is None:
            colorbar = plt.colorbar(img)
            colorbar.set_label(legend_dict[feature])
    else:
        custom_cmap = mpl.colors.ListedColormap(color_dict)
        if(subplot is None):
            img = plt.imshow(board.get_cells_feature(feature, history_index), cmap=custom_cmap, interpolation='nearest')
        else:
            subplot.set_data(board.get_cells_feature(feature, history_index))

        if subplot is None:
            legend = [mpl.patches.Patch(color=color, label=label) for color, label in zip(color_dict, legend_dict[feature])]
            plt.legend(handles=legend, loc='center right', bbox_to_anchor = (1.85, 0.5), fontsize='small')

    if(show):
        plt.title('Gentrification Board')
        plt.show()

    return img

def draw_stacked_bar(board):
    
    h = board.get_cells_feature("H").flatten()
    pp = board.get_cells_feature("PP").flatten()
    d = board.get_cells_feature("D").flatten()

    x_labels = [f"{i}" for i in range(len(h))]
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x_labels, h, label="Household Income (H)", color='lightgreen')
    ax.bar(x_labels, pp, bottom=h, label="Property Price (PP)", color='lightblue')
    ax.bar(x_labels, d, bottom=h + pp, label="Desirability (D)", color='lightcoral')

    ax.set_xlabel("Cells")
    ax.set_ylabel("Values")
    ax.set_title("Stacked Bar Chart of Board Features")
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.xticks(rotation=90, fontsize = 6)
    plt.tight_layout()
    plt.show()






