import numpy as np
import plotly.express as px
import pandas as pd

# Akik zip-ből csinálják:
df = pd.read_csv(
    "C:/Users/nemet/Python/mh_autotune-main/resources/trajectories/spiral.csv")

# Plotly beolvasása

# Az egyes tengelyek a dataframe egyes oszlopai
fig = px.line_3d(df, x='p_x', y='p_y', z='p_z')
fig.show()


df["p_x_d"] = (df["p_x"]-df["p_x"].shift(1))/(df["t"]-df["t"].shift(1))
df["p_y_d"] = (df["p_y"]-df["p_y"].shift(1))/(df["t"]-df["t"].shift(1))
df["p_z_d"] = (df["p_z"]-df["p_z"].shift(1))/(df["t"]-df["t"].shift(1))
df["p_v_abs"] = np.sqrt(df["p_x_d"].values**2 +
                        df["p_y_d"].values**2+df["p_z_d"].values**2)
df
