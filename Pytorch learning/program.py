#WT方法对天气情况（环流异常场）进行分类
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np
import netCDF4 as nc
from minisom import MiniSom
import math
#输入位势高度场训练集
file=nc.Dataset("Ana\Data\\adaptor.mars.internal-1693670161.9362974-29925-5-c9872e5c-a35b-4f1a-8627-3295833c7db0.nc")
#数据预处理（标准化）
print(file.variables.keys())
g=9.80665
geoheight=file.variables['z'][:]/10/g
longitude=file.variables["longitude"][:]
latitude=file.variables["latitude"][:]
time=file.variables["time"][:]
for x in longitude.shape:
    for y in latitude.shape:
        for z in time.shape:
            geoheight_anomaly[z,x,y]=1
geoheight_Average=np.mean(geoheight,0)


geoheight_anomaly = np.zeros(geoheight.shape)
#通过SOM进行降维处理（将三维数据降维成二维）
#初始化模型
som_size=5*math.sqrt(geoheight_anomaly)
print(som_size)
som=MiniSom(som_size[0],som_size[1],sigma=.5,learning_rate=.5,neighborhood_function='gaussian',random_seed=42)
som.train_batch(geoheight,1000,verbose=True)
