"""A module for interactive toolbars with ipywidgets.
Source: Dr. Qiusheng Wu -- https://github.com/giswqs/geodemo/blob/master/geodemo/toolbar.py
"""

import os
import ipywidgets as widgets
import ipyleaflet
from ipyleaflet import WidgetControl
from ipyfilechooser import FileChooser
from IPython.display import display
from .dataprocess import unique_sorted_values_plus_ALL

def change_basemap(m):
    """Widget for change basemaps. Source: Dr. Qiusheng Wu -- https://github.com/giswqs/geemap/blob/master/geemap/toolbar.py
    Args:
        m (object): hagerstrand.Map()
    """
    from .basemaps import _ee_basemaps

    dropdown = widgets.Dropdown(
        options=list(_ee_basemaps.keys()),
        value="ROADMAP",
        layout=widgets.Layout(width="200px"),
        description="Basemaps",
    )

    close_btn = widgets.Button(
        icon="times",
        tooltip="Close the basemap widget",
        button_style="primary",
        layout=widgets.Layout(width="32px"),
    )

    basemap_widget = widgets.HBox([dropdown, close_btn])

    def on_click(change):
        basemap_name = change["new"]

        if len(m.layers) == 1:
            old_basemap = m.layers[0]
        else:
            old_basemap = m.layers[1]
        m.substitute_layer(old_basemap, _ee_basemaps[basemap_name])

    dropdown.observe(on_click, "value")

    def close_click(change):
        m.toolbar_reset()
        if m.basemap_ctrl is not None and m.basemap_ctrl in m.controls:
            m.remove_control(m.basemap_ctrl)
        basemap_widget.close()

    close_btn.on_click(close_click)

    basemap_control = WidgetControl(widget=basemap_widget, position="topright")
    m.add_control(basemap_control)
    m.basemap_ctrl = basemap_control


def filter_df_widget(df, field):
    """Widget for filtering a DataFrame

    Args:
        df (pd.DataFrame): A DataFrame to filter
        field (str): A field within the DataFrame for the filter criterion
    """
    
    dropdown_field = widgets.Dropdown(
        options = unique_sorted_values_plus_ALL(df[field]),
        value="ALL",
        layout=widgets.Layout(width="200px"),
        description=field
    )

    close_dropdown_field = widgets.Button(
        icon="times",
        tooltip="Close the filter widget",
        button_style="primary",
        layout=widgets.Layout(width="32px")
    )

    filter_widget = widgets.HBox([dropdown_field, close_dropdown_field])

    out_field = widgets.Output()

    def on_click_dropdown(change):
        with out_field:
            out_field.clear_output()
            if (change.new == 'ALL'):
                display(df)
            else:
                display(df[df[field] == change.new])

    dropdown_field.observe(on_click_dropdown, names="value")

    def close_click_dropdown(change):
        filter_widget.close()
    
    close_dropdown_field.on_click(close_click_dropdown)
    
    display(filter_widget)
    display(out_field)


