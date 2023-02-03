# drf-boilerplate

drf(django restframework) 로 프로젝트를 시작하기 위한 보일러플레이트

## 구현 돼있는 기능

### 공통

- [ ] model
- [ ] serializer
- [ ] views

### 인증/인가 (jwt 방식)

- [ ] custom user model
- [ ] local login
- [ ] social login (OAuth 2.0 authorization)
  - [ ] naver
  - [ ] kakao
  - [ ] google

### 테스트

- [x] unit test

### CI/CD

- [ ] settings.py 분리
- [x] dockerfile
- [x] docker-compose
- [ ] github action (CI/CD)
  - [x] test
  - [x] linting
  - [ ] deploy
