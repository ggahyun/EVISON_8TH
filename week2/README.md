<Login_project에 있는 SQL Injection이 발생하는 부분을 어떻게 패치했는가?>
(1) $sql = "SELECT * FROM users WHERE username = '$username' AND password='$password'";

취약점 설명: 입력받은 username과 password가 일치하는 사용자를 찾는 부분은 사용자 입력을 그대로 SQL에 붙여서 실행하므로 SQL Injection 취약점이 있는 부분이다. 

공격 방법: username에 admin' OR 1=1 -- 을 입력하거나 admin' -- 을 입력하면 주석 처리로 인해 비밀번호 검증을 안 한다.

보안 개선: preapre() + bind_param() 사용
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
if ($stmt === false) {
    //prepare 실패 처리
    error_log("Prepare failed: " . $conn->error);
    die("서버 오류가 발생했습니다.");
}
$stmt->bind_param("ss", $username, $password);

Prepared statement인 prepare() + bind_param()을 사용해 쿼리를 파라미터화하면 입력값이 SQL 구문으로 해석되지 않고, 값으로 안전하게 바인딩(특정 값에 연결되어 더 이상 변경되지 않는 상태)되어 SQL Injection을 차단한다.
bind_param()으로 type(문자열, 정수 등)을 명시할 수 있어서 바이너리나 숫자 처리에 안전하다.

(2)$result=$conn->query($sql);

취약점 설명: $conn->query($sql)는 문자열로 완성된 SQL을 한 번에 서버로 보내서 입력을 이어 붙이면 SQL Injection에 취약하다. 문자열을 이어 붙이면 공격자가 ' OR 1=1을 넣어 쿼리를 변형할 수 있기  때문이다.

보안 개선: 
$exec_ok = $stmt->execute();
if ($exec_ok === false) {
    error_log("Execute failed: " .  $stmt->error);
    die("서버 오류가 발생했습니다.");
}
$result = $stmt->get_result();

$stmt->execute();와 $result = $stmt->get_result();는 준비된 쿼리(Prepared Statement)를 쓰는 방식으로, SQL과 값을 분리해서 보내기 때문에 SQL Injection을 방지한다.

(3) 결과 확인 부분
취약점 설명: 사용자 이름 출력 시 스크립트 실행(XSS)가 실행될 수 있다.

보안 개선:  
$safe_name = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');
htmlspecialchars()로 출력값 이스케이프를 통해 XSS를 방지한다.


***
SQL Injection
- 서버(DB)를 공격하는 것
- 방법:사용자 입력을 검증하지 않고 SQL 쿼리에 그대로 붙이면, 공격자가 SQL 문법을 조작할 수 있음
- 예시: SELECT * FROM users WHERE username = 'admin' -- ' AND password=''

XSS(Cross-Site Scripting)
- 사용자 브라우저(클라이언트)를 공격하는 것
- 방법: 사용자 입력을 HTML로 출력할 때 필터링 없이 <script> 같은 태그가 실행됨
- 예시: <input value="<script>alert('해킹');</script>">