def main_toolbar(m):

    padding = "0px 0px 0px 5px"  # upper, right, bottom, left

    toolbar_button = widgets.ToggleButton(
        value=False,
        tooltip="Toolbar",
        icon="wrench",
        layout=widgets.Layout(width="28px", height="28px", padding=padding),
    )

    close_button = widgets.ToggleButton(
        value=False,
        tooltip="Close the tool",
        icon="times",
        button_style="primary",
        layout=widgets.Layout(height="28px", width="28px", padding=padding),
    )    

    toolbar = widgets.HBox([toolbar_button])

    def close_click(change):
        if change["new"]:
            toolbar_button.close()
            close_button.close()
            toolbar.close()
            
    close_button.observe(close_click, "value")

    rows = 2
    cols = 2
    grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="62px"))

    icons = ["folder-open", "map", "gears", "filter"]

    for i in range(rows):
        for j in range(cols):
            grid[i, j] = widgets.Button(description="", button_style="primary", icon=icons[i*rows+j], 
                                        layout=widgets.Layout(width="28px", padding="0px"))

    toolbar = widgets.VBox([toolbar_button])

    def toolbar_click(change):
        if change["new"]:
            toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
        else:
            toolbar.children = [toolbar_button]
        
    toolbar_button.observe(toolbar_click, "value")

    toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")

    m.add_control(toolbar_ctrl)

    output = widgets.Output()
    output_ctrl = WidgetControl(widget=output, position="topright")

    buttons = widgets.ToggleButtons(
        value=None,
        options=["Apply", "Reset", "Close"],
        tooltips=["Apply", "Reset", "Close"],
        button_style="primary",
    )
    buttons.style.button_width = "80px"

    data_dir = os.path.abspath('./data')

    # File Chooser Widget
    fc = FileChooser(data_dir)
    fc.use_dir_icons = True
    fc.filter_pattern = ['*.shp', '*.geojson', '*.json']

    filechooser_widget = widgets.VBox([fc, buttons])

    def button_click(change):
        if change["new"] == "Apply" and fc.selected is not None:
            if fc.selected.endswith(".shp"):
                m.add_shapefile(fc.selected, layer_name="Shapefile")
            elif fc.selected.endswith(".geojson"):
                m.add_geojson(fc.selected, layer_name="GeoJSON")
            elif fc.selected.endswith(".json"):
                m.add_geojson(fc.selected, layer_name="GeoJSON")
        elif change["new"] == "Reset":
            fc.reset()
        elif change["new"] == "Close":
            fc.reset()
            m.remove_control(output_ctrl)
    buttons.observe(button_click, "value")     

    # Basemap Widget
    from .basemaps import _ee_basemaps

    dropdown_basemap = widgets.Dropdown(
        options=list(_ee_basemaps.keys()),
        value="ROADMAP",
        layout=widgets.Layout(width="200px"),
        description="Basemaps",
    )

    close_button_basemap = widgets.Button(
        icon="times",
        tooltip="Close the basemap widget",
        button_style="primary",
        layout=widgets.Layout(width="32px"),
    )

    basemap_widget = widgets.HBox([dropdown_basemap, close_button_basemap])

    def on_click(change):
        basemap_name = change["new"]

        if len(m.layers) == 1:
            old_basemap = m.layers[0]
        else:
            old_basemap = m.layers[1]
        m.substitute_layer(old_basemap, _ee_basemaps[basemap_name])

    dropdown_basemap.observe(on_click, "value")

    def close_click(change):
        if m.basemap_ctrl is not None and m.basemap_ctrl in m.controls:
            m.remove_control(m.basemap_ctrl)
        basemap_widget.close()

    close_button_basemap.on_click(close_click)

    basemap_control = WidgetControl(widget=basemap_widget, position="topright")
    m.basemap_ctrl = basemap_control

    # Select Layer for Filtering Widget
    layers = [layer.name for layer in m.layers if not isinstance(layer, ipyleaflet.TileLayer)]

    dropdown_layer = widgets.Dropdown(
        options=layers,
        description='Layer:'
    )

    dropdown_layer_field = widgets.Dropdown(
        description='Field:'
    )

    dropdown_layer_field_value = widgets.Dropdown(
        description='Value:'
    )

    out_filter_layer = widgets.Output()

    def on_click_layer(change):
        with out_filter_layer:
            out_filter_layer.clear_output()
            dropdown_layer_field.options = list(m.find_layer(change.new).data['features'][0]['properties'].keys())

    dropdown_layer.observe(on_click_layer, names="value")

    out_filter_layer_field = widgets.Output()

    def on_click_layer_field(change):
        with out_filter_layer_field:
            out_filter_layer_field.clear_output()
            field_values = set()
            for record in m.find_layer(dropdown_layer.value).data['features']:
                field_values.add(record['properties'][dropdown_layer_field.value])
            dropdown_layer_field_value.options = sorted(field_values)

    dropdown_layer_field.observe(on_click_layer_field, names="value")


    add_filter_layer = widgets.Button(
         icon="plus",
         tooltip="Add a layer based on the filter options",
         button_color="lightgreen",
         layout=widgets.Layout(width="32px")
    )

    out_click_add_filter_layer = widgets.Output()

    def click_add_filter_layer(change):
            
        import itertools
        import copy

        data = copy.deepcopy(m.find_layer(dropdown_layer.value).data)
        filter_data = [record for record in data['features'] if record['properties'][dropdown_layer_field.value] == dropdown_layer_field_value.value]
        data['features'] = filter_data

        style = {
            "stroke": True,
            "color": "#000000",
            "weight": 2,
            "opacity": 1,
            "fill": True,
            "fillColor": "#0000ff",
            "fillOpacity": 0.4,
        }

        geojson = ipyleaflet.GeoJSON(
            data=data,
            style=style,
            name="{} - {} - {} Layer".format(
                dropdown_layer.value,
                dropdown_layer_field.value,
                dropdown_layer_field_value.value
            )
        )

        m.add_layer(geojson)

    add_filter_layer.on_click(click_add_filter_layer)

    close_dropdown_layer = widgets.Button(
         icon="times",
         tooltip="Close the filter widget",
         button_style="primary",
         layout=widgets.Layout(width="32px")
    )

    box_layout = widgets.Layout(display='flex',
                                flex_flow='row',
                                align_items='stretch',
                                width='70%')

    filter_buttons_box = widgets.Box([close_dropdown_layer, add_filter_layer])
    filter_dropdown_box = widgets.Box([dropdown_layer, dropdown_layer_field, dropdown_layer_field_value])
    filter_widget = widgets.HBox([filter_dropdown_box, filter_buttons_box])

    def close_click_dropdown(change):
        filter_widget.close()
    
    close_dropdown_layer.on_click(close_click_dropdown)
    
    filter_layer_control = WidgetControl(widget=filter_widget, position="bottomright")
    m.filter_layer_ctrl = filter_layer_control

    def tool_click(b):    
        with output:
            output.clear_output()
            if b.icon == "folder-open":
                display(filechooser_widget)
                m.add_control(output_ctrl)

            elif b.icon == "filter":
                dropdown_layer.options = [layer.name for layer in m.layers if not isinstance(layer, ipyleaflet.TileLayer)]
 #               display(layers)
                display(filter_widget)
                m.add_control(filter_layer_control)

            elif b.icon == "map":
                display(basemap_widget)
                m.add_control(basemap_control)

            elif b.icon == "gears":
                import whiteboxgui.whiteboxgui as wbt

                if hasattr(m, "whitebox") and m.whitebox is not None:
                    if m.whitebox in m.controls:
                        m.remove_control(m.whitebox)

                tools_dict = wbt.get_wbt_dict()
                wbt_toolbox = wbt.build_toolbox(
                    tools_dict, max_width="800px", max_height="500px"
                )

                wbt_control = WidgetControl(
                    widget=wbt_toolbox, position="bottomright"
                )                

                m.whitebox = wbt_control
                m.add_control(wbt_control)

#            elif b.icon == "question":

            print(f"You clicked the {b.icon} button")



    for i in range(rows):
        for j in range(cols):
            tool = grid[i, j]
            tool.on_click(tool_click)