import os
from dotenv import load_dotenv
from icalendar import Calendar, Event
import datetime
import subprocess
import json
import pyperclip
import gemini
# 加载.env文件
load_dotenv()

# 从环境变量中获取API密钥
# openai.api_key = os.getenv("OPENAI_API_KEY")
model_name="gpt-4o-mini",

def get_event_info():
    """从剪贴板获取事件信息"""
    event_info = pyperclip.paste()
    print("从剪贴板读取的事件信息：")
    print(event_info)
    return event_info

def process_with_openai(event_info):
    """使用OpenAI API处理事件信息并返回JSON格式的结果"""
    # client = openai.OpenAI()
    today = datetime.date.today().strftime("%Y-%m-%d")
    # 星期几
    weekday = datetime.date.today().weekday()+1
    time_zone = datetime.datetime.now().astimezone().tzinfo
    print("try to run prompt")
    messages=[
        {
        "role": "user",
        "content": f"你是一个日历助手,可以从用户输入中提取事件信息并格式化为JSON。今天是{today}，时区为{str(time_zone)}，星期{weekday}。参考今天的日期，从以下多行信息中提取事件标题、日期、开始时间、结束时间、地点和详细描述,并以JSON格式返回。格式应为: {{\"title\": \"事件标题\", \"date\": \"YYYY-MM-DD\", \"start_time\": \"HH:MM\", \"end_time\": \"HH:MM\", \"location\": \"地点\", \"description\": \"详细描述\"}}。如果某项信息缺失,对应的值应为null。如果没有明确指定日期,请假设事件发生在今天或最近的未来日期。不需要返回```json和```,以下是事件信息: \n{event_info}\n"
        }
    ]
    response = gemini.llm_response(messages)
    if(response.startswith("```json")):
        response = response[10:]
    if(response.endswith("```")):
        response = response[:-3]
    return response

def create_ics_file(event_json: str):
    """根据JSON创建ICS文件"""
    cal = Calendar()
    event = Event()
    # event_json 删除第一行和最后一行,保留str格式
    event_data = json.loads(event_json)
    # print(event_data)
    print("json转化成功")
    event.add('summary', event_data['title'])
    
    if event_data['date'] and event_data['start_time']:
        start_datetime = datetime.datetime.strptime(f"{event_data['date']} {event_data['start_time']}", "%Y-%m-%d %H:%M")
        event.add('dtstart', start_datetime)
    
    if event_data['date'] and event_data['end_time']:
        end_datetime = datetime.datetime.strptime(f"{event_data['date']} {event_data['end_time']}", "%Y-%m-%d %H:%M")
        event.add('dtend', end_datetime)
    
    if event_data['location']:
        event.add('location', event_data['location'])
    
    if event_data['description']:
        event.add('description', event_data['description'])
    
    cal.add_component(event)
    
    with open('event.ics', 'wb') as f:
        f.write(cal.to_ical())

def open_ics_file():
    """打开ICS文件"""
    if os.name == 'nt':  # Windows
        os.startfile('event.ics')
    elif os.name == 'posix':  # macOS 和 Linux
        subprocess.call(('open', 'event.ics'))

def main():
    event_info = get_event_info()
    processed_info = process_with_openai(event_info)
    print("处理结果：")
    print(processed_info)
    try:
        create_ics_file(processed_info)
        print("ICS文件已创建")
        open_ics_file()
    except json.JSONDecodeError:
        print("无法解析JSON数据,请检查LLM的输出格式")
    except Exception as e:
        print(f"创建ICS文件时发生错误: {str(e)}")

if __name__ == "__main__":
    main()
