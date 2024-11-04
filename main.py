import requests
import json
import time
from datetime import datetime
import requests
from auto_cookie import get_cookie
import winsound
import sys
studentAssoc = 0 #学生ID
courseSelectTurnAssoc = 0 #学期ID
lessonAssoc = 0 #课程ID




url = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/add-predicate' #预-请求网址
url_request = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/add-request' #请求网址
url_predicate_response_orgin = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/predicate-response/'  #预-请求验证网址
url_add_drop_response_orgin = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/add-drop-response/'  #请求验证网址
url_get_stuID ='https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/students' #获取学生ID网址
url_OpenTurns = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/open-turns/' #获取学期ID网址
url_Lesson = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/query-lesson/' #获取课程ID网址
url_select = 'https://jwxt.nufe.edu.cn/course-selection-api/api/v1/student/course-select/' #获取所有课程网址
data = {
    "studentAssoc": 0,
    "courseSelectTurnAssoc": 0,
    "requestMiddleDtos": [
        {
            "lessonAssoc": 0,
            "virtualCost": 0 #应该是识别码，0代表预先请求
        }
    ],
    "coursePackAssoc": None
}
data_request = {
    "studentAssoc": 0,
    "courseSelectTurnAssoc": 0,
    "requestMiddleDtos": [
        {
            "lessonAssoc": 0,
            "virtualCost": None #应该是识别码，None代表请求
        }
    ],
    "coursePackAssoc": None
}

#协议请求头 只用寻找 Authorization
headers = {
    # 'Accept': 'application/json, text/plain, */*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': '',
    # 'Content-Length': '134',
    # 'Content-Type': 'application/json',
    # 'Cookie': 'cs-course-select-student-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzdXB3aXNkb20iLCJleHAiOjE3MjU5MDAyMDgsInVzZXJuYW1lIjoiMjEyMDIzMTM0MiJ9.lYL-TsLjDi9nkDfoE0_v4ij503j9XKDk_pMs5urfZK0',
    # 'Origin': 'https://jwxt.nufe.edu.cn',
    # 'Referer': 'https://jwxt.nufe.edu.cn/course-selection/',
    # 'Sec-Ch-Ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36 Core/1.116.438.400 QQBrowser/13.0.6071.400'
}


#   请求体



# response = requests.post(url, headers=headers, json=data)
# response_json = response.json()

# # # 提取result字段
# # result = response_json.get("result")

# # # 检查result是否等于0
# # if result == 0:
# #     print("Result is 0")
# # else:
# #     print("Result is not 0")
# print(response.status_code)
# print(response.text)

#   预请求验证
def check_predicate(response_data):
    response = requests.get(url_predicate_response_orgin+response_data, headers=headers, json=data)
    response_json = response.json()
    if response_json.get("data") == None:
        print(response_json.get("message"))
        print("预选课程数据发送失败(data数据异常)")

        return False
    
    response_lessonAssoc = response_json.get("data").get("result").get(str(lessonAssoc)) #获取json返回格式的数据
        

    if response_lessonAssoc == None:
        print("预选课程数据发送成功")
        return True

    else:
        
        if response_lessonAssoc.get("text") == "相同教学班只能选一次":
            print("该课程已选，请打开查看已选课程")
            

        else:
            print("预选课程数据发送失败")
            print(response_lessonAssoc.get("text"))

        return False
    
# 请求验证
def check_request(response_data):
    response = requests.get(url_add_drop_response_orgin+response_data, headers=headers, json=data)
    response_json = response.json()
    if response_json.get("data") == None:
        print(response_json.get("message"))

        return False
    response_success = response_json.get("data").get("success")

    if response_success:

        return True
    else:
        print(response_json.get("data").get("errorMessage"))
        return False
#主函数
def main():
    i=0 #计数器

    now = datetime.now() #加上准点时间验证

    while True:
        if now.hour == predict_Time.hour and now.minute == predict_Time.minute and now.second ==predict_Time.second:
            while True:
                try:
                    
                    response = requests.post(url, headers=headers, json=data)
                    if(response.status_code == 500):

                        print("用户数据获取失败，请检查网络连接")
                        winsound.Beep(1000, 500)  # 1000Hz的频率，500毫秒的持续时间
                        return False
                    response_json = response.json()
                    response_data = response_json.get("data")
                    if check_predicate(response_data):
                    
                    # 如果预-请求响应成功，执行正请求
                        response_request = requests.post(url_request, headers=headers, json=data_request)
                        response_request_json = response_request.json()
                        response_request_data = response_request_json.get("data")
                        # print(f"Status Code: {response.status_code}")
                        # print(f"Response: {response.text}")
                        if check_request(response_request_data):
                            winsound.Beep(1000, 500)  # 1000Hz的频率，500毫秒的持续时间
                            winsound.Beep(1000, 500)  # 1000Hz的频率，500毫秒的持续时间
                            

                            print(f"选课成功,课程ID：{lessonAssoc},课程名称:{target_name}")
                            time.sleep(100000)
                            return True
                except requests.exceptions.ConnectionError as e:
                    print(f"Connection error: {e}. [error id]=1")

                    
                except requests.exceptions.Timeout:
                    print("Request timed out. [error id]=2")

                except requests.RequestException as e:
                # 捕获所有请求异常（包括连接错误、超时等）
                    print(f"Request exception: {e}. [error id]=3")
                i=i+1
                print(f"选课失败，正在尝试第{i}次")
        print(f"距离抢课开始还有{predict_Time - now}")
        # print(f"距离抢课开始还有：{-now.hour+predict_Time.hour}小时{-now.minute+predict_Time.minute}分钟{-now.second+predict_Time.second}秒")
        now = datetime.now()

