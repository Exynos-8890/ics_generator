from event_to_calendar import *
import time

def main():
    start_time = time.time()
    with open('testcase.txt', 'r', encoding='utf-8') as f:
        event_info = f.read()
    processed_info = process_event(event_info)
    end_time = time.time()
    print("处理耗时：", round((end_time - start_time),3), "秒")
    print("处理结果：")
    print(processed_info)

if __name__ == "__main__":
    main()