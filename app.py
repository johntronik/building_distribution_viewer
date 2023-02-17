from PIL import Image
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import japanize_matplotlib
import pydeck as pdk



df = pd.read_csv('data/df.csv')

def plot_chart(city:str):
    N = 40
    bottom = 1
    width = (2*np.pi) / N
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    fig, ax = plt.subplots(1,1,figsize=(5,5), subplot_kw={'projection': 'polar'})

    # prepare data
    radii = np.array([float(t) for t in df.query('name==@city')['radii'].values[0][1:-1].split(',')])
    # plot
    ax.set_title(city)
    bars = ax.bar(theta, radii, width=width, bottom=bottom)

    # x-labels setting
    ax.set_xlim([-np.pi, np.pi])
    ax.set_xticks(np.linspace(-np.pi, np.pi, 9)[1:])
    ax.set_xticklabels(["SW", "W", "NW", "N", "NE", "E", "SE", "S",])
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location("N")

    # y-label setting
    ax.set_yticklabels([])

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.jet(r / 10))
        bar.set_alpha(0.8)
    return fig


def plot_map(city:str):
    row = df[df['name']==city]
    code,lat,lon = row[['code', 'lat', 'lon']].values[0]
    DATA_URL = f"https://raw.githubusercontent.com/niiyz/JapanCityGeoJson/master/geojson/13/{int(code)}.json"

    INITIAL_VIEW_STATE = pdk.ViewState(latitude=lat, longitude=lon, zoom=13, max_zoom=16, pitch=45, bearing=0)
    geojson = pdk.Layer(
        "GeoJsonLayer",
        DATA_URL,
        opacity=0.1,
        get_fill_color="[100, 200, 100]",
    )
    return pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE)


st.set_page_config(layout="wide")
st.markdown('## 都市を集計します')

# city = '東京都中央区'
city = st.selectbox('街を選んでください', df['name'])

left,right = st.columns([1,2])
with left:
    st.pyplot(plot_chart(city))
with right:
    st.pydeck_chart(plot_map(city))
    # df_city = df.query('name==@city')[['lon','lat']]
    # st.map(df_city, zoom=14)





s = '''---
## これなに?
ref: [PLATEAUから街の構造を見る](https://www.estie.jp/blog/entry/2022/08/10/110801)

Geoff Boeingさんの研究に[”Urban spatial order: street network orientation, configuration, and entropy”](https://appliednetsci.springeropen.com/articles/10.1007/s41109-019-0189-1)というものがあります。
これは、道路の方角や長さを街ごとに集計することで、その街の特性がわかるという研究です。

### 集計方法
#### 1. PLATEAUのbuildingデータを読み込む
- 具体的には、東京都データのうち bldg のlod0RoofEdgeのデータ(上空から見た建物の形)を読み込みます。
#### 2. ビルを単純化する
- たとえば、こういうビルがあります。(PLATEAUの建物ID: 13107-bldg-18762)
'''

s1 = '''- そのビルを含む四角形に単純化します。'''

s2 = '''
- 具体的には、shapelyの minimum_rotated_rectangleを使用しました。

#### 3. 四角形の全ての辺の角度（方角）、長さを計算する
- NumPyでやりました。
#### 4. 方角をヒストグラムで集計する
- この時、辺の長さで重み付けしました。大きい建物は、街の印象に対する影響が大きいと思ったためです。
- NumPyでやりました。

'''
st.markdown(s)
st.image(Image.open('data/raw.png'), width=100)
st.markdown(s1)
st.image(Image.open('data/mrr.png'), width=100)
st.markdown(s2)
