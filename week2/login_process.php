<?php 
//db 연결 
$db_host="localhost"; 
$db_user = "root"; 
$db_pass=""; 
$db_name="my_db"; 
$db_port = 3306; 
$conn=new mysqli($db_host, $db_user, $db_pass, $db_name, $db_port);

if($conn->connect_error){
    die("데이터베이스 연결 실패: " . $conn->connect_error); // connect_error로 수정
}

//login.html에서 POST 방식으로 보낸 데이터 받기 
$username=$_POST['username']; 
$password=$_POST['password'];

// SQL 쿼리 작성(입력받은 username과 password가 일치하는 사용자 찾기) 
// SQL Injection 취약점이 있는 부분: $sql = "SELECT * FROM users WHERE username = '$username' AND password='$password'"; 

//Prepared Statement를 사용해서 SQL Injection 차단
$stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
if ($stmt === false) {
    //prepare 실패 처리
    error_log("Prepare failed: " . $conn->error);
    die("서버 오류가 발생했습니다.");
}
$stmt->bind_param("ss", $username, $password);

// 쿼리 실행 
// 문자열 $sql을 직접 DB로 보냄. 사용자 입력을 그대로 붙이면 SQL 인젝션 위험함: $result=$conn->query($sql);

$exec_ok = $stmt->execute();
if ($exec_ok === false) {
    error_log("Execute failed: " .  $stmt->error);
    die("서버 오류가 발생했습니다.");
}

// 결과 가져오기 (mysqlnd 드라이버가 필요)
$result = $stmt->get_result(); //mysqli_result 객체

// 결과 확인 
if($result->num_rows > 0){ // num_rows로 수정
    //일치하는 사용자가 있으면(결과 행이 1개 이상이면)
    //출력 시 XSS 방지
    $safe_name = htmlspecialchars($username, ENT_QUOTES, 'UTF-8');
    echo "<h1>로그인 성공!</h1>";
    echo "<p>'$safe_name'님, 환영합니다.</p>";
}else{
    echo "<h1>로그인 실패</h1>";
    echo "<p>아이디 또는 비밀번호가 올바르지 않습니다.</p>";
    echo '<a href="login.html">다시 시도하기</a>';
}

//DB 연결 종료 
$stmt->close();
$conn->close(); 
?>