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

## 테스트

Python 표준 라이브러리 `unittest`를 사용하여 UID 0 계정 점검 기능을 검증합니다.

### 실행 방법

```bash
python3 -m unittest discover -v
```

### 주요 검증 항목

- 정상 root 계정 및 추가 UID 0 계정 판정
- 잘못된 UID 및 비ASCII 숫자 입력 처리
- UID 경계 조건 검증 (음수, 부호, 공백, 빈 값 등)
- 존재하지 않는 파일과 빈 파일 처리
- 정상 passwd 샘플 파일 읽기 및 판정

### 검증 결과

**2026-11-05 기준: unittest 8개 테스트 메서드 전체 통과**

기존 테스트를 포함한 전체 회귀 테스트를 수행했습니다.

※ `subTest()`로 검증하는 여러 경계 입력은 하나의 테스트 메서드로 집계됩니다.

## 점검 범위와 한계
한계: 현재 /etc/passwd 형식 파일 기반 점검이며 외부 계정 저장소는 검사하지 않음

## 향후 개발 계획
테스트 확장, 파일 소유자·권한 점검, JSON/Markdown 보고서