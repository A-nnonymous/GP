import folium
from folium.plugins import HeatMap

"""
    Create a Heatmap layer

    Parameters
    ----------
    data : list of points of the form [lat, lng] or [lat, lng, weight]
        The points you want to plot.
        You can also provide a numpy.array of shape (n,2) or (n,3).
    name : string, default None
        The name of the Layer, as it will appear in LayerControls.
    min_opacity  : default 1.
        The minimum opacity the heat will start at.
    max_zoom : default 18
        Zoom level where the points reach maximum intensity (as intensity
        scales with zoom), equals maxZoom of the map by default
    radius : int, default 25
        Radius of each "point" of the heatmap
    blur : int, default 15
        Amount of blur
    gradient : dict, default None
        Color gradient config. e.g. {0.4: 'blue', 0.65: 'lime', 1: 'red'}
    overlay : bool, default True
        Adds the layer as an optional overlay (True) or the base layer (False).
    control : bool, default True
        Whether the Layer will be included in LayerControls.
    show: bool, default True
        Whether the layer will be shown on opening (only for overlays).
    """
folium.map