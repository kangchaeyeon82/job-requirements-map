import json,os,re
from collections import Counter
L=json.load(open('data/list.json',encoding='utf-8'))
TAX={
"언어":{"C":r"(?<![A-Za-z#/+])C(?![A-Za-z#+])|C/C\+\+|C언어","C++":r"C\+\+","Python":r"python|파이썬","Java/Kotlin":r"\bjava\b|kotlin","C#":r"C#","Rust":r"\brust\b","Go":r"\bgolang\b|\bGo\b(?= ?(언어|lang|,|/))","Verilog/SV":r"verilog|systemverilog","VHDL":r"vhdl","MATLAB/Simulink":r"matlab|simulink","Assembly":r"assembly|어셈블리"},
"OS·플랫폼":{"Linux":r"linux|리눅스","Embedded Linux/Yocto":r"yocto|buildroot|embedded linux|임베디드 리눅스","Linux Kernel/드라이버":r"kernel|커널|device driver|디바이스 드라이버|드라이버","RTOS":r"rtos|freertos|zephyr|threadx|vxworks|실시간 운영","Android/AOSP":r"android|aosp|안드로이드","ROS/ROS2":r"\bros\b|ros2|ros/ros2","Bootloader":r"bootloader|부트로더|u-boot","Windows":r"windows|윈도우"},
"프로세서·칩":{"MCU":r"\bmcu\b|마이크로컨트롤러|마이컴","STM32":r"stm32","ARM/Cortex":r"\barm\b|cortex","ESP32":r"esp32","Nordic nRF":r"nordic|nrf5","FPGA":r"fpga|xilinx|altera|vivado","SoC":r"\bsoc\b","NVIDIA Jetson/GPU":r"jetson|nvidia|\bgpu\b|cuda","NPU":r"\bnpu\b","RISC-V":r"risc-v","DSP":r"\bdsp\b","Qualcomm":r"qualcomm|퀄컴","Raspberry Pi/Arduino":r"raspberry|라즈베리|arduino|아두이노","PLC":r"\bplc\b"},
"통신·인터페이스":{"UART":r"uart","SPI":r"\bspi\b","I2C":r"i2c","CAN/CAN-FD":r"\bcan\b|can-fd|canfd|can ?통신","Ethernet":r"ethernet|이더넷","EtherCAT":r"ethercat","USB":r"\busb\b","PCIe":r"pcie","MIPI":r"mipi","BLE/Bluetooth":r"\bble\b|bluetooth|블루투스","Wi-Fi":r"wi-?fi|wlan","LTE/5G/셀룰러":r"\blte\b|\b5g\b|cellular|nb-iot|lte-m","TCP/IP·소켓":r"tcp|소켓|socket","MQTT":r"mqtt","Modbus":r"modbus","RS-232/485":r"rs-?232|rs-?485","GPIO/PWM/ADC":r"gpio|pwm|\badc\b"},
"HW 설계·검증":{"회로 설계":r"회로 ?설계|schematic|회로도|circuit design","PCB/Artwork":r"pcb|artwork|아트웍","OrCAD":r"orcad","Altium":r"altium","PADS":r"\bpads\b","KiCad":r"kicad","Cadence/Allegro":r"cadence|allegro","아날로그 회로":r"아날로그|analog","디지털 회로":r"디지털 회로|digital (circuit|logic|design)","전원 설계(DC-DC 등)":r"dc-dc|전원 ?(회로|설계|부)|power (supply|design|management)|pmic|smps","EMC/EMI":r"emc|emi","SI/PI":r"\bsi/pi\b|signal integrity|신호 무결성","RF/안테나":r"\brf\b|안테나|antenna","모터 제어/BLDC":r"모터|motor|bldc|인버터","BMS/배터리":r"\bbms\b|배터리|battery","계측장비(오실로스코프 등)":r"오실로스코프|oscilloscope|계측|analyzer|분석기","Bring-up/보드 디버깅":r"bring-?up|브링업","인증(KC/FCC/CE)":r"\bkc\b|fcc|\bce\b 인증|전파인증|인증 ?(획득|대응|경험)","양산/DFM":r"양산|dfm|mass production","RTL/ASIC":r"\brtl\b|asic|synopsys|합성"},
"개발 도구·방법론":{"Git":r"\bgit\b|github|gitlab|형상관리","Docker/K8s":r"docker|kubernetes|k8s|컨테이너","CI/CD":r"ci/cd|jenkins|github actions","JTAG/디버거":r"jtag|j-link|디버거|trace32|swd","Jira/Confluence":r"jira|confluence","CMake/빌드시스템":r"cmake|makefile|bazel|빌드 시스템","단위테스트/검증 자동화":r"unit ?test|단위 ?테스트|gtest|테스트 자동화|hil|sil","AI 코딩툴 활용":r"claude|copilot|cursor|chatgpt|ai (코딩|도구|툴)|llm 기반 (개발|도구)"},
"AI·비전":{"AI/딥러닝":r"딥러닝|deep learning|머신러닝|machine learning|\bai\b|인공지능","TensorRT/모델 최적화":r"tensorrt|onnx|양자화|quantiz|모델 경량화|tflite","PyTorch/TF":r"pytorch|tensorflow","LLM/VLM":r"\bllm\b|\bvlm\b|vla","컴퓨터 비전/카메라":r"vision|비전|카메라|camera|opencv|isp|gstreamer"},
"로보틱스·제어":{"제어 이론(PID/MPC)":r"\bpid\b|\bmpc\b|제어 ?이론|control theory|칼만|kalman","센서 퓨전/IMU":r"fusion|퓨전|\bimu\b","LiDAR/Radar":r"lidar|라이다|radar|레이더","SLAM/Localization":r"slam|localization|측위","드론(PX4/ArduPilot)":r"px4|ardupilot|mavlink|드론|drone|uav","로봇/매니퓰레이터":r"로봇|robot|매니퓰레이터|manipulator|amr|agv","시뮬레이션(Isaac/Gazebo)":r"isaac|gazebo|시뮬레이션|simulation","기구/SolidWorks":r"solidworks|기구 ?설계|\bcad\b"},
"차량·안전 표준":{"자동차/차량":r"automotive|자동차|차량|vehicle","AUTOSAR":r"autosar","ISO 26262/기능안전":r"26262|기능 ?안전|functional safety","ASPICE":r"aspice","MISRA":r"misra","IEC 61508 등 산업안전":r"iec ?6\d{4}|iec"},
}
EDU={"학사 이상":r"학사|bachelor|4년제|대졸|b\.s","석사 이상":r"석사|master|m\.s","박사":r"박사|ph\.?d","전자/전기공학":r"전자|전기|electrical|electronic","컴퓨터공학/SW":r"컴퓨터|computer science|소프트웨어|software engineering","기계/메카트로닉스":r"기계|메카트로닉스|mechanical|mechatronics","제어/로봇공학":r"제어계측|제어공학|로봇공학"}
SOFT={"커뮤니케이션/협업":r"커뮤니케이션|소통|협업|communication|collaborat","문서 작성":r"문서|documentation|보고서","영어":r"영어|english|영문","자기주도/문제해결":r"주도|문제 ?해결|problem[- ]solving|ownership","스타트업/빠른 환경":r"스타트업|startup|빠르게"}
def find(dic,text):
    out=[]
    for k,p in dic.items():
        if re.search(p,text,re.I): out.append(k)
    return out