class Login_Data:

    def __init__(self, username, password,target_teacher_name,target_name,target_courseCode,predict_Time):
        self.username = username
        self.password = password
        self.target_teacher_name = target_teacher_name
        self.target_name = target_name
        self.target_courseCode = target_courseCode
        self.predict_Time = predict_Time


def DataInput():
    username = input("请输入您的账号(输完回车): ")
    password = input("请输入您的密码(输完回车): ")
    target_teacher_name = input("请输入您的选课老师名字(没有就回车): ")
    target_name = input("请输入您的课程名称(带上课程数字编号 如 网球3 ): ): ")
    target_courseCode = input("请输入您的课程代码(没有就回车): ")
    
    month = int(input("请输入抢课月份(1-12): "))
    day = int(input("请输入抢课开始日(1-31): "))
    hour = int(input("请输入抢课开始小时(0-23): "))
    minute = int(input("请输入抢课开始分钟(0-59): "))
    second = int(input("请输入抢课开始秒数(0-59): "))
    predict_Time = datetime(datetime.now().year,month,day,hour,minute,second)

    return Login_Data(username,password,target_teacher_name,target_name,target_courseCode,predict_Time)

if __name__ == "__main__":
    print("软工班特供版,请在抢课提前2小时前打开此程序(能显示预览界面的时候)。")
    # 这是加入白名单
    whitelist=[2120243448,2120242335,2120241946,2120242852,2120241188,2120243152
               ,2120243019,2120240981,2120243525,2120242760,2120233697,2120221309,
                2120221109, 2120223024, 2120230029, 2120231160, 2120231281,
                2120231369, 2120231382, 2120231383, 2120231442, 2120231481,
                2120231493, 2120231571, 2120231641, 2120231671, 2120231716,
                2120231718, 2120231749, 2120231777, 2120231869, 2120231876,
                2120231913, 2120231933, 2120232018, 2120232067, 2120232213,
                2120232272, 2120232276, 2120232292, 2120232311, 2120232330,
                2120232421, 2120232448, 2120232457, 2120232465, 2120232477,
                2120232559, 2120232597, 2120232636, 2120232704, 2120232737,
                2120232787, 2120232961, 2120232969, 2120233007, 2120233009,
                2120233069, 2120233130, 2120233151, 2120233159, 2120233196,
                2120233206, 2120233212, 2120233233, 2120233312, 2120233316,
                2120233336, 2120233357, 2120233372, 2120233392, 2120233422,
                2120233524, 2120233536, 2120233679, 2120233697, 2120233707,
                2120233736, 2120233770, 2120233776, 2120233983, 2120233984,
                2120234161, 2120234174, 4120230028, 4120230030
               ]
    
    list = DataInput()
# ===================================================
# 下列是让用户在窗口输入账号登录
    username = list.username
    if int(username) not in whitelist:
        print("不在白名单中，启动自毁程序，你的电脑即将自毁。倒计时")
        for i in range(10, 0, -1):
            print(i)
            time.sleep(1)
        time.sleep(10)
        sys.exit()
    password = list.password
    target_teacher_name = list.target_teacher_name
    target_name = list.target_name
    target_courseCode = list.target_courseCode
    predict_Time = list.predict_Time
# ===================================================
# 注释上面部分，取消这部分不使用手动输入账号登录
    # target_teacher_name = "" # 教师姓名
    # target_courseCode = '' # 课程代码 可选
    # target_name = '书记校长公开课' # 课程名称
    # username = ""  # 学号
    # password = ""  # 密码
