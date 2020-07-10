import unittest
import requests
import parameterized
import json

question_id_list1 = ["1", "2", "3"]
question_id_list2 = ["5", "4"]


class TestDuplicated(unittest.TestCase):  # 假设get获取的数据中不包含当前题目的id，仅显示重复题的id
    @parameterized.parameterized.expand(question_id_list1)
    def test_get(self, question_id):
        url = f'http://192.168.1.204:1234/duplicated-questions/{question_id}/'
        res = requests.get(url=url)
        res_dict = json.loads(res)
        question_id_list1.remove(question_id)  # 删除本题对应的id
        if res_dict["duplicated_with"].sort() == question_id_list1.sort():  # 判断剩余的列表内容是否和返回值相同
            self.assertIn('get接口测试通过')
        else:
            self.assertIn('get接口测试不通过')

    def test_put(self):  # 假设PUT传当前题目id，数据中携带重复题的id列表
        question_id = 2
        url = f'http://192.168.1.204:1234/duplicated-questions/{question_id}/'
        data = {
            'duplicated_with': ["6", "7"]
        }
        res_put = requests.put(url=url, data=data)
        res_get = requests.get(url=url)
        res_get_dict = json.loads(res_get)
        if res_get_dict["duplicated_with"].sort() == ["2", "6", "7"]:
            self.assertIn('put接口测试通过')
        else:
            self.assertIn('put接口测试不通过')

    def test_post(self):  # 假设POST传当前题目id，数据中携带重复题的id
        question_id = 2
        url = f'http://192.168.1.204:1234/duplicated-questions/{question_id}/'
        data = {
            'duplicated_with': ["8"]
        }
        res_post = requests.post(url=url, data=data)
        res_get = requests.get(url=url)
        res_get_dict = json.loads(res_get)
        if '8' in res_get_dict["duplicated_with"]:
            self.assertIn('post接口测试通过')
        else:
            self.assertIn('post接口测试不通过')

    def test_delete(self):  # 使用question_id_list2 = ["5", "4"]测试delete接口
        question_id = 4
        url = f'http://192.168.1.204:1234/duplicated-questions/{question_id}/'
        res = requests.delete(url=url)  # 删除id=4的重复题
        res2 = requests.get(url=url)  # 查看id=4的重复题，列表应为["4"]
        res2_dict = json.loads(res2)

        question_id = 5
        url = f'http://192.168.1.204:1234/duplicated-questions/{question_id}/'
        res3 = requests.get(url=url)  # 查看id=5的重复题，列表应为["5"]
        res3_dict = json.loads(res3)
        if res2_dict["duplicated_with"] == 4 & res3_dict["duplicated_with"] == 5:  # 两个列表若有一个不正确则不通过
            self.assertIn('delete接口测试通过')
        else:
            self.assertIn('delete接口测试不通过')


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(TestDuplicated('test_get'), TestDuplicated('test_put'), TestDuplicated('test_post'), TestDuplicated('test_delete'))
    unittest.TextTestRunner(verbosity=2).run(suite)

