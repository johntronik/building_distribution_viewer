import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.markdown('## 都市を集計します')
ku = st.selectbox('街を選んでください', ['千代田区', '中央区', '港区', '新宿区', ''])

left,right = st.columns([1,2])
with right:
    if ku=='千代田区':
        image2 = Image.open('data/map_chiyoda.png')
    else:
        image2 = Image.open('data/map_chuo.png')
    st.image(image2)

with left:
    if ku=='千代田区':
        image1 = Image.open('data/output_chiyoda.png')
    else:
        image1 = Image.open('data/output_chuo.png')
    st.image(image1)

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
