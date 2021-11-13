# -*- coding: utf-8 -*-
"""Simple Stock Analysis of PT Bukalapak.com Tbk for Long Term Investment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eq1RQroGNBf1BJ0jvQNZFOrJkzgT6yly

# Simple Stock Analysis for Long Term Investment

### A. Question(s) and Goal(s)
   - Jika kita ingin berinvestasi dalam interval jangka panjang, bagaimana kita bisa mengurangi risiko sekaligus memaksimalkan pengembalian investasi?
   - Apa cara terbaik untuk memilih saham berdasarkan kriteria dari pertanyaan sebelumnya?

Tujuan dari analisis ini adalah untuk menghasilkan sekelompok saham yang relatif andal dalam memberikan pengembalian investasi mengingat risiko yang terlibat.
Analisis harus memberikan data yang substansial untuk menggunakan saham secara percaya diri untuk analisis atau penggunaan di masa mendatang.

### B. Data Collection

Ada banyak cara untuk mengumpulkan harga saham historis dengan fundamentalnya. Untuk analisis khusus ini, Pandas menyediakan perpustakaan untuk
mengambil forum data dari berbagai sumber. Pustaka tersebut bernama Pandas Data Reader. Perpustakaan adalah pembungkus untuk mengambil data seperti stok historis
harga, PDB negara, data ekonomi Dunia, dll. Analisis ini secara khusus. Data Yahoo Finance digunakan karena gratis dan memiliki
database saham yang sangat besar. Dengan menghindari pekerjaan manual, payah seperti mengunduh file CSV, analisis dapat digunakan untuk stok sebanyak mungkin.
"""

pip install pandas-datareader

import pandas_datareader.data as web

!pip install --upgrade pandas
!pip install --upgrade pandas-datareader

"""For starter, let's analyze S&P 500 (SPY). As the ETF is famous for it's reliability to indicate the world's economy. To make the data more
relevant, 10 years worth of data is fetched.
"""

buka = web.DataReader('BUKA.JK', 'yahoo', start='2021-08-06', end='2021-11-13')
buka

"""Seperti yang ditunjukkan di atas, data yang diambil memiliki beberapa opsi untuk melihat harga untuk setiap hari tertentu sejak 2010. Karena analisis akhir akan melibatkan
pengembalian investasi, harga Penutupan Disesuaikan. Digunakan Pilihan ini diambil untuk menyederhanakan analisis. juga, berdasarkan jangka waktu harga penutupan yang disesuaikan,
harga harus paling mencerminkan harga ETF pada hari tertentu.
"""

buka = buka[['Adj Close']]. rename(columns={'Adj Close': 'Price'}).copy()
buka.tail(10)

"""Untuk lebih memahami data, mari kita plot menggunakan Matplotlib. Perpustakaan menyediakan banyak toolkit visualisasi."""

import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
plt.style.use('seaborn')

plt.figure(figsize=(16,10))
plt.plot(buka['Price'], '-')
plt.gcf().autofmt_xdate()
plt.title('BUKA Prices Since 2021', fontsize=20)
plt.xlabel('Date', fontsize=16)
plt.ylabel('Price in Rp', fontsize=16)
plt.show()

"""Plot di atas menunjukkan harga S&P 500 dari 2010 hingga Januari 2021. Seperti yang diharapkan, data sudah menunjukkan tren yang jelas, yaitu naik. Untuk
contoh, mari kita ambil pengembalian investasi jika seseorang mengembalikan uang pada tahun 2010. Karena plot dengan gaya yang sama akan banyak digunakan dalam analisis ini,
fungsi dapat ditulis untuk menyederhanakan penggunaan di masa mendatang.
"""

def plot_time_series(data, title, x_label, y_label):
    plt.figure(figsize=(16,10))
    plt.plot(data, '-')
    plt.gcf().autofmt_xdate()
    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.show()

import numpy as np

price_IPO = buka['Price'][0]
price_2021 = buka['Price'][-1]
roi = np.log(price_2021 / price_IPO) * 100 # Logarithmic Return
print(f'Price on {buka.index[0].strftime("%d-%m-%y")}: Rp{round(price_IPO, 2)}')
print(f'Price on {buka.index[-1].strftime("%d-%m-%y")}: Rp{round(price_2021, 2)}')
print(f'Return of Investment: {round(roi, 2)}%')

