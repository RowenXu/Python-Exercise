import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import cmaps
import netCDF4 as nc
import cartopy.feature as cfeature
# 读取500hpa位势文件
ncfile = nc.Dataset("D:\ExtremeHeat\\2022Heatwave\\2022Heatwave\h_Jul_500hPa.nc")
h = ncfile.variables['z'][:]
lon = ncfile.variables['longitude'][:]
lat = ncfile.variables['latitude'][:]
#计算位势高度的平均值
h_mean = np.mean(h,axis=0)/100
#建立画布
fig = plt.figure(figsize=(10,8))
#建立投影
ax = plt.axes(projection=ccrs.PlateCarree())
#添加海陆分界线
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
#添加国家边界
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
#添加经纬度坐标
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.000000008, color='gray',linestyle=':')
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
gl.xlocator = mpl.ticker.FixedLocator(np.arange(-180,180, 60))
gl.ylocator = mpl.ticker.FixedLocator(np.arange(-90,90, 30))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 12, "color": 'k'}
gl.ylabel_style = {'size': 12, 'color': 'k'}
#添加标题
ax.set_title('500hPa Geopotential Height in the Pacific Ocean',fontsize=20)
#设置等值线
contourf=ax.contourf(lon,lat,h_mean,levels=np.arange(400,600,30),cmap=cmaps.GMT_seis)
plt.show()