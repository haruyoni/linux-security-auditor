from email import message
import unittest
from uid0_check import evaluate_uid0


class TestEvaluateUID0(unittest.TestCase):

    def test_normal_root(self):
        lines = [
            "root:x:0:0:root:/root:/bin/bash",
            "user:x:1000:1000:User:/home/user:/bin/bash"
        ]

        result = evaluate_uid0(lines)

       # self.assertEqual(실제값, 기대값)
        self.assertEqual(result["status"], "NORMAL")
        self.assertEqual(result["accounts"], [(1, "root")])


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