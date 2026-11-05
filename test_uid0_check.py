from cgitb import reset
from email import message
import unittest
from uid0_check import evaluate_uid0

import tempfile
from pathlib import Path

from uid0_check import check_passwd_file


class TestEvaluateUID0(unittest.TestCase):

    # 정상적인 root 계정만 존재할 때 NORMAL 반환 테스트
    def test_normal_root(self):
        lines = [
            "root:x:0:0:root:/root:/bin/bash",
            "user:x:1000:1000:User:/home/user:/bin/bash"
        ]

        result = evaluate_uid0(lines)

       # self.assertEqual(실제값, 기대값)
        self.assertEqual(result["status"], "NORMAL")
        self.assertEqual(result["accounts"], [(1, "root")])


    # UID 0 계정이 여러 개 존재할 때 REVIEW 반환 테스트
    def test_extra_uid0(self):
        lines = [
            "root:x:0:0:root:/root:/bin/bash",
            "admin:x:0:1000:Admin:/home/admin:/bin/bash"
        ]

        result = evaluate_uid0(lines)

        # TODO 1: status가 REVIEW인지 확인
        self.assertEqual(result["status"], "REVIEW")
        # TODO 2: accounts에 root와 admin이 모두 있는지 확인
        # self.assertIn(찾을_값, 검사할_목록)
        # username = [username for line_number, username in result["accounts"]]
        # self.assertIn("root", username)
        # self.assertIn("admin", username)
        self.assertEqual(
            result["accounts"],
            [(1, "root"), (2, "admin")]
        )

        # TODO 3: evidence에 판정 근거가 기록되었는지 확인
        # self.assertIn("root 외 UID 0 계정이 존재합니다", result["evidence"])
        self.assertTrue(
            any(
                "root 외 UID 0" in message
                for message in result["evidence"]
            )
        )

    # UID가 숫자가 아닌 경우 ERROR 반환 테스트
    def test_invalid_uid_returns_error(self):
        lines = [
            "root:x:0:0:root:/root:/bin/bash",
            "admin:x:abc:1000:Admin:/home/admin:/bin/bash"
        ]

        result = evaluate_uid0(lines)

        self.assertEqual(result["status"], "ERROR")
        self.assertEqual(result["accounts"], [])
        self.assertTrue(
            any(
                "UID가 올바르지" in message
                for message in result["evidence"]
            )
        )

    # ASCII UID 검증 테스트
    def test_non_ascii_uid_returns_error(self):
        lines = [
            "root:x:٠:0:root:/root:/bin/bash"
        ]

        result = evaluate_uid0(lines)

        # TODO 1: status가 ERROR인지 확인
        self.assertEqual(result["status"], "ERROR")
        # TODO 2: accounts가 빈 리스트인지 확인
        self.assertEqual(result["accounts"], [])
        # TODO 3: evidence가 리스트인지 확인
        self.assertIsInstance(result["evidence"], list)
        # TODO 4: evidence에 UID 형식 오류가 기록됐는지 확인
        self.assertTrue(
            any(
                "UID가 올바르지" in message
                for message in result["evidence"]
            )
        )

    # UID 경계값 검증 테스트(subTest 활용)
    def test_invalid_uid_boundaries(self):
        invalid_uids = [
            "-1",
            "+0",
            " 0",
            "",
            "１２"
        ]

        for uid in invalid_uids:
            with self.subTest(uid=uid):
                lines = [
                    f"root:x:{uid}:0:root:/root:/bin/bash"
                ]

                result = evaluate_uid0(lines)

                # TODO 1: status가 ERROR인지 확인
                self.assertEqual(result["status"], "ERROR")

                # TODO 2: accounts가 빈 리스트인지 확인
                self.assertEqual(result["accounts"], [])

                # TODO 3: evidence에 UID 오류 근거가 있는지 확인
                self.assertTrue(
                    any(
                        "UID가 올바르지" in message
                        for message in result["evidence"]
                    )
                )


class TestCheckPasswdFile(unittest.TestCase):

    # 파일이 존재하지 않을 때 ERROR 반환 테스트
    def test_missing_file_returns_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing_passwd.txt"

            result = check_passwd_file(str(path))

            # TODO 1: status가 ERROR인지 검증
            self.assertEqual(result["status"], "ERROR")

            # TODO 2: accounts가 []인지 검증
            self.assertEqual(result["accounts"], [])

            # TODO 3: evidence에 파일 읽기 실패 근거가
            # 있는지 검증
            self.assertTrue(
                any(
                    "파일 읽기 실패" in message
                    for message in result["evidence"]
                )
            )

    # 파일이 비어있을 때 ERROR 반환 테스트
    def test_empty_file_returns_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty_passwd.txt"

            # TODO 1: 크기가 0바이트인 빈 파일 생성
            path.touch()

            # TODO 2: check_passwd_file() 실행
            result = check_passwd_file(str(path))

            # TODO 3: status가 ERROR인지 확인
            self.assertEqual(result["status"], "ERROR")

            # TODO 4: accounts가 []인지 확인
            self.assertEqual(result["accounts"], [])

            # TODO 5: evidence에 빈 입력 근거가 있는지 확인
            self.assertTrue(
                any(
                    "데이터가 비어" in message
                    for message in result["evidence"]
                )
            )