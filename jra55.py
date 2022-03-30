from typing import Optional, Tuple
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import japanize_matplotlib  # noqa
import pygrib
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


plt.rcParams["font.size"] = 18  # 図の文字サイズを大きくしておく
seed = 42  # 乱数状態の固定

path = "./anl_p125_hgt.2012011012"  # JRA-55データのパス
level = 850  # 気圧面
projection = ccrs.PlateCarree()  # 正距円筒図法


def inquire_grib_data(path: str) -> None:
    """データ概要を表示

    Args:
        path(str): 読むデータのパス
    """
    grbs = pygrib.open(path)
    for grb in grbs:
        print(grb)
    return


def read_grib_data(
    path: str, name: Optional[str] = None, level: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """データを読む

    - levelを与えないと全３次元データ

    Args:
        path(str): 読むデータのパス
        name(Optional[str]): 変数名(anl_surf125に対して与える)
        level(Optional[int]): 気圧面（anl_p125に対して与える）

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: 経度, 緯度, 気圧面, データ
    """
    grbs = pygrib.open(path)

    if name is not None:
        alines = grbs.select(name=name)
    elif level is not None:
        alines = grbs.select(level=level)
    else:
        alines = grbs.select()

    lat, lon = alines[0].latlons()  # lonは経度、latは緯度データ: (ny,nx)の２次元格子です
    ny, nx = lat.shape
    nline = len(alines)
    gdata = np.empty((nline, ny, nx), dtype="float32")
    levels = np.empty((nline), dtype="float32")

    for iline, aline in enumerate(alines):
        gdata[iline, :, :] = aline.values[::-1, :]
        levels[iline] = aline["level"]

    return lon, lat[::-1], levels, gdata


lon, lat, levels, data = read_grib_data(path, level=level)
data850 = data[0]


# 描画領域の設定
fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(projection=projection)

# 地図関係
ax.add_feature(cfeature.LAND)
ax.coastlines(lw=0.5)
ax.gridlines(linestyle="-", color="gray", draw_labels=True)

# 等高線を描画
# オプションはこちらを参照のこと：https://matplotlib.org/3.5.1/api/_as_gen/matplotlib.pyplot.contour.html
cont = ax.contour(lon, lat, data850, transform=ccrs.PlateCarree(), cmap="rainbow")
cont.clabel(fmt="%1.1f", fontsize=14)

fig.savefig("output/jra55_contour.png")


projection_lambert = ccrs.LambertConformal()  # ランベルト正角円錐図法

fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(projection=projection_lambert)

ax.add_feature(cfeature.LAND)
ax.coastlines(lw=0.5)
ax.gridlines(linestyle="-", color="gray", draw_labels=True)
ax.set_extent([120, 150, 20, 50], ccrs.PlateCarree())  # 範囲の指定は正距円筒図法を利用

contf = ax.contourf(
    lon,
    lat,
    data850,
    transform=ccrs.PlateCarree(),
    cmap="rainbow",
    extend="both",
    levels=range(1200, 1600, 50),
)
fig.colorbar(contf, orientation="vertical", shrink=0.8)

fig.savefig("output/jra55_contourf.png")


df_weather = pd.read_html(
    "https://www.geekpage.jp/web/livedoor-weather-hacks/latlng.php", header=0
)[0]

df_weather = df_weather.dropna(axis=0)
df_weather["天気"] = [random.choice(["晴れ", "曇り", "雨"]) for i in range(len(df_weather))]

fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(projection=projection_lambert)

ax.add_feature(cfeature.LAND)
ax.coastlines(lw=0.5)
ax.gridlines(linestyle="-", color="gray", draw_labels=True)
ax.set_extent([120, 150, 20, 50], ccrs.PlateCarree())

cont = ax.contour(
    lon,
    lat,
    data850,
    transform=ccrs.PlateCarree(),
    cmap="rainbow",
    levels=range(1200, 1600, 50),
)
cont.clabel(fmt="%1.1f", fontsize=14)

# 散布図を描画
# オプションはこちらを参照のこと：https://seaborn.pydata.org/generated/seaborn.scatterplot.html
# sns(seaborn)はmatplotlibのラッパーライブラリでpd(pandas)のDataFrameなどとの相性が非常に良い
sns.scatterplot(
    x="経度(lng)",
    y="緯度(lat)",
    hue="天気",
    data=df_weather,
    transform=ccrs.PlateCarree(),
    palette="rainbow",
    ax=ax,
)

fig.savefig("output/weather_sample.png")


df_cluster = pd.read_csv(
    "cluster_data.csv",
    encoding="shift-jis",
)

fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(projection=projection)

ax.coastlines(lw=0.5, color="gray")
# メモリだけ表示するのはめんどくさそうだったので、幅0の緯線経線を引いて力技で表示
ax.gridlines(draw_labels=True, linewidth=0)
ax.set_extent([120, 150, 20, 50], ccrs.PlateCarree())

# styleでどの値に応じてマーカーの形を変えるかを規定して、markersで実際に利用するマーカーの形を記述する
sns.scatterplot(
    x="lon",
    y="lat",
    hue="cluster_NO",
    style="frag",
    markers=["o", "^"],
    data=df_cluster,
    s=100,
    palette="rainbow_r",
    ax=ax,
)

fig.savefig("output/cluster_r.png")


# ちなみにpythonでクラスター分析(k-means法)

k_means = KMeans(n_clusters=6, random_state=seed).fit(df_cluster.loc[:, "1":"12"])
df_cluster_copy = df_cluster.copy()
df_cluster_copy["cluster_py"] = k_means.labels_
df_cluster_copy

fig = plt.figure(figsize=(20, 15))
ax = fig.add_subplot(projection=projection)

ax.coastlines(lw=0.5, color="gray")
ax.gridlines(draw_labels=True, linewidth=0)
ax.set_extent([120, 150, 20, 50], ccrs.PlateCarree())

sns.scatterplot(
    x="lon",
    y="lat",
    hue="cluster_py",
    style="frag",
    markers=["o", "^"],
    data=df_cluster_copy,
    s=100,
    palette="rainbow_r",
    ax=ax,
)

fig.savefig("output/cluster_py.png")


x_pca = pd.DataFrame(
    PCA(n_components=2).fit_transform(df_cluster.loc[:, "1":"12"]),
    columns=["1st", "2nd"],
)
x_pca["cluster"] = df_cluster_copy["cluster_py"]

sns.scatterplot(x="1st", y="2nd", hue="cluster", data=x_pca, palette="rainbow_r")
plt.legend(bbox_to_anchor=(1.05, 1))

fig.savefig("output/pca.png")
