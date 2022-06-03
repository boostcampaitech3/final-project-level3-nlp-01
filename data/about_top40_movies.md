# top40 movies by score
- 평점 기반으로 rank된 영화(총 40편)입니다.
특정 날짜를 기준으로 rank되었습니다.

- huggingface의 dataset 형식으로 저장했습니다. 

- `! pip install datasets`
`from datasets import load_from_disk`
`dataset = load_from_disk({top40_movies_by_score의 경로})`
위 순서로 dataset을 변수로 가져올 수 있습니다.

- (변환은 자유지만 저는 DataFrame 형식을 선호합니다.)