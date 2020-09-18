import scipy.integrate as spi
import numpy as np
import matplotlib.pyplot as pl
import datetime as dt

np.set_printoptions(precision=3)


# Initial conditions
# 인구수 51780579

S0 = 9772  # :양성판정+검사중+음성판정
E0 = 818  # :검사중
I0 = 31  # :확진자
R0 = 2  # :완치자 + 사망자(0)


# testd 4/13
# t_date = dt.date(2020, 4, 13)
#
# nation_cnt = 51780579
# test = 518743
# negative = 1882155
# confirmed = 4660
# released = 15198
# death = 217
# test_ing = test - (negative + confirmed + released + death)

# testd 9/1
t_date = dt.date(2020, 9, 1)

# 누적 검사 : 1,959,080 / 격리 중 : 4,660 / 격리 해제 : 15,198 / 사망 : 324 / 결과 음성 : 1,882,155 / 검사중 : 56,743 / 누적확진 : 20,182
nation_cnt = 51780579
test = 1959080
negative = 494815
confirmed = 20182
released = 15198
death = 324
test_ing = test - (negative + confirmed + released + death)


S0 = nation_cnt - (test_ing + confirmed + released + death)
E0 = test_ing
I0 = confirmed
R0 = released + death



# Time vector
t = np.linspace(0, 100, 100)

N = S0 + E0 + I0 + R0  # 모집단

S0_ = S0 / N
E0 = E0 / N
I0 = I0 / N
R0 = R0 / N

# print(S0_)  # 양성판정 확진자 + 음성판정 격리해지자수 비율 proporion

'''
Ro = 0.5 # 1인당 전파율 1월20일 보고된 한국코로나바이러스 역학조사 논문에 나온 수치)
print('논문에 보고된 Ro 평균',Ro)
To = 336 # 14*24 회복기간 2주  *  24시간
beta = (Ro/To) + (Ro/(To*S0))   # Ro 이용해서 beta 구하는 논문수식
print('\n논문 수식으로 구한 감염율 beta =',beta) 
논문 수식으로 구한 감염율 beta = 0.0014882475196382277
1월 초기에 전염병예측모델과 현재 현황이 많이 달라져서 사용할수 없음. 그당시 Ro, beta  모두 작은값.
'''

Rn = 1.0
gamma =  1/14 # I ->R 회복율 = 평균 회복기간의 역수
beta = Rn * gamma
ramda = 1 / 14
sigma = 0.25
nu = mu = 1/(70*365) # 자연사망율 반영


Input = (S0_, E0, I0, R0)


def SEIR(INT, t):
    '''The main set of equation'''
    Y = np.zeros((4))
    X = INT  # S0,   I0
    Y[0] = mu - beta * X[0] * X[2] - mu * X[0]
    Y[1] = beta * X[0] * X[2] - sigma * X[1] - mu * X[1]
    Y[2] = sigma * X[1] - gamma * X[2] - mu * X[2]  # (자연사망자 제외)
    Y[3] = gamma * X[2] - mu * X[3]
    return Y  # for spicy.odeint


t_start = 0.0
t_end = 180
t_inc = 1.0
t_range = np.arange(t_start, t_end + t_inc, t_inc)
SEIR = spi.odeint(SEIR, Input, t_range)



pl.figure(figsize=(15, 10))
pl.plot(SEIR[:, 0], '-g', label='Susceptibles')
pl.plot(SEIR[:, 1], '-b', label='Exposed')
pl.plot(SEIR[:, 2], '-r', label='Infectious')
pl.plot(SEIR[:, 3], '-k', label='Recovereds')
pl.legend(loc=0)
pl.title('Prediction of nCOV-19 SEIR model')
pl.xlabel('Time(days)')  # 국내 전염병의 추세가 하루하루 다르기 때문에.. 일주일단위보다는 1일단위로 보는게 맞는듯..
pl.ylabel('individuals')

pl.show()

max_inf_rate = max(SEIR[:,2])
max_inf_date = None

for t in range(int(t_end)):
    
    if SEIR[t,2] == max_inf_rate:
        print('최대 증가율 {} , 최대 일 : {}'.format(SEIR[t,2],t))
        max_inf_date = t


inc_inf_cnt = int(I0 * (max_inf_rate + 1) * N)
fo_date = t_date + dt.timedelta(days=max_inf_date)

print('{} 예측 결과 :: {}'.format(fo_date,inc_inf_cnt))

