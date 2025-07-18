import dash_leaflet as dl
import dash_mantine_components as dmc
from dash import dcc, html
from rio_tiler.colormap import ColorMaps

# Default settings
DEFAULT_CENTER = [0, 0]
DEFAULT_ZOOM = 2
AVAILABLE_COLORMAPS = ColorMaps().list()
DEFAULT_COLORMAP = "blues_r"
VARIABLES = ["SIC Mean"]

# Blues_r for colourbar which uses different input to titiler's approach to colour:
blues_r = [
    "#f7fbff",
    "#deebf7",
    "#c6dbef",
    "#9ecae1",
    "#6baed6",
    "#4292c6",
    "#2171b5",
    "#08519c",
    "#08306b",
]
blues_r.reverse()

leaflet_map = html.Div(
    # style={'width': 'inherit', 'height': 'inherit'},
    style={"width": "inherit", "height": "inherit", "position": "relative"},
    children=[
        dl.Map(
            [
                dl.TileLayer(
                    id="map-base-layer",
                    attribution=("© OpenStreetMap contributors"),
                    zIndex=0,
                ),
                dl.LayersControl([], id="cog-results-layer"),
                dl.Colorbar(
                    id="cbar",
                    width=30,
                    height=200,
                    style={"opacity": "1.0",
                        "backgroundColor": "rgba(255, 255, 255, 0.8)",
                        "padding": "10px",
                        "border-radius": "10px",
                        },
                    position="topleft",
                    tooltip=True,
                    colorscale=blues_r,
                ),
                dl.ScaleControl(position="bottomright"),
                dl.FullScreenControl(position="bottomleft"),
            ],
            crs="EPSG3857",
            attributionControl=True,
            style={"width": "inherit", "height": "inherit"},
            center=DEFAULT_CENTER,
            zoom=DEFAULT_ZOOM,
            id="map",
        ),
        # Controls for map manipulation
        html.Div(
            [
                html.Label("Select Forecast Start:"),
                dmc.DatePickerInput(
                    id="forecast-init-date-picker",
                    value=None,
                    popoverProps={"zIndex": 10000},
                ),
                html.Label("Select Variable:"),
                dcc.Dropdown(
                    id="variable-dropdown",
                    options=[{"label": var, "value": var} for var in VARIABLES],
                    value=VARIABLES[0],
                    clearable=False,
                ),
                html.Label("Select Colormap:"),
                dcc.Dropdown(
                    id="colormap-dropdown",
                    options=[
                        {"label": col, "value": col} for col in AVAILABLE_COLORMAPS
                    ],
                    value=DEFAULT_COLORMAP,
                    clearable=False,
                ),
                html.Label("Opacity Control:"),
                dcc.Slider(
                    id="opacity-slider",
                    min=0.0,
                    max=1.0,
                    # step=0.1,
                    value=1.0,
                    updatemode="drag",
                    persistence="True",
                    persistence_type="memory",
                    # marks={0: '0', 0.2: '0.2', 0.4: '0.4', 0.6: '0.6', 0.8: '0.8', 1: '1'},
                ),
            ],
            style={
                "position": "absolute",
                "top": "20%",
                "right": "20px",
                "background": "rgba(255, 255, 255, 0.8)",
                "padding": "10px",
                "borderRadius": "10px",
                "boxShadow": "0 6px 8px rgba(0, 0, 0, 0.1)",
                "width": "250px",
                "zIndex": 1000,  # Ensure controls are on top of the map
            },
        ),
        dcc.Store(id="forecast-dates-store", data=None),
    ],
)
