# netflixproject
# 1. 프로젝트 주제
### 1) 프로젝트명 : NetNote

### 2) 상세 설명

넷플릭스에서 제공하는 콘텐츠 감상 후 기록하여 다른 사용자들과 공유하는 커뮤니티 서비스

# 2. 페이지별 와이어프레임

### 1) 첫 페이지

![image](https://user-images.githubusercontent.com/98968060/162932670-be9ca5ac-33ac-4340-9086-d2c813e7027e.png)

구현해야 하는 기능

- 사이트의 첫 화면
- 미리보기 클릭 시, 메인 페이지로 이동
- 회원가입 클릭 시, 회원가입 페이지로 이동
- 로그인 클릭 시, 로그인 페이지로 이동

### 2) 회원가입 페이지

![image](https://user-images.githubusercontent.com/98968060/162932724-e1bf9a83-f02a-4057-ae32-3fcbdf10341e.png)

구현해야 하는 기능

- 아이디 중복 확인
    - 중복이 아닌 경우, “사용할 수 있는 아이디입니다” 출력
    - 중복인 경우, “사용할 수 없는 아이디입니다” 출력
- 비밀번호와 비밀번호 확인 일치 여부 확인
    - 일치하지 않는 경우, “비밀번호가 일치 하지 않습니다” 출력
- 비밀번호를 암호화 하기 위해 해시 함수 사용
- 회원가입 버튼 클릭 시, 아이디와 비밀번호 DB에 저장 후 로그인 페이지로 이동

### 3) 로그인 페이지

![image](https://user-images.githubusercontent.com/98968060/162932819-9ea43a0e-43d3-4808-8b8e-df4a594e79d9.png)

구현해야 하는 기능

- 로고 클릭 시, 첫 페이지로 이동
- 로그인 클릭 시, 메인 페이지로 이동
- 입력 받은 PW값을 다시 해시 값으로 변환 후, DB에 저장된 사용자 정보 조회
    - ID, PW 조회 정보가 없는 경우
        
        Alert창 (”아이디 혹은 비밀번호를 다시 확인해주세요”) 출력
        
    - ID, PW 조회 정보가 있는 경우
        - JWT 토큰 발급
        - 토큰 값을 쿠키에 저장
- 회원가입 클릭 시, 회원가입 페이지로 이동

### 4) 메인 페이지

![image](https://user-images.githubusercontent.com/98968060/162932902-e2277a2b-f341-4b30-9342-1c143a9ffbc0.png)

구현해야 하는 기능

- 로그인이 되어 있지 않는 경우, 우측 상단에 로그인, 회원가입 버튼 보이게 구현
- 로그인이 되어 있는 경우, 우측 상단에 기록하기, 마이페이지, 로그아웃 버튼 보이게 구현
    - 기록하기 버튼 클릭 시, 모달창에서 URL 주소값을 받은 후 기록하기 페이지로 이동
    
    ![image](https://user-images.githubusercontent.com/98968060/162933003-eb82f413-7545-4cc5-a4cb-63bc545626cd.png)

    
    - 마이페이지 버튼 클릭 시, 마이페이지 페이지로 이동
    - 로그아웃 버튼 클릭 시, 쿠키 삭제
- 로고 클릭 시, 메인 페이지 이동
- 공유 카드 클릭 시, 뷰 페이지로 이동

### 5) 기록하기 페이지

![image](https://user-images.githubusercontent.com/98968060/162933059-9e0f6d18-6d4f-4413-8f09-3ef206193de3.png)


구현해야 하는 기능

- 크롤링 해서 포스터, 제목, 감독의 input 값 출력
- 날짜, 함께 본 사람, 메모는 사용자가 직접 입력
- 마우스 오버 시, 별점 선택(1~5)
- 저장하기 버튼 클릭 시
    
    Alert창 (”저장되었습니다”) 출력 후 메인 페이지로 이동
    

### 6) 뷰 페이지

![image](https://user-images.githubusercontent.com/98968060/162933140-946ddb3c-792a-4227-bc29-6ca4fb01c8da.png)

구현해야 하는 기능

- DB에 저장된 값을 가져와 뷰 페이지에서 보여줌

# 3. API 설계

| 기능 | method | url | request | response |
| --- | --- | --- | --- | --- |
| 첫페이지 |  | /netnote/ | - |  |
| 로그인 | post | /netnote/login | {’id’ :id, ‘pw’:pw} | 로그인 완료! |
| 회원가입: 사용자 정보 저장 | post | /netnote/sign_up | {’id’ :id, ‘pw’:pw} | 가입 완료! |
| 회원가입: 아이디 중복 조회 | get | /netnote/chkid | {’id’ :id} | 아이디 중복 조회 여부 |
| 로그아웃 | get | /netnote/logout | {’id’ :id} | 로그아웃 |
| 메인: 기록 조회 | get | /netnote/main | {’img’:img, ‘title’:title} | 메인_기록 보여주기 |
| 메인: URL 저장 | post | /netnote/geturl | {’url’:url} | URL 주소 저장 |
| 기록: 기록 저장 | get, post | /netnote/write | {’img’:img, ‘title’:title, ‘director’:dirctor, ‘date’:date,  ‘together’:together, ‘memo’:memo, ‘star’:star} | 기록 작성 |
| 뷰: 기록정보 불러오기 | get | /netnote/view | {’img’:img, ‘title’:title, ‘director’:dirctor, ‘date’:date, ‘together’:together, ‘memo’:memo, ‘star’:star} | 기록 보여주기 |
