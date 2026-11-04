# Linux Security Auditor

## 프로젝트 소개
Linux 보안 상태를 읽기 전용으로 점검하는 Python 도구

## 주요 기능
UID 0 계정 검사, NORMAL/REVIEW/ERROR 판정, 점검 근거 출력

## 개발 환경
Ubuntu 24.04 LTS, Python 3.12

### UID 입력 검증
- UID는 ASCII 숫자(0-9)만 허용합니다.
- 음수, 부호, 공백, 비ASCII 숫자를 거부합니다.
- 입력 형식 오류는 정상으로 처리하지 않고 ERROR로 판정합니다.

## 실행 방법

## 테스트
Python 표준 라이브러리 unittest를 사용합니다.

실행 명령:

python3 -m unittest discover -v

검증 결과 (2026-11-04):
- 5개 테스트 메서드 통과
- 비ASCII UID 입력 검증 보완
- 기존 테스트 회귀 검증 통과

## 점검 범위와 한계
한계: 현재 /etc/passwd 형식 파일 기반 점검이며 외부 계정 저장소는 검사하지 않음

## 향후 개발 계획
테스트 확장, 파일 소유자·권한 점검, JSON/Markdown 보고서