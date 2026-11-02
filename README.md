# Linux Security Auditor

## 프로젝트 소개
Linux 보안 상태를 읽기 전용으로 점검하는 Python 도구

## 주요 기능
UID 0 계정 검사, NORMAL/REVIEW/ERROR 판정, 점검 근거 출력

## 개발 환경
Ubuntu 24.04 LTS, Python 3.12

## 실행 방법

## 테스트
수동 테스트 수행, unittest 2개 통과 확인

## 점검 범위와 한계
한계: 현재 /etc/passwd 형식 파일 기반 점검이며 외부 계정 저장소는 검사하지 않음

## 향후 개발 계획
테스트 확장, 파일 소유자·권한 점검, JSON/Markdown 보고서