# ===================================================

    # predict_Time = datetime(2024, 11, 4, 20, 16, 0) # 预测抢课时间



    headers['Authorization'] = get_cookie(username,password)
    stuID = requests.get(url_get_stuID, headers=headers)
    print(stuID)
    stuID_json = stuID.json()
    if stuID_json.get("data") == []:
        print("获取学生ID失败，请检查是否已经开放选课预览页面。程序退出")
        time.sleep(10)
        sys.exit()
    studentAssoc = stuID_json.get("data")[0]


    # courseSelectTurnAssoc = requests.get(url_OpenTurns + str(studentAssoc), headers=headers)
    # courseSelectTurnAssoc_json = courseSelectTurnAssoc.json()
    # courseSelectTurnAssoc = courseSelectTurnAssoc_json.get("data")[0].get("id")

    # select = requests.get(url_select + str(studentAssoc) +'/turn/' + str(courseSelectTurnAssoc) + '/select'  , headers=headers)
    # select_json = select.json()
    # semesterId = select_json.get("data").get('turn').get("semesterAssoc")
    # campusId = select_json.get("data").get("campusId")
    

    # 遍历所有元素并获取 id
    courseSelectTurnAssoc = requests.get(url_OpenTurns + str(studentAssoc), headers=headers)
    courseSelectTurnAssoc_json = courseSelectTurnAssoc.json()
    course_ids = [item.get("id") for item in courseSelectTurnAssoc_json.get("data")]
    course_name = [item.get("name") for item in courseSelectTurnAssoc_json.get("data")]
    i = 0
    results = []

    for course_id in course_ids:
        select = requests.get(url_select + str(studentAssoc) + '/turn/' + str(course_id) + '/select', headers=headers)
        
        select_json = select.json()
        semesterId = select_json.get("data").get('turn').get("semesterAssoc")
        campusId = select_json.get("data").get("campusId")
        # 将结果存入数组
        results.append({
            "turn_id": course_id,
            "semester_id": semesterId,
            "campus_id": campusId,
            "course_name": course_name[i]
        })

        i = i+1
        
    for i, result in enumerate(results):
        print(f"选择序号: {i}, 课程名称: {result['course_name']}, Course ID: {result['turn_id']}, Semester ID: {result['semester_id']}, Campus ID: {result['campus_id']}")

    index = int(input("请输入要选择的序号:"))

    selected_course = results[index]
    selected_campus_id = selected_course["campus_id"]
    selected_semesterId = selected_course["semester_id"]
    selected_turn_id = selected_course["turn_id"]
    selected_course_name = selected_course["course_name"]


    data_course = {
    "adminclassId": "",
    "campusId": selected_campus_id,
    "canSelect": 1,
    "courseNameOrCode": target_courseCode,
    "coursePropertyId": "",
    "courseSubstitutePoolId": None,
    "courseTypeId": "",
    "creditGte": None,
    "creditLte": None,
    "departmentId": "",
    "grade": "",
    "hasCount": None,
    "ids": None,
    "lessonNameOrCode": "",
    "majorId": "",
    "openDepartmentId": "",
    "pageNo": 1,
    "pageSize": 20,
    "semesterId": selected_semesterId,
    "sortField": "course",
    "sortType": "ASC",
    "studentId": studentAssoc,
    "substitutedCourseId": None,
    "teacherNameOrCode": target_teacher_name,
    "turnId": selected_turn_id,
    "week": "",
    "_canSelect": "可选"
}

    course = requests.post(url_Lesson + str(studentAssoc) +'/' + str(selected_turn_id), headers=headers, json=data_course)
    course_josn = course.json()
    for lesson in course_josn['data']['lessons']:
        if lesson['course']['nameZh'] == target_name:
            lesson_names = lesson['course']['nameZh']
            lessonAssoc = lesson['id']
            break

    # lessons = course_josn['data']['lessons']
    # lessonAssoc = [lesson['id'] for lesson in lessons]
    # lesson_names = [lesson['minorCourse']['nameZh'] for lesson in lessons]
    data = {
        "studentAssoc": studentAssoc,
        "courseSelectTurnAssoc": selected_turn_id,
        "requestMiddleDtos": [
            {
                "lessonAssoc": lessonAssoc,
                "virtualCost": 0 #应该是识别码，0代表预先请求
            }
        ],
        "coursePackAssoc": None
    }
    data_request = {
        "studentAssoc": studentAssoc,
        "courseSelectTurnAssoc": selected_turn_id,
        "requestMiddleDtos": [
            {
                "lessonAssoc": lessonAssoc,
                "virtualCost": None #应该是识别码，None代表请求
            }
        ],
        "coursePackAssoc": None
    }
    print('请确认即将抢课信息：')
    print(f'学生信息:ID:{studentAssoc}')
    print(f"选课大类名称：{selected_course_name}, 获取到的课程ID：{lessonAssoc}，授课教师：{target_teacher_name}" )
    time.sleep(2)
    url_predicate_response_orgin = url_predicate_response_orgin + str(studentAssoc) +'/'
    url_add_drop_response_orgin = url_add_drop_response_orgin + str(studentAssoc) +'/'
    main()
    time.sleep(100000)