# source for https://www.kaggle.com/ginajiyoungsong/modeling-infectios-disease-sir-seir

import scipy.integrate as spi
import numpy as np
import pylab as pl
import datetime as dt

t_start = 0.0
t_inc = 1.0
t_end = 150.0

Rn = 2.3
gamma =  1/14 # I ->R 회복율 = 평균 회복기간의 역수
beta = Rn * gamma


# 2/18 31번확진자 나온날 기준으로 초기 SIR 모델 만듦.
# S0  = 9772 ; I0  = 31;R0 = 2

# tested  4/13
t_date = dt.date(2020, 4, 13)


test = 518743
negative = 494815
confirmed = 10537
released = 7447
death = 217
test_ing = test - (negative + confirmed + released + death)

S0 = negative
# E0 = test_ing
I0 = confirmed
R0 = released + death


N = S0 + I0 + R0
S0 = S0 / N  # susceptible hosts
I0 = I0 / N    # infectious hosts
R0 = R0 / N      # recovered hosts

Input = (S0, I0, R0)

def simple_SIR(INT, t):
  '''The main set of equation'''
  Y=np.zeros((3))
  X = INT      #  S0,   I0
  Y[0] = -beta * X[0] * X[1]
  Y[1] = beta*X[0]*X[1]  - gamma * X[1]
  Y[2] = gamma * X[1]
  return Y # for spicy.odeint


t_range = np.arange(t_start, t_end + t_inc, t_inc)
SIR= spi.odeint(simple_SIR, Input, t_range)

pl.figure(figsize=(15,8))
pl.plot(SIR[:, 0], '-g', label='Susceptibles')
pl.plot(SIR[:, 2], '-k', label='Recovereds')
pl.plot(SIR[:, 1], '-r', label='Infectious')
pl.legend(loc=0)
pl.title('Prediction of Simple nCOV-19 SIR model')
pl.xlabel('Time(day)')
pl.ylabel('individuals')
pl.show()

max_inf_rate = max(SIR[:,1])
max_inf_date = None

for t in range(int(t_end)):
  if SIR[t,1] == max_inf_rate:
    print('최대 증가율 {} , 최대 일 : {}'.format(SIR[t,1],t))
    max_inf_date = t


inc_inf_cnt = int(I0 * (max_inf_rate + 1) * N)
fo_date = t_date + dt.timedelta(days=max_inf_date)

print('{} 예측 결과 :: {}'.format(fo_date,inc_inf_cnt))