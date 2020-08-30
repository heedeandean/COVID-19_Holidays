# source for https://www.kaggle.com/ginajiyoungsong/modeling-infectios-disease-sir-seir

import scipy.integrate as spi
import numpy as np
import pylab as pl

beta =  0.1934 # S ->I 감염율 = beta 를 구하지 못해서 논문에 나온 beta 값 참조 ( 2020.02.10 중국논문발표)
#우리나라도 중국과 마찬가지로 2차 지역감염이 시작되고 전염력이 2/18 당시 매우 높았던것으로 보여 논문의 beta 도입.

gamma =  1/14 # I ->R 회복율 = 평균 회복기간의 역수
t_inc = 1.0
t_end = 150.0

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
  Y[0] = -beta * X[0] * X[1]
  Y[1] = beta*X[0]*X[1]  - gamma * X[1]
  Y[2] = gamma * X[1]
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