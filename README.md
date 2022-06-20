# Humans of 42 
42서울 주변의 사람들을 인터뷰하는 채널입니다.
[humansof42.com](https://humansof42.com)에서 배포된 웹사이트를 만나볼 수 있습니다.

### server migration
- buy a new server
- set development settings
- dump postgresql DB
- update collections with python 3.10
- install gunicorn and set gunicorn.socket & gunicorn.service
- update nginx settings
- install certbot but it does not support python 3.10....


### Technologies
- Python
- Django
- Django REST framework
- Bootstrap
- Postgresql
- Oauth 2.0
- Summernote
- GCP Compute Engine -> Vultr로 서버 이전 예정
- nginx, gunicorn


### Features
- User
  - 42API로 회원가입/로그인
  - 42API로 가입한 회원에 한해 이메일과 패스워드로 로그인
  
- Interview
  - 인터뷰 생성, 보기, 수정, 삭제(only admin)
 
- Comment
  - 댓글 생성, 보기, 삭제(only login user)
 
- Like
  - 공감 버튼(only login user)

- 카카오톡으로 공유하기
