## 프로젝트 개요

이 프로젝트는 경기도가 주최한 ‘**데이터 기반 코로나19 예측 공모전**’ 에 참여하기 위해 만들어졌으며, 경기도 경제 과학 진흥원이 설명하는 공모는 다음과 같다.

- 목적 : 데이터를 활용한 코로나19 예측을 수행함으로써 데이터 활용 능력에 대한 역량 강화 및 문화 조성
- 주제 : 추석기간 동안(`20. 9. 30 ~ 10. 4) 경기도 내 코로나19 지역감염 확진자 수 예측 및 지역감염을 줄이기 위한 정책 제언
- 활용 데이터 : 기본 제공 데이터 + 참가자가 수집가능한 모든 데이터를 자체적으로 수집/활용
  - 기본 제공 데이터 : [경기도감염병관리지원단](www.gidcc.or.kr)에서 매일 갱신되는 확진자 데이터 활용
  - 참가자 자체 수집 데이터 : 사회적 거리두기 시행 기간, 마스크 착용률 등
- 개발환경
  - python info
    - Version : 3.6.10
    - Anaconda ver 4.8.2
    - package info
      - jupyter notebook  ver 6.0.3
      - tensorflow ver 2.1.0
      - numpy ver 1.19.1
      - pandas ver 1.1.1
  - R info
    - Version : 4.0.2
  - DB info
    - MySQL ver 5.7
## 프로젝트 참여자

- [alpha-94](https://github.com/alpha-94)
  - 데이터 수집, 국내 시계열 예측 모델링 구축
- [jung-un](https://github.com/jung-un)
  - 데이터 분석, 정책 제언
- [eunji32](https://github.com/eunji32)
  - 데이터 분석, 정책 제언
- [heedeandean](https://github.com/heedeandean)
  - 데이터 수집, 해외 시계열 모델링 구축, DB 구축



## 가설 및 변수 설정

### 경기도 확진자 데이터 분석 및 가설 설정

- 경기도 확진자의 주 감염경로는 다음과 같다.

  |   감염경로   |  비율  |
  | :----------: | :----: |
  | **접촉감염** | 73.06% |
  |    불명확    | 13.40% |
  |   집단발생   | 13.21% |
  |   해외유입   | 0.29%  |
  |  타지역감염  | 0.05%  |

  주로 확진자 감염경로는 확진자에 의한 접촉이 가장 많은 비율로 나타났다.

- 따라서 가설을 *'접촉을 줄일 수록 확진자 수는 감소할 것이다. '* 로 정했다.

- 국내감염의 경우 확진자의 접촉이 가장 높은 수치기록을 가졌으며 다양한 집단 모임에서 감염 발생하였으며 접촉 관련 변수 선정 후 확진자 수와 관련성 검증을 하기로 했다.

- 해외 감염 확진자의 경우 97% 이상이 자가격리 기간을 가져 타인에게 전파할 위험성이 낮으므로 접촉과 연관성이 낮아 가설 검증에서 제외하기로 하고 해외 확진자 수의 경우 누적 확진자 수를 기준으로 시계열 분석을 진행하기로 했다.

### 변수 선정 기준

- 1일 예상 감염률(2차 위험률)

  - 확진자는 **유증상자**와 **무증상자**로 나뉠 수 있으며 각각 **3.5%** , **0.8%** 의 위험률을 지닌다고 [방역당국이 설명](https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=103&oid=584&aid=0000009104)해 주었다. 

    따라서 확진 상세사항을 유증상자, 무증상자를 나눴고 일자별 계산을 통해 2차위험률(spread) 변수를 설정하여 확진자 수와 연관성 분석을 실시 하였다.

- 사회적 거리두기

  - 확진자가 폭발할 때마다 방역당국이 지정한 방역대책 중 사회적 거리두기에 따라 가중치를 두어 확진자 수와 연관성 분석을 실시 하였다.

  - 다음은 사회적 거리두기 단계에 따른 가중치의 설명이다.

    |          기간           |         단계 내용         | 가중치 |
    | :---------------------: | :-----------------------: | :----: |
    |      ~ 2020-03-21       |             -             |   0    |
    | 2020-03-22 ~ 2020-04-19 |   강력한 거리두기 시행    |  1.5   |
    | 2020-04-20 ~ 2020-08-18 | 완화한 형태 거리두기 시행 |   1    |
    | 2020-08-19 ~ 2020-08-29 |   수도권 거리두기 2단계   |   2    |
    | 2020-08-30 ~ 2020-09-13 |  사회적 거리두기 2.5단계  |  2.5   |
    |      2020-09-14 ~       |   사회적 거리두기 2단계   |   2    |

- 1일 검사자 수

  - 검사자 수는 확진자와의 접촉이 의심되어 검사를 받았다고 가정하고 검사자 수와 확진자 수의 연관성 분석을 실시 하였다.

### 변수 적합성 검증

- 변수 적합성 검증의 경우 R 의 `corrplot` 을 이용하여 적합성 검증을 진행하였다.

- 확진자 수와 1일 검사자 수의 관계

  ![](https://github.com/heedeandean/COVID19_Holidays/blob/master/md/pic/exam_.png)

- 확진자 수와 사회적거리두기 가중치의 관계

  ![](https://github.com/heedeandean/COVID19_Holidays/blob/master/md/pic/policy_.png)

- 확진자 수와 2차 공격률의 관계

  ![](https://github.com/heedeandean/COVID19_Holidays/blob/master/md/pic/spread_.png)

  >  1일 검사자와 사회적 거리두기 가중치의 경우 다소 높은 상관관계를 가지며 2차 공격률의 경우 매우 높은 상관관계를 가진다. 이에 따른 결과를 통해 접촉을 줄일 수록 확진자 수는 줄어든다는 가설은 입증된다.

## 활용 데이터 및 가공

### 데이터 수집 및 적재

- [경기도감염병관리지원단](http://www.gidcc.or.kr/%EC%BD%94%EB%A1%9C%EB%82%98covid-19-%ED%98%84%ED%99%A9/) 과[ 경기도청과 경기도감염관리지원단](https://www.gg.go.kr/bbs/board.do?bsIdx=722&menuId=2903#page=1)에서 제공하는 데이터를 이용하여 크롤링을 진행했다.

  크롤링은 크게 `BeautifulSoup`과 `selenium` 을 이용하여 수집하고 기본 전처리를 진행했다.

- 데이터 적재의 경우 `MySQL` 을 이용하여 적재 하였다.

### 예측 모델링 내 input 데이터 가공

- 현재 데이터에서 향후 데이터의 입력값이 있어야 미래 확진자 수를 예측할 수 있기 때문에 현재 모델  X에 해당하는 2차 공격률, 1일 검사자 수를 (사회적 거리두기의 경우는 2단계로 고정)  시계열 분석을 통해 현재 데이터 이후 X 데이터를 예측했다.

- 시계열에 따른 선형 모델은 `numpy.polyfit` 을 이용하였고 최근 8.15 집회(8/15 ~ 9/22)에 따른 선형 추세선은 다음과 같다.

  - 2차 공격률

  $$
  y  =0.0006548859543817529x + 1.283555294117647
  $$

  - 검사자 수

  $$
  y  = 116.86905162064834x + 10069.988235294119
  $$

  

- 추세선 결과에 따라 미래 X 데이터를 도출하였다.



## 모델 구현

### 경기도 국내 감염 확진자 수 예측 모델

- SETTING

  - Function

    > - build_dataset
    >
    >   > LSTM 시계열형 데이터 빌드
    >
    > - build_dataset_x
    >
    >   > X 데이터 시계열형 데이터 빌드
    >
    > - series_diff
    >
    >   > Seires  날짜 별로 분리하기 위한 함수
    >
    > - polyfit_prd
    >
    >   > 추세선 함수

  - Parameter

    > LSTM  에 맞는 시퀀스 및 INPUT, OUTPUT dimension 지정



- Preprocess Data

  - load data

    > `pymysql` 패키지를 이용하여 MySQL 연결 후 데이터 로드

  - Scaling (Min-Max Scaling)

    > `sklearn` 패키지 내 `preprocessing.MinMaxScaler` 를 이용하여 정규화 하였다.

- LSTM Modeling

  - Layers

    ```python
    tf.model = tf.keras.Sequential()
    tf.model.add(tf.keras.layers.LSTM(units=5,input_shape=(seq_length, data_dim), return_sequences=True))
    tf.model.add(tf.keras.layers.LSTM(units=5, return_sequences=False))
    tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='linear'))
    ```

    > 약 200일 가량의 데이터 셋으로 LSTM 을 모델링 하기에는 너무 예민한지 유닛 수를 늘리면 늘릴 수록 오버피팅이 쉽게 일어났다. 그래서 유닛수를 차차 줄이면서 최적의 값을 찾았다. 가장 적합한 활성화 함수는 relu, linear 두가지 였지만 linear 가 가장 안정적인 오차율을 발생시켰다.

  - Compile

    ```python
    tf.model.compile(loss='mse',
                     # optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                     optimizer='adam',
                     metrics=['accuracy'])
    
    es = EarlyStopping(monitor='val_loss', mode='min',patience = 40)
    
    h = tf.model.fit(trainX, trainY,
                     epochs=iterations,
                     batch_size=7,
                     validation_data=[testX,testY],
                     verbose=1,
                     callbacks = [es]
                    )
    ```

    > optimizer 에 learning_rate 적용하려고 했으나 애초에 Tensorflow 내에 랜덤수를 고정하지도 않았으며 너무나 예민했기에 자동으로 지정해주었고, loss 는 Mean Square Error 를 이용하였다.
    >
    > 또한 `EarlyStopping` 을 이용하여 40번 정도를 돌면서 `val_loss` 가 최소가 되었을때 멈추도록 하였다.

  - Predict

    ```python
    test_predict = tf.model.predict(testX)
    MSE = mean_squared_error(testY.reshape(-1,1),test_predict) 
    RMSE = np.sqrt(MSE)
    pred_score = 100 * ( 1 - (((test_predict - testY)**2).sum())/((testY**2).sum()))
    ```

    > `pred_score`는 88.95741695607973 정도가 나왔다. 나름 모델 피팅이 좋게 나왔으며 90점 이상인 모델은 저장이 되도록 세이브포인트를 지정했다.

  - Visualization

    ![](https://github.com/heedeandean/COVID19_Holidays/blob/master/md/pic/predict_cfm.png)

    > 추석기간은 아무래도 집에 있어야 할 것 같다.😩

### 경기도 해외 유입 확진자 수 예측 모델

- SETTING

  - load data

    > 마찬가지로 MySQL 로 로드 하였으며, 국내 테이블과는 다르게 해외 테이블은 미리 전처리 하여 DB에 저장 되어있다.

- Modeling

  - Produce

    > 해외 감염은 별다른 변수 없이 누적 확진자 수를 통해 시계열 모델링 하였다.
    >
    > 모델은 `fbprophet.Prophet` 를 이용하였으며 parameter 를 조정하며 모델을 생성하였다.

  - Visualization

    ![](https://github.com/heedeandean/COVID19_Holidays/blob/master/md/pic/predict_predict_cfm.png)

    > 10월 4일에 yhat 이 lower 와 upper 가 10명 정도 차이가 난다. 



## 결론

추석 기간에 확진자 수는 41~47명 사이로 웃도는 것으로 모델 결과가 나왔다.

8월 달의 집회로 많은 확진자 수가 폭발적으로 늘어 대유행을 만들었고 이 여파는 10월 중순까지 지속할 것으로 예측된다. 

더도말고 덜도 말고 한가위만 같아야겠지만 이번 추석은 최대한 친지 방문이나 여행을 가는 것을 고려해 보아야 할 것 같다. 

2019 년 12월 우한에서부터 발발되어 지금까지 장기적인 바이러스와 싸움이 지속하고 있지만, 서로의 배려와 방역으로 우리는 이겨낼 수 있을 것이다.  코로나의 종식을 기원한다.👏👏

