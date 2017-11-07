## install yahei fonts in ubuntu system  for matplotlinb

* locat python-version and mv .ttf to location ,eg:/usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/ttf

* set matplotlib params in your code 
``` python
matplotlib.rcParams['font.sans-serif'] = ['YaHei Consolas Hybrid']    # 指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False          # 解决保存图像是负号'-'显示为方
```

* done