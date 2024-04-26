# 공공데이터 공모전 API Server

## 사전 설치

### Docker

> https://www.docker.com/products/docker-desktop/

###

## 실행법

1. 프로젝트 최상위에 `secrets-api-key.json`을 넣는다.

2. [run-server.sh](./run-server.sh) 를 실행한다. `$ ./run-server.sh`

3. 확인
    * Docker Desktop 의 Dashboard에서 Container를 확인한다.
    * `localhost:8000/admin` 에 접속해본다.

###

## 랜드마크 데이터 추가
1. 서버 키기 `python3 manage.py runserver`
2. http://127.0.0.1:8000/test/landmark 로 접속 -> 데이터를 로컬 DB에 적재

## swagger 켜기
1. http://127.0.0.1:8000/swagger/

-> 안되면 연락!!

