import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def pca_variance(pca, dataframe):
    
    dimensions = ['Dimension {}'.format(i) for i in range(1,len(pca.components_)+1)]
    components = pd.DataFrame(np.round(pca.components_, 4), columns = dataframe.keys())
    ratios = pca.explained_variance_ratio_.reshape(len(pca.components_), 1)
    variance_ratios = pd.DataFrame(np.round(ratios, 4), columns = ['Explained Variance'])
    variance_ratios.index = dimensions

    fig, ax = plt.subplots(figsize = (14,8))

    # Plot the feature weights as a function of the components
    components.plot(ax = ax, kind = 'bar');
    ax.set_ylabel("Feature Weights")
    ax.set_xticklabels(dimensions, rotation=0)


    # Display the explained variance ratios
    for i, ev in enumerate(pca.explained_variance_ratio_):
        ax.text(i-0.40, ax.get_ylim()[1] + 0.05, "Explained Variance\n          %.4f"%(ev))
        
def pca_cumsum(pca):
    # create an x-axis variable for each pca component
    x = np.arange(1,7)

    # plot the cumulative variance
    plt.plot(x, np.cumsum(pca.explained_variance_ratio_), '-o', color='black')

    # plot the components' variance
    plt.bar(x, pca.explained_variance_ratio_, align='center', alpha=0.5)

    # plot styling
    plt.ylim(0, 1.05)
    plt.annotate('Cumulative\nexplained\nvariance',
                 xy=(3.7, .88), arrowprops=dict(arrowstyle='->'), xytext=(4.5, .6))
    for i,j in zip(x, np.cumsum(pca.explained_variance_ratio_)):
        plt.annotate(str(j.round(4)),xy=(i+.2,j-.02))
    plt.xticks(range(1,7))
    plt.xlabel('PCA components')
    plt.ylabel('Explained Variance')
    plt.show()
