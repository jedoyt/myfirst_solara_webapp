import plotly.express as px
import solara

### OBJECTS FOR IRIS SCATTERPLOT ###
df = px.data.iris()

x_axis = solara.reactive("sepal_length")
y_axis = solara.reactive("sepal_width")
columns = list(df.columns)

click_data = solara.reactive(None)

def find_nearest_neighbours(df, xcol, ycol, x, y, n=10):
    df = df.copy()
    df["distance"] = ((df[xcol] - x)**2 + (df[ycol] - y)**2)**0.5
    return df.sort_values('distance')[1:n+1]
####################################

###### OTHER WEB APP OBJECTS #######
## reactive variable for Button of Button Click Counter ##
clicks = solara.reactive(0)

## reactive variable for Hello World Markdown
txt_color = solara.reactive('red')

@solara.component
def MarkdownWithColor(markdown_text: str):
    # color = solara.use_reactive() # another possibility
    color, set_color = solara.use_state("red") # local state
    solara.Select(label="Color", values=["red", "green", "blue", "orange"],
                  value=color, on_value=set_color)
    solara.Markdown(markdown_text, style={'color': color})
####################################

@solara.component
def Page():
    ### SECTION FOR IRIS SCATTER PLOT ###
    fig = px.scatter(df, x_axis.value, y_axis.value, color="species", custom_data=[df.index])

    if click_data.value is not None:
        x = click_data.value["points"]["xs"][0]
        y = click_data.value["points"]["ys"][0]

        # add an indicator 
        fig.add_trace(px.scatter(x=[x], y=[y], text=["⭐️"]).data[0])
        df_nearest = find_nearest_neighbours(df, x_axis.value, y_axis.value, x, y, n=3)
    else:
        df_nearest = None


    solara.FigurePlotly(fig, on_click=click_data.set)
    solara.Select(label="X-axis", value=x_axis, values=columns)
    solara.Select(label="Y-axis", value=y_axis, values=columns)
    if df_nearest is not None:
        solara.Markdown("## Nearest 3 neighbours")
        solara.DataFrame(df_nearest)
    else:
        solara.Info("Click to select a point")
    #####################################
        
    ##### OTHER WEB APP INTERACTIONS #####
    ### Button Click Counter ###
    btn_color = "green"
    if clicks.value >= 5:
        btn_color = "red"

    def increment():
        clicks.value += 1
        print("clicks", clicks)

    if clicks.value == 0:
        label = "Not clicked yet"
    else:
        label = f"Clicked: {clicks}"
    solara.Button(label=label, on_click=increment, color=btn_color)
    ###########################
    
    ###### Hello World! ######
    solara.Select(label="Color", values=['red', 'green', 'blue', 'orange'], value=txt_color)
    solara.Markdown("## Hello World!", style={'color': txt_color.value})
    ###########################

    with solara.Columns():
        MarkdownWithColor("## Re-use is simple")
        MarkdownWithColor("## With solara")
    ####################################