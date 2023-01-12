import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def custom_seaborn(vector_raster=True):
    """
    Custom settings for Seaborn visualizations.
    """
    sns.set_theme(context='paper',
            style='white',
            palette='gray',
            font='sans-serif',
            font_scale=.8,
            color_codes=True,
            rc={'figure.dpi':300, 'savefig.dpi':300, 'figure.figsize':(6,4)})
    if vector_raster is True:
        from IPython.display import set_matplotlib_formats
        set_matplotlib_formats('pdf', 'png')



def format_axes_commas(name_axis_object):
    """
    This function formats the x and y axis tick labels with commas
    as thousand separators.
    """
    name_axis_object.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    name_axis_object.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))


def plot_knn_decision_boundaries(X, y, model, xlabel, ylabel, colors, fontsize=8):
    """
    A utility function to simplify plotting decision boundaries with knn.
    Used primarily for teaching purposes in Chapter 12.
    """
    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

    # Reduces to the first two columns of data
    reduced_data = X[:, :2]

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1

    # Meshgrid creation
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh using the model.
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
    np.arange(y_min, y_max, 0.1))

    # Predictions to obtain the classification results
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

    # Plotting
    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c = colors)
    plt.xlabel(xlabel,fontsize=fontsize)
    plt.ylabel(ylabel,fontsize=fontsize)
    plt.xticks(fontsize=fontsize-1)
    plt.yticks(fontsize=fontsize-1)
    plt.xlim(0,1)
    plt.ylim(0,1)


def draw_ner_blockmodel_sfdp(G, blocks, filename = None):

    try:
        import graph_tool as gt
    except:
        print("Error importing graph-tool. Make sure that it's correctly installed.")

    top_n_G = gt.all.GraphView(G, efilt = G.ep['mask'])
    top_n_G = gt.all.GraphView(top_n_G, vfilt = lambda v: v.out_degree() > 0)
    top_n_blocks = blocks.copy(top_n_G, bs = blocks.get_bs())

    if filename:
        top_n_blocks.draw(
            layout = 'sfdp',
            vertex_text = top_n_G.vp['labels'],
            eorder = top_n_G.ep['weight'],
            vertex_text_position=45,
            bg_color=[255,255,255,1],
            output_size=[1024,1024],
            output = filename
            )
    else:
        top_n_blocks.draw(
            layout = 'sfdp',
            vertex_text = top_n_G.vp['labels'],
            eorder = top_n_G.ep['weight'],
            vertex_text_position=45,
            bg_color=[255,255,255,1],
            )
