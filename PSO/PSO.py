import numpy as np

iteration = 100  #iterasyon sayısı 
swarm_size = 10  #sürünün sayısı 
c1 = 2           #sabit(ivme katsayısı) c1 sayısı 
c2 = 2           #sabit(ivme katsayısı) c2 sayısı 
w = 0.7          #atalet katsayısı(W bir eylemsizlik parametresidir. Bu parametre, son hız değeri tarafından verilen hareket yayılımını etkiler.)
LB = -5.12       #parçacığın alt değeri
UB = 5.12        #parçacığın üst değeri
D = 5            #boyut sayısı başta veriliyor

vmax_coef = 0.1   #max. hız için katsayı 

degiskenler = []  #değişkenler dizisi 
degerler = []     #değerler dizisi

v_max = vmax_coef * (UB - LB) #max. hız hesabı 
v_min = -v_max                #min. hız hesabı


def fitnes_fun(xx):      #Burası Shepere function tanımlaması 

    d = xx.shape[2 - 1]  #değişken sayısı
    sum = []
    for k in range(0, xx.shape[1 - 1]):  #parçacık sayısı

        for ii in range(0, d):

            xi = xx[k][ii]
     ## print (xi)                       #sürüdeki parçacıklarin değerleri listeleniyor
        sum.append([xi**2])

    return np.array(sum)

particles_v = v_min + \
    np.random.uniform(swarm_size, D, (swarm_size, D)) * (v_max - v_min)  #parçacık hızının hesabı(rasgele hesaplanıyor parçacık hızı)

particles_x = LB + \
    np.random.uniform(swarm_size, D, (swarm_size, D)) * (UB - LB)         #parçacık konumunun hesabı(rasgele hesaplanıyor parçacık konumu)

f_val = fitnes_fun(particles_x)     #fitnes_fun fonsiyonundan gelen parçacığın fitnes değeri başlangıçtaki değer(her parçacık için uygunluk değeri) 

##print (particles_v.shape) #parçacık sayısının parçacık sayısı
## print (f_val.shape)      #fitnes değerinin parçacık sayısı
##print (particles_v)       #parçacık hızı listesi

p_best = particles_x  #parçacığın en iyi bireysel konumu
p_best_val = f_val    #kendi en iyi konumuyla karşılaştırır (şu ana kadar bulunan en iyi değer p_best_val değeri)
index = np.argmin(f_val) # fitnes değerinin min. seçilir ve index değişkenine atanır 
#print ( index)   #fitnes degerinin arasındaki min. değerin indexi
g_best = particles_x[index,:]   #g_best'teki tüm parçacıklar arasından en iyi konumunu seçer.
g_best_val = f_val[index]       #global değerin en iyi konumu ile karşılaştırılır.

##print (particles_x)                    #parçacığın konumunu istersek görebiliriz
##print ('g_best_value'), g_best.shape #parçacığın en iyi konumu elde edilir ve listelenir
##print (g_best)


for i in range(0, iteration): #iterasyon sayısının döngüye girmesi
    for j in range(0, swarm_size): #sürü sayısının döngüye girmesi
        for k in range(0, D):      #boyut sayısının döngüye girmesi
            r1 = np.random.rand()  #r1 ve r2 random değerlerinin tanımlanması 
            r2 = np.random.rand()
               #parçacığın yeni hızı hesaplanır.
            particles_v[j][k] = w * particles_v[j][k] + c1 * \
                r1 * (p_best[j][k] - particles_x[j][k]) + \
                c2 * r2 * (g_best[k] - particles_x[j][k])
            #parçacığın yeni hızına göre yeni konumu hesaplanır.
            particles_x[j][k] = particles_x[j][k] + particles_v[j][k]

            if particles_x[j][k] > UB:  #parçacığın değeri  üst değerden büyükse parçacık değeri üst değere eşittir
                particles_x[j][k] = UB
            
            if particles_x[j][k] < LB:  #parçacığın değeri alt değerden küçükse parçacık değeri alt değere eşittir
                particles_x[j][k] = LB
            
            if particles_x[j][k] > v_max: #parçacığın değeri v_max. değerden büyükse parçacık değeri parçacık hızına eşittir
                particles_x[j][k] = v_max
           
            if particles_x[j][k] < v_min:  #parçacığın değeri v_min. değerden küçükse parçacık değeri parçacık hızına eşittir
                particles_x[j][k] = v_min
         

    f_val = fitnes_fun(particles_x)  #fitnes_fun fonksiyonuna girerek parçacık değerinin fitnes değeri bulunması

    for j in range(0, swarm_size):  #sürü sayısını döngüye koyarak 

        if f_val[j][0] < p_best_val[j][0]: #en iyi fitnes değerinin sürüdeki 0. indexinin parçacığın en iyi kendi değerinden küçük olduğunda 
            p_best[j, :] = particles_x[j,:] #en iyi p_best durumunun parçacığın indexine atanması 
            p_best_val[j][0] = f_val[j][0] # en iyi p_best değerinin fitnes değerindeki 0. indexe atanması


        if f_val[j][0] < g_best_val:  #en iyi fitnes değerinin sürüdeki 0. indexinin parçacığın en iyi global değerinden küçük olduğunda 
            g_best = particles_x[j, :] #en iyi g_best durumunun parçacığın indexine atanması 
            g_best_val = f_val[j, 0]   # en iyi g_best değerinin fitnes değerindeki 0. indexe atanması
            print ('Fitness degeri:') 
            print (g_best_val)         #fitnes değerinin okunması
            print('Tasarim degiskenleri:')
            print (g_best)             #tasarım değişkenlerinin okunması

    degiskenler.append(g_best.tolist()) #değişkenlerin listesi 
    ##print (g_best)
    degerler.append(g_best_val.tolist()) #değerlerin listesi
    ##print (g_best_val)

import matplotlib.pyplot as plt #grafik çizimi 

fig, ax = plt.subplots(figsize=(8, 6))   #grafiğin görünümü 8x6
inst = range(0, iteration)
ax.plot(inst, degerler)
ax.set_xlabel("t (s)")
ax.set_ylabel("Yakınsama Eğrisi (mm)")
ax.legend()
ax.grid()
plt.show()