"""Dengan menggunakan pengembalian logaritmik, seseorang dapat mengharapkan lebih dari dua kali lipat investasi. Ini berarti jika USD 1000  diinvestasikan kembali pada tahun 2010, uangnya akan bernilai sekitar USD 2240 hari ini. Jadi, dalam rentang 10 tahun, seseorang dapat mengharapkan pengembalian rata-rata 10% setiap tahun. Meskipun ini bukan jaminan, ini harus memberikan perkiraan kasar dari data S&P 500. Numpy adalah perpustakaan hebat yang berisi banyak fungsi dan karya matematika yang kuat sangat baik dengan sejumlah besar data. Namun, dalam contoh khusus ini, fungsi log harus mencukupi.

### C. Data Analysis

Dengan melihat sekilas data, ada beberapa pekerjaan yang harus dilakukan sebelum dapat digunakan. Salah satunya adalah mencari pengembalian investasi dari setiap harinya.
Ini adalah langkah yang perlu. Dalam Investasi, harga saham pada hari tertentu tidak terlalu relevan. Selisih harga 2 hari yang berbeda harga
adalah.
"""

buka['Price d+1'] = buka['Price'].shift(-1)
buka['ROI'] = np.log(buka['Price d+1'] / buka['Price']) * 100
buka

#Visualisasi ROI of S&P 500 everyday since 2011 - 2021
plot_time_series(buka['ROI'], 'ROI of BUKA Stock everyday', 'Date', 'ROI in %')

"""Dengan melihat grafik di atas, meskipun agak sulit untuk membedakannya, ada beberapa petunjuk yang bisa diambil. Misalnya, ROI terburuk
terjadi sekitar tahun 2020 dimana kurang dari -10%. Namun, hari terbaik datang juga sekitar tahun 2020 di mana ROI melebihi 8% dalam satu hari.
Selanjutnya, di bagian awal, dinyatakan bahwa analisis akan digunakan untuk berinvestasi dalam interval jangka panjang. Ini berarti ROI harian akan kurang relevan karena
intervalnya terlalu pendek. Resampling adalah cara yang baik untuk mengubah data dari ROI harian menjadi ROI bulanan.
"""

buka = buka[['ROI']].resample('1M').sum()
buka

#Visualisasi ROI of BUKA Stock every month
plot_time_series(buka['ROI'], 'ROI of BUKA Stock every month', 'Date', 'ROI in %')

buka.describe() #Operation Describe

"""dari visualisasi dan ringkasan di atas, kini data terlihat sedikit lebih mudah dibaca. Misalnya, meskipun ROI naik turun,
mereka tidak jauh dari titik tertentu. Ini disebut osilasi. Nilai tengah dari osilasi itu adalah rata-rata dari data, bentuk contoh ini adalah 1,06
Ini juga berarti, rata-rata, seseorang dapat mengharapkan ROI 1% setiap bulan selama periode 10 tahun. Kemudian, osilasi mereka juga memiliki bagian atas
terikat dan batas bawah, dan itu disebut simpangan baku atau std. dengan sedikit modifikasi pada kodenya, semuanya dapat divisualisasikan sebagai berikut.
"""

def plot_time_series_with_summary(data, title, x_label, y_label):
    plt.figure(figsize=(16, 10))
    plt.plot(data, '-')
    plt.gcf().autofmt_xdate()
    plt.axhline(y=data.mean(), label='Mean', color='r')
    plt.fill_between(data.index, (data.mean()-data.std()), (data.mean()+data.std()), color='b', alpha=.1, label='Volatility')
    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.legend()
    plt.show()

#Visualization Volatility ROI of BUKA Stock every month 
plot_time_series_with_summary(buka['ROI'], 'ROI of BUKA Stock every month', 'Date', 'ROI in %')

"""Dalam harga saham, std disebut volatilitas. Ini adalah metrik penting karena ketika sejumlah besar uang terlibat, saham yang kurang stabil adalah
lebih menguntungkan. Stok yang kurang volatil berarti lebih mudah diprediksi karena risikonya juga lebih rendah. Terlebih lagi, Jika data terdistribusi normal, satu
terdistribusi normal. Salah satu yang cocok adalah plot Q-Q.
"""

import statsmodels.api as sm
sm.qqplot(buka, line = '45').show()

"""Menggunakan statsmodels libray, plot Q-Q harus menunjukkan jika dataset terdistribusi normal. Jika sebagian besar titik jatuh pada garis merah, maka distribusinya
terdistribusi normal. Sayangnya, bukan data ini. JADI singkatnya, pengumpulan data saham dalam periode 10 tahun dapat menghasilkan perkiraan kasar untuk
menghasilkan ekspektasi tentang apa yang digunakan ROI dan risiko. Rata-rata dan Standar Deviasi. Namun, untuk menentukan apakah risiko dan ROI itu tinggi atau rendah, diperlukan perbandingan dengan saham lain.
"""

