class CollegeInfo(object):
    def __init__(self):
        self.student_name = '小明'
        self.student_age = 20
        self.student_salary = 3000
        pass

    def choose_colledge_by_age(self, student_age=None):
        student_age = student_age if student_age else self.student_age
        return '北大' if student_age > 30 else '清华'

    def query_salary(self, student_salary=None):
        student_salary = student_salary if student_salary else self.student_salary
        return '土豪' if student_salary > 4000 else '傻逼'


college_info = CollegeInfo()

if __name__ == '__main__':
    pass
