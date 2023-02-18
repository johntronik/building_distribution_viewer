import streamlit as st
import numpy as np
import pandas as pd
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import japanize_matplotlib
from PIL import Image

st.set_page_config(layout="wide")


df = pd.read_csv("./data/df.csv")


@st.cache_data
def plot_chart(city: str):
    N = 40
    bottom = 1
    width = (2 * np.pi) / N
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    fig, ax = plt.subplots(1, 1, figsize=(3, 3), subplot_kw={"projection": "polar"})

    # prepare data
    radii = np.array(
        [float(t) for t in df.query("name==@city")["radii"].values[0][1:-1].split(",")]
    )
    # plot
    ax.set_title(city)
    bars = ax.bar(theta, radii, width=width, bottom=bottom)

    # x-labels setting
    ax.set_xlim([-np.pi, np.pi])
    ax.set_xticks(np.linspace(-np.pi, np.pi, 9)[1:])
    ax.set_xticklabels(
        [
            "SW",
            "W",
            "NW",
            "N",
            "NE",
            "E",
            "SE",
            "S",
        ]
    )
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")

    # y-label setting
    ax.set_yticklabels([])

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.jet(r / 10))
        bar.set_alpha(0.8)
    return fig


st.markdown('緑のアイコンをクリックすると、区の建物の"エントロピー"を計算して表示します')

left, right = st.columns([2, 1])
with left:
    m = folium.Map(
        location=[35.658581, 139.745433],
        zoom_start=13,
        tiles="cartodbpositron",
    )
    Draw(export=True).add_to(m)
    fg = folium.FeatureGroup(name="23ku")
    DATA_URL = "https://raw.githubusercontent.com/niiyz/JapanCityGeoJson/master/geojson/custom/tokyo23.json"
    folium.Choropleth(
        geo_data=DATA_URL,
        data=df,
        columns=["code", "entropy"],
        key_on="properties.N03_007",
        fill_opacity=0.4,
        line_opacity=0.7,
        line_color="black",
        fill_color="OrRd",
        legend_name="建物のエントロピー",
    ).add_to(m)

    for row in df.itertuples():
        fg.add_child(
            folium.Marker(
                location=[row.lat, row.lon],
                tooltip=f"{row.name}",
                icon=folium.Icon(color="green"),
            )
        )

    map_output = st_folium(
        m,
        feature_group_to_add=fg,
        returned_objects="last_object_clicked_tooltip",
        width=1200,
        height=800,
    )

with right:
    city = map_output["last_object_clicked_tooltip"] or "東京都港区"
    st.pyplot(plot_chart(city))


s = """---
## これなに?
ref: [PLATEAUから街の構造を見る](https://www.estie.jp/blog/entry/2022/08/10/110801)

Geoff Boeingさんの研究に[”Urban spatial order: street network orientation, configuration, and entropy”](https://appliednetsci.springeropen.com/articles/10.1007/s41109-019-0189-1)というものがあります。
これは、道路の方角や長さを街ごとに集計することで、その街の特性がわかるという研究です。

### 集計方法
#### 1. PLATEAUのbuildingデータを読み込む
- 具体的には、東京都データのうち bldg のlod0RoofEdgeのデータ(上空から見た建物の形)を読み込みます。
#### 2. ビルを単純化する
- たとえば、こういうビルがあります。(PLATEAUの建物ID: 13107-bldg-18762)
"""

s1 = """- そのビルを含む四角形に単純化します。"""

s2 = """
- 具体的には、shapelyの minimum_rotated_rectangleを使用しました。

#### 3. 四角形の全ての辺の角度（方角）、長さを計算する
- NumPyでやりました。
#### 4. 方角をヒストグラムで集計する
- この時、辺の長さで重み付けしました。大きい建物は、街の印象に対する影響が大きいと思ったためです。
- NumPyでやりました。

"""
st.markdown(s)
st.image(Image.open("data/raw.png"), width=100)
st.markdown(s1)
st.image(Image.open("data/mrr.png"), width=100)
st.markdown(s2)
