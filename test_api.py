import requests
import json

# 配置后端 API 的基本 URL
BASE_URL = "http://localhost:8000/api"

# 设置不使用代理访问 localhost
proxies = {
    "http": None,
    "https": None,
}

def get_room_info():
    url = f"{BASE_URL}/room_info"
    print("1")
    try:
        response = requests.get(url, proxies=proxies)
        print("2")
        response.raise_for_status()
        print("3")
        rooms = response.json()
        print("房间信息获取成功：")
        for room in rooms:
            print(json.dumps(room, ensure_ascii=False, indent=2))
        return rooms
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 错误: {err}")
        print(f"响应内容: {response.text}")
    except Exception as err:
        print(f"其他错误: {err}")
    return None

# 其他函数同样添加 proxies 参数
def checkin(room_number, guest_name, guest_id_number):
    url = f"{BASE_URL}/checkin"
    payload = {
        "room_number": room_number,
        "guest_name": guest_name,
        "guest_id_number": guest_id_number
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        response.raise_for_status()
        result = response.json()
        print("办理入住成功：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 错误: {err}")
        print(f"响应内容: {response.text}")
    except Exception as err:
        print(f"其他错误: {err}")
    return None

def checkout(room_number):
    url = f"{BASE_URL}/checkout"
    payload = {
        "room_number": room_number
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=payload, proxies=proxies)
        response.raise_for_status()
        result = response.json()
        print("办理退房成功：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    except requests.exceptions.HTTPError as err:
        print(f"HTTP 错误: {err}")
        print(f"响应内容: {response.text}")
    except Exception as err:
        print(f"其他错误: {err}")
    return None

def main():
    print("===== 获取初始房间信息 =====")
    rooms = get_room_info()

    if not rooms:
        print("无法获取房间信息，退出测试。")
        return

    # 选择一个未入住的房间进行测试
    available_rooms = [room for room in rooms if not room.get('isPoweredOn', False)]
    if not available_rooms:
        print("没有可用的房间进行入住测试。")
        return

    test_room = available_rooms[0]
    room_number = test_room['roomNumber']
    guest_name = "张三"
    guest_id_number = "123456789012345678"

    print(f"\n===== 办理入住 (房间 {room_number}) =====")
    checkin_result = checkin(room_number, guest_name, guest_id_number)
    if not checkin_result:
        print("办理入住失败，退出测试。")
        return

    print("\n===== 获取入住后的房间信息 =====")
    rooms_after_checkin = get_room_info()

    print(f"\n===== 办理退房 (房间 {room_number}) =====")
    checkout_result = checkout(room_number)
    if not checkout_result:
        print("办理退房失败，退出测试。")
        return

    print("\n===== 获取退房后的房间信息 =====")
    rooms_after_checkout = get_room_info()

if __name__ == "__main__":
    main()
