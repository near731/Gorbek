# Imports

import numpy as np
import plotly.express as px
import pandas as pd

# reading csv

df = pd.read_csv(
    "mh_autotune-main/resources/trajectories/spiral.csv")
df


# Dataframe
fig = px.line_3d(df, x='p_x', y='p_y', z='p_z')
fig.show()

# Velocity

df["v_x"] = (df["p_x"]-df["p_x"].shift(1))/(df["t"]-df["t"].shift(1))
df["v_y"] = (df["p_y"]-df["p_y"].shift(1))/(df["t"]-df["t"].shift(1))
df["v_z"] = (df["p_z"]-df["p_z"].shift(1))/(df["t"]-df["t"].shift(1))
df["v_abs"] = np.sqrt(df["v_x"].values**2 +
                      df["v_y"].values**2+df["v_z"].values**2)
df


fig = px.scatter_3d(df.iloc[1:, :], x='p_x', y='p_y', z='p_z', color="v_abs")
fig.show()

fig = px.scatter(df.iloc[1:, :], x='v_x', y='v_x')
fig.show()

# Accelaration

df["a_x"] = (df["v_x"]-df["v_x"].shift(1))/(df["t"]-df["t"].shift(1))
df["a_y"] = (df["v_y"]-df["v_y"].shift(1))/(df["t"]-df["t"].shift(1))
df["a_z"] = (df["v_z"]-df["v_z"].shift(1))/(df["t"]-df["t"].shift(1))
df["a_abs"] = np.sqrt(df["a_x"].values**2 +
                      df["a_y"].values**2+df["a_z"].values**2)
df


fig = px.scatter_3d(df.iloc[1:, :], x='p_x', y='p_y', z='p_z', color="a_abs")
fig.show()

fig = px.scatter(df.iloc[1:, :], x='a_x', y='a_x')
fig.show()

# Torsion

df["da_x"] = (df["a_x"]-df["a_x"].shift(1))/(df["t"]-df["t"].shift(1))
df["da_y"] = (df["a_y"]-df["a_y"].shift(1))/(df["t"]-df["t"].shift(1))
df["da_z"] = (df["a_z"]-df["a_z"].shift(1))/(df["t"]-df["t"].shift(1))

da = df["da_x"], df["da_y"], df["da_z"]
p = df["p_x"], df["p_y"], df["p_z"]
v = df["v_x"], df["v_y"], df["v_z"]
a = df["a_x"], df["a_y"], df["a_z"]

df["tv"] = (df["v_x"]*df["a_x"]*df["da_x"]+df["v_y"]*df["a_y"]
            * df["da_y"]+df["v_z"]*df["a_z"]*df["da_z"])

df["th_x"] = (df["v_y"].values*df["a_z"].values -
              df["v_z"].values*df["a_y"].values)
df["th_y"] = (df["v_z"].values*df["a_x"].values -
              df["v_x"].values*df["a_z"].values)
df["th_z"] = (df["v_x"].values*df["a_y"].values -
              df["v_y"].values*df["a_x"].values)

df["th_abs"] = np.sqrt(df["th_x"].values**2 +
                       df["th_y"].values**2+df["th_z"].values**2)

df["t"] = df["tv"]/df["th_abs"]

fig = px.scatter_3d(df.iloc[1:, :], x='p_x', y='p_y', z='p_z', color="t")
fig.show()


def kisero_trieder(df=df, pont=100):

    print("\n", pont, "-es ponthoz tartozó kisérő triéder paraméterek:")

    # Érintő

    t_x = df["v_x"].values[pont]/df["v_abs"].values[pont]
    t_y = df["v_y"].values[pont]/df["v_abs"].values[pont]
    t_z = df["v_z"].values[pont]/df["v_abs"].values[pont]
    t = np.sqrt(t_x**2+t_y**2+t_z**2)

    print("\nÉrintő")

    print("\nt_x[", pont, "]=", t_x)
    print("\nt_y[", pont, "]=", t_y)
    print("\nt_z[", pont, "]=", t_z)

    #print("\nHossz=", t)

    # Főnormális

    n_x = df["a_x"].values[pont]/df["a_abs"].values[pont]
    n_y = df["a_y"].values[pont]/df["a_abs"].values[pont]
    n_z = df["a_z"].values[pont]/df["a_abs"].values[pont]
    n = np.sqrt(n_x**2+n_y**2+n_z**2)

    print("\nFőnormális")

    print("\nn_x[", pont, "]=", n_x)
    print("\nn_y[", pont, "]=", n_y)
    print("\nn_z[", pont, "]=", n_z)

    #print("\nHossz=", n)

    # Binormális

    bh_x = df["v_y"].values[pont]*df["a_z"].values[pont] - \
        df["v_z"].values[pont]*df["a_y"].values[pont]
    bh_y = df["v_z"].values[pont]*df["a_x"].values[pont] - \
        df["v_x"].values[pont]*df["a_z"].values[pont]
    bh_z = df["v_x"].values[pont]*df["a_y"].values[pont] - \
        df["v_y"].values[pont]*df["a_x"].values[pont]

    bh = np.sqrt(bh_x**2+bh_y**2+bh_z**2)

    b_x = bh_x/bh
    b_y = bh_y/bh
    b_z = bh_z/bh
    b = np.sqrt(b_x**2+b_y**2+b_z**2)

    print("\nBinormális")

    print("\nb_x[", pont, "]=", b_x)
    print("\nb_y[", pont, "]=", b_y)
    print("\nb_z[", pont, "]=", b_z)

    #print("\nHossz=", b)

    return(t, n, b)


kisero_trieder(df=df, pont=100)
kisero_trieder(df=df, pont=20)
kisero_trieder(df=df, pont=50)


# Németh Áron Imre/D1J5ZG
