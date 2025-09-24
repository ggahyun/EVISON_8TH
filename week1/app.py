from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

guestbook = [] #서버에 저장되는 방명록을 위해 간단한 데이터베이스인 리스트 사용, 전역 번수로 미리 선언된 guestbook

@app.route('/')
def home(): #메인 페이지: 검색 폼 + 방명록 작성 폼 + 모든 방명록 출력

    #Flask가 index.html을 읽고 문자열로 생성해서 HTTP 응답으로 돌려주는 함수
    return render_template('index.html', guestbook=guestbook) #파이썬 변수(오)을 템플릿에 guestbook(왼)이라는 이름으로 넘긴다는 뜻
    
@app.route('/search') #검색 기능: 검색 결과 출력, 이 부분이 Reflected XSS가 구현된 위치
def search():
    query = request.args.get('q', '') #검색어 가져오기, q 파라미터를 escape하지 않고 그대로 출력
    return f"검색 결과: {query}" #입력받은 query 값을 아무런 처리없이 그대로 HTML에 포함시켜 반환
    #return f"검색 결과: {escape(query)}" 이렇게 하면 escape 가능
    #renturn render_template('search.html', query=query) 이렇게 하고 search.html 템플릿에서 query를 |sage로 출력하면 escape 안 하는 코드

@app.route('/write', methods=['GET', 'POST']) #/write 경로로 들어오는 HTTP 요청을 처리: GET 요청(폼을 보여줄 때)과 POST 요청(폼에서 보낸 데이터를 서버가 받을 때)을 받음
def write(): #/write 경로로 요청이 왔을 때 실행되는 함수
    if request.method == 'POST': #요청의 HTTP 메서드가 POST면(POST면 폼 데이터를 저장, GET이면 작성 폼을 보여줌)
        name = request.form.get('name', '익명') #request.form에서 'name' 필드 값을 가져옴. name이 없으면 기본값으로 '익명'을 사용
        message = request.form.get('message', '') #message가 없을 때 기본값으로 빈 문자열 ''사용
        #출력 시 escape 하지 않고 HTML그대로 출력->Stored XSS 취약함

        guestbook.append({'name': name, 'message': message}) #geustbook이라는 리스트에 딕셔너리 항목 추가
        return redirect(url_for('home')) #home함수(메인페이지)로 리디렉션, POST-Redirect-Get 패턴으로 POST 재전송 방지(중복 등록 방지)
    
    return render_template('index.html') #GET 요청이라면 작성 폼을 보여주기 위해 indext.html 템플릿(작성 폼이 포함되어 있어야 함)을 렌더링해서 반환.

if __name__ == '__main__': #이 파일을 직접 실행하면 서버 실행
    app.run(debug=True) #디버그 모드 활성화