# NLP 01 (대답해조) Final Project

## 모델 및 파이프라인 파트를 하고 있는 중입니다!(KBS)
#
## 현재 상황입니다!

### model/pipeline.py 제작(완료)
### model/train.py(for FineTuning)(해야함)

#
# 사용법(간단하게!)
## 가상환경(그냥 간단하게 해버리는 법)
```pip install -r requirements.txt```
## 가상환경(정석적으로 poetry 사용하는 법)
### 먼저, poetry를 설치해야 합니다.(만약, 안되면 구글링하면 금방 찾을 수 있습니다)
```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python```
### 그 후에는 이 명령어를 사용합니다. (이 명령어는 터미널 연결 시 마다 사용하게 될겁니다.)
```export PATH="$HOME/.poetry/bin:$PATH"```
### poetry 명령어가 작동하는 지 확인합니다.
### 작동이 된다면, 현재 폴더에 poetry.lock 및 pyproject.toml이 존재하는 지 확인합니다.
### 확인 이후 다음과 같이 진행합니다.
```poetry install```
### 정상적이라면, 가상환경 .venv 폴더가 생성되며, 해당 환경에 필요한 패키지들이 생성됩니다.
### 설치 완료 후, 다음과 같은 명령어를 통해 가상환경을 활성화합니다.
```export PATH="$HOME/.poetry/bin:$PATH"```

```source $(poetry env info --path)/bin/activate```
### 이 명령어는 터미널 연결 시마다 사용해주시면 편리하게 활성화됩니다.
#
# Pipeline
## transformers의 TextClassificationPipeline을 상속받아서 커스텀하였습니다. 그 결과 노래 감성 분석에 사용 가능한 SongPipeline이 탄생했습니다.
### 기존의 맨 앞에서 512글자를 자르고 TextClassificationPipeline을 사용하던 방식과 SongPipeline을 사용한 방식을 비교하였습니다.
### 해당 결과는 temp.ipynb에서 확인할 수 있습니다.