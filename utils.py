import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from IPython.display import display, HTML

datasets = None

# Returns all loaded datasets
def getDatasets(datasets_folder):

    pvs = {}
    
    for i in range(1,10):
    
        folder = os.path.join(datasets_folder, "PVS " + str(i))
        data_left = pd.read_csv(os.path.join(folder, 'dataset_gps_mpu_left.csv'), float_precision="high")
        data_right = pd.read_csv(os.path.join(folder, 'dataset_gps_mpu_right.csv'), float_precision="high")
        data_labels = pd.read_csv(os.path.join(folder, 'dataset_labels.csv'))

        pvs["pvs_" + str(i)] = {
            "data_left": data_left,
            "data_right": data_right,
            "data_labels": data_labels
        }

    return pvs

# Shows data classes on a plot
def plotDataClass(pvs, classes):
    
    data_labels = datasets["pvs_" + str(pvs)]["data_labels"]
    plt.figure(figsize=(16,6)) 
    
    for i in range(0, len(classes)):
        classe = classes[i]
        (data_labels[classe] * (i+1)).plot(linewidth=2)

    plt.legend()

# Shows data classes on a map
def createMapDataClass(pvs, classes, colors, zoom_start=14):
    
    dataset = datasets["pvs_" + str(pvs)]
    data = pd.concat([dataset["data_left"], dataset["data_labels"]], axis=1)

    gps = data[['latitude', 'longitude']]
    focolat = (gps['latitude'].min() + gps['latitude'].max()) / 2
    focolon = (gps['longitude'].min() + gps['longitude'].max()) / 2
    maps = folium.Map(location=[focolat, focolon], zoom_start=zoom_start)

    grouper = data.groupby(["latitude","longitude"]).mean().round(0)

    for i in range(0, len(classes)):
    
        classe = classes[i]
        color = colors[i]
        points = grouper[grouper[classe] == 1].index.values.reshape(-1)
        
        for point in points:
            folium.Circle(point, color=color, radius=0.1).add_to(maps)

    return maps.get_root().render().replace('"', '&quot;')
    
# Shows legend for data classes
def createLegendDataClass(classes_names, colors):
    
    html_legend = """
    <style>
        .legend { list-style: none; }
        .legend li { float: left; margin-right: 10px; }
        .legend span { border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; }
    </style>
    <div style="width: 100%; height: 10px;">
    <ul class="legend" style="list-style: none;">
    """
    
    for i in range(0, len(classes_names)):
        name = classes_names[i]
        color = colors[i]
        
        html_legend += """
        <li><span style="background-color: {}"></span> {}</li>
        """.format(color, name)
    
    html_legend += """
    </ul>
    </div>
    <br>
    """
    
    return html_legend
    
# Shows data class maps side by side
def showMapDataClass(pvs, classes, classes_names, colors):
    
    html = createLegendDataClass(classes_names, colors)
    
    html += """
    <div>
    """
    
    if isinstance(pvs, list):
        
        for i in pvs:
            maps = createMapDataClass(i, classes, colors, 13)
            html += """
            <iframe srcdoc="{}" style="float:left; width: {}px; height: {}px; display:inline-block; width:33%; margin: 0 auto; border: 1px solid black"></iframe>
            """.format(maps, 500, 500)
    else:
        maps = createMapDataClass(pvs, classes, colors)
        html += """
            <iframe srcdoc="{}" style="float:left; width: 99%; height: 500px; display:inline-block; margin: 0 auto; border: 1px solid black"></iframe>
            """.format(maps)

    html += "</div>"
    
    display(HTML(html))

# Measure the quantity and distribution metrics of the data classes
def metricsDataClass(classes):
    
    list_data = []
    
    for pvs in range(1,10):
        data = datasets["pvs_" + str(pvs)]
        list_data.append(data["data_labels"][classes].sum())
       
    data = pd.DataFrame(list_data)
    data["Total"] = data.sum(axis=1)
    
    for classe in classes:
        data[classe + "_distribuition_%"] = round(data[classe]/data["Total"] * 100, 2)
        
    data.index = np.arange(1, len(data) + 1)
    data.index = data.index.rename("PVS")
    return data