#地形图的绘制
import matplotlib.pyplot as plt 
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeat
import numpy as np
import netCDF4 as nc
import cmaps
from matplotlib.colors import Normalize

Simsun=FontProperties(fname='D:\Python\SIMSUN.ttf')
Times=FontProperties(fname='C:\windows\FONTS\BASKVILL.TTF')
mpl.rcParams['axes.unicode_minus']=False

fig=plt.figure(figsize=(5,5),dpi=100) #新建画布
axe=plt.subplot(1,1,1,projection=ccrs.PlateCarree()) #设置为简单柱面投影
axe.set_title('1000HPA MONTHLY WIND FIELD IN JAN',fontproperties=Simsun,fontsize=12,y=1.05)#标题设置
axe.add_feature(cfeat.COASTLINE.with_scale('10m'),linewidth=1,color='k')#海岸线（可选海洋/陆地/湖泊）

#设置显示范围和网格
axe.set_extent([0,357.5,-90,90],crs=ccrs.PlateCarree())

#绘制网格
gl=axe.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linewidth=0.8,color='gray',linestyle=':')

#绘制经纬度
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER,LATITUDE_FORMATTER
gl.xlocator=mticker.FixedLocator(np.arange(-179.5,357.5,2.5))
gl.ylocator=mticker.FixedLocator(np.arange(-90,90,2.5))
gl.xformatter=LONGITUDE_FORMATTER
gl.yformatter=LATITUDE_FORMATTER
gl.xlabel_style = {'size': 12, "color": 'k', "font": Times}
gl.ylabel_style = {'size': 12, 'color': 'k', "font": Times}
#读取数据+采样
ncfile=nc.Dataset('D:\Python\suwnd.mon.ltm.nc')#文件地址
uwind=ncfile.variables['uwnd'][1,:,:]
laninterval=3
loninterval=3
uwind=uwind[::laninterval,::loninterval]
ncfile=nc.Dataset('D:\Python\svwnd.mon.ltm.nc')
vwind=ncfile.variables['vwnd'][1,:,:]
vwind=vwind[::laninterval,::loninterval]
lat=ncfile.variables['lat'][:]
lon=ncfile.variables['lon'][:]
lat=lat[::laninterval]
lon=lon[::loninterval]
#箭头均一化、上色
windspeed=np.sqrt(uwind**2+vwind**2)
uwind=uwind/windspeed
vwind=vwind/windspeed
color_map=np.zeros_like(uwind,dtype=float)
ranges=[(0,0.1),(0.1,0.5),(0.5,0.8),(0.8,1.2),(1.2,1.5),(1.5,2),(2,5),(5,100)]
for i in range(len(ranges)):
    color_map[np.where((windspeed>ranges[i][0])&(windspeed<=ranges[i][1]))]=i
norm=Normalize()
norm.autoscale(color_map)
#1.箭头大小相同，颜色不同
quiver=axe.quiver(lon,lat,uwind,vwind,norm(color_map),cmap=cmaps.amwg_blueyellowred,pivot='mid',width=0.001,scale=100,headwidth=4,alpha=1,transform=ccrs.PlateCarree())

#2.箭头大小不同，颜色相同
#quiver=axe.quiver(lon,lat,uwind,vwind,pivot='mid',width=0.001,scale=50,color='blue',headwidth=4,alpha=1,transform=ccrs.PlateCarree())
#axe.quiverkey(quiver,0.91,1.05,1,"1m/s",labelpos='E',coordinates='axes',fontproperties={'size': 10,'family':'Times New Roman'})
#输出
plt.show()