jobs=[];
for it in L:
    j=json.load(open(f"data/d/{it['id']}.json",encoding='utf-8'))['job'];d=j['detail']
    req=d.get('requirements') or '';pref=d.get('preferred_points') or ''
    task=d.get('main_tasks') or ''
    rk={};pk={}
    for cat,dic in TAX.items():
        a=find(dic,req); b=find(dic,pref)
        if a: rk[cat]=a
        if b: pk[cat]=b
    jobs.append(dict(id=it['id'],co=it['company']['name'],pos=it['position'],cat=it['category_tag']['id'],
      loc=(it['address'] or {}).get('location'),dist=(it['address'] or {}).get('district'),country=(it['address'] or {}).get('country'),
      yf=it.get('annual_from'),yt=it.get('annual_to'),newbie=it.get('is_newbie'),emp=it.get('employment_type'),
      due=j.get('due_time'),req=req.strip(),pref=pref.strip(),task=task.strip(),
      rk=rk,pk=pk,edu=find(EDU,req),soft=find(SOFT,req+'\n'+pref)))
json.dump(jobs,open('jobs.json','w',encoding='utf-8'),ensure_ascii=False)
for cat,dic in TAX.items():
    cr=Counter(k for x in jobs for k in x['rk'].get(cat,[]));cp=Counter(k for x in jobs for k in x['pk'].get(cat,[]))
    print(cat,[(k,cr[k],cp[k]) for k in sorted(dic,key=lambda k:-(cr[k]+cp[k]))])
print(Counter(e for x in jobs for e in x['edu']));print(Counter(e for x in jobs for e in x['soft']))
print(Counter(x['loc'] for x in jobs));print(Counter(x['country'] for x in jobs));print(Counter(x['emp'] for x in jobs))
print(Counter((x['yf'],x['yt']) for x in jobs).most_common(30))
print(Counter(x['co'] for x in jobs).most_common(20))
print(sum(1 for x in jobs if not x['rk']), sum(1 for x in jobs if len(x['req'])<30))
