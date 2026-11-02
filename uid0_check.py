def parse_passwd_line(line: str) -> tuple[str, int]:
    # TODO 1: ':'를 기준으로 필드 분리
    parts = line.split(':')
    # TODO 2: 필드 수가 7개인지 확인
    if len(parts) == 7 :
    # TODO 3: 사용자명과 UID 추출
    # 빈 사용자명 필터링
        username = parts[0]
        if username == "":
            raise ValueError("사용자명이 비어있습니다.")
        uid = parts[2]
    # TODO 4: UID를 정수로 변환하고 검증
        if uid.isdecimal() :
           return (username, int(uid))
        else :
            raise ValueError(f"UID가 올바르지 않습니다. 현재 UID :{uid}")
    # TODO 5: (사용자명, UID) 반환

    else :
        raise ValueError(f"passwd 필드 수가 7개가 아닙니다. 현재 필드 수:{len(parts)}")


def analyze_passwd(lines: list[str]) -> list[tuple[int, str]]:
    # TODO 1: UID 0 계정을 저장할 리스트 생성
    uid0_list = []
    # TODO 2: enumerate()로 각 줄과 행 번호 확인
    for line_number, line in enumerate(lines, start=1):
    # TODO 3: 기존 parse_passwd_line() 호출
        username, uid = parse_passwd_line(line)

    # TODO 4: UID가 0이면 행 번호와 사용자명 저장
        if uid == 0 :
            uid0_list.append((line_number, username))

    # TODO 5: 결과 리스트 반환
    return uid0_list


def evaluate_uid0(lines: list[str]) -> dict:
    status=""
    evidence=[]
    accounts=[]
    root_total_count=0
    root_count=0
    other_count = 0
    # TODO 1: 빈 입력인지 확인
    if lines :

    # TODO 2: 모든 행을 검증하고 UID 0 계정 수집
    # 기존 함수 재사용
        try:
            # line 전체에서 root계정 개수 검증
            for line in lines:
                username, uid = parse_passwd_line(line)
                if username == "root":
                    root_total_count+=1

            accounts = analyze_passwd(lines)
            # TODO 3: root 계정의 존재 여부, UID, 중복 확인

            for line_number, username in accounts :
                if username == "root":
                    root_count+=1
                else:
                    other_count+=1

            # TODO 4: NORMAL / REVIEW / ERROR 판정
            if root_total_count==1 and root_count==1 and other_count==0:
                status = "NORMAL"
                evidence.append("root 계정 1개이며 다른 UID 0 계정이 없습니다.")
            else:
                status = "REVIEW"
                if root_total_count>1:
                    evidence.append("root 계정이 중복됩니다")
                if root_total_count==0:
                    evidence.append("root 계정이 없습니다")
                elif root_count==0:
                    evidence.append("root 계정의 UID가 0이 아닙니다")
                if other_count>0:
                    evidence.append("root 외 UID 0 계정이 존재합니다")


        except ValueError as e:
            status = "ERROR"
            evidence = [f"파싱 실패: {e}"]
    else:
        status = "ERROR"
        evidence = ["입력 데이터가 비어있습니다."]
    # TODO 5: status, accounts, evidence 반환
    return {"status":status,"accounts":accounts, "evidence":evidence}



# lines = [
#     "root:x:1:0:root:/root:/bin/bash",
#     "root:x:2:0:root:/root:/bin/bash"
# ]

# print(evaluate_uid0(lines))


def check_passwd_file(path: str) -> dict:
    result = {
        "status" : "ERROR",
        "accounts" : [],
        "evidence" : []
    }
    try:
    # TODO 1: 파일을 읽기 전용으로 열기
        with open(path, "r", encoding="utf-8") as f:

            # TODO 2: 파일 내용을 줄 단위로 분리하기
            lines = f.read().splitlines()

        # TODO 3: evaluate_uid0(lines) 호출하기
        result = evaluate_uid0(lines)

        # TODO 4: 파일 읽기 실패를 ERROR로 처리하기
    except PermissionError as e:
        result["evidence"].append(f"파일 읽기 실패: {e}")
    except UnicodeError as e:
        result["evidence"].append(f"파일 읽기 실패: {e}")
    except OSError as e:
        result["evidence"].append(f"파일 읽기 실패: {e}")

    return result

if __name__ == "__main__":
    # 기존 임시 테스트 코드를 여기에 배치치
    print(check_passwd_file("samples/passwd_normal.txt"))
    print(check_passwd_file("samples/passwd_empty.txt"))