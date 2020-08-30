import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as pl

# Initial conditions
# 인구수 51780579
S0 = 9772  # :양성판정+검사중+음성판정
E0 = 818  # :검사중
I0 = 31  # :확진자
R0 = 2  # :완치자 + 사망자(0)



# Time vector
t = np.linspace(0, 100, 100)

N = S0 + I0 + R0  # 모집단

S0_ = S0 / N
E0 = E0 / N
I0 = I0 / N
R0 = R0 / N

print(S0_)  # 양성판정 확진자 + 음성판정 격리해지자수 비율 proporion

'''
Ro = 0.5 # 1인당 전파율 1월20일 보고된 한국코로나바이러스 역학조사 논문에 나온 수치)
print('논문에 보고된 Ro 평균',Ro)
To = 336 # 14*24 회복기간 2주  *  24시간
beta = (Ro/To) + (Ro/(To*S0))   # Ro 이용해서 beta 구하는 논문수식
print('\n논문 수식으로 구한 감염율 beta =',beta) 
논문 수식으로 구한 감염율 beta = 0.0014882475196382277
1월 초기에 전염병예측모델과 현재 현황이 많이 달라져서 사용할수 없음. 그당시 Ro, beta  모두 작은값.
'''
beta = 0.1934  # 중국논문에 나온 beta 값
ramda = 1 / 14
sigma = 0.25
nu = mu = 1/(70*365) # 자연사망율 반영
gamma= 1/14 # I ->R 회복율 = 회복기간의 역수

Input = (S0_, E0, I0)


def SEIR(INT, t):
    '''The main set of equation'''
    Y = np.zeros((3))
    X = INT  # S0,   I0
    Y[0] = mu - beta * X[0] * X[2] - mu * X[0]
    Y[1] = beta * X[0] * X[2] - sigma * X[1] - mu * X[1]
    Y[2] = sigma * X[1] - gamma * X[2] - mu * X[2]  # (자연사망자 제외)
    return Y  # for spicy.odeint


t_start = 0.0;
t_end = 150;
t_inc = 1.0
t_range = np.arange(t_start, t_end + t_inc, t_inc)
SEIR = spi.odeint(SEIR, Input, t_range)

Rec = 1. - (SEIR[:, 0] + SEIR[:, 1] + SEIR[:, 2])

pl.figure(figsize=(15, 10))
pl.subplot(311)
pl.plot(SEIR[:, 0], '-g', label='Susceptibles');
pl.legend(loc=0)
pl.title('Prediction of nCOV-19 SEIR model')
pl.xlabel('Time(days)')  # 국내 전염병의 추세가 하루하루 다르기 때문에.. 일주일단위보다는 1일단위로 보는게 맞는듯..
pl.ylabel('Susceptibles')

pl.subplot(312)
pl.plot(SEIR[:, 1], '-b', label='Exposed')
pl.plot(SEIR[:, 2], '-r', label='Infectious');
pl.legend(loc=0)
pl.xlabel('Time(days)')
pl.ylabel('Infectious')

pl.subplot(313)
pl.plot(Rec, '-k', label='Recovereds')
pl.xlabel('Time(days)')
pl.legend(loc=0)
pl.ylabel('Recovereds')
pl.show()