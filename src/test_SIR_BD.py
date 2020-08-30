# source for https://www.kaggle.com/ginajiyoungsong/modeling-infectios-disease-sir-seir

import scipy.integrate as spi
import numpy as np
import pylab as pl

'''
parameters

μ   is the per capita death rate, and the population level birth rate.
β   is the transmission rate and incorporates the encounter rate between susceptible and infectious individuals together with the probability of transmission.
γ   is called the removal or recovery rate, though often we are more interested in its reciprocal (1/γ) which determines the average infectious period.
S(0)    is the initial proportion of the population that are susceptible.
I(0)    is the initial proportion of the population that are infectious.All rates are specified in days.

'''

beta = 0.1934 # S ->I 감염율
gamma= 1/14 # I ->R 회복율 = 회복기간의 역수

nu = mu = 1/(70*365) # 자연사망율 반영

t_inc =1.0 ; t_end =150.0

'''
# Initial conditions
pop= 51780579 # 총인구수
test = 136707
test_ing = 28414
negative_tested = 102965 ; NT =negative_tested
print('positive_tested',test_ing + NT) # I0제외된 전체 test 받은 수

I0 = 5328 /test  # 3/3 기준 :확진자
S0 = ( test -I0 )/test # 3/3 기준 :양성판정+음성판정+검사중인 사람수( 총검사자 ) - 확진자'''

# 2/18 31번확진자 나온날 기준으로 초기 SIR 모델 만듦.
S0  = 9772 ; I0  = 31;R0 = 2

N = S0 + I0 + R0
S0  = 9772 /N  # susceptible hosts
I0  = 31 /N    # infectious hosts
R0 = 2 /N      # recovered hosts
Input = (S0, I0, 0.0)

def simple_SIR(INT, t):
  '''The main set of equation'''
  Y=np.zeros((3))
  X = INT      #  S0,   I0
  Y[0] = -beta * X[0] * X[1] - mu * X[0]
  Y[1] = beta*X[0]*X[1]  - gamma * X[1] - mu * X[1]
  Y[2] = gamma * X[1] - mu * X[2]                   # 자연사망자 제외 (위와 식이 조금 변형됨)
  return Y # for spicy.odeint

t_start =0.0 ;
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