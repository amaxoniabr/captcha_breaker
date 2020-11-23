from base64 import b64encode
from sys import argv
from requests import post
from time import sleep


def encode_file(file_path):
    with open(file_path, "rb") as file:
        encoded_value = b64encode(file.read())
        return encoded_value


def create_req_body(encoded_file):
    json = {
        "clientKey": "c07cd9f7cb01c4274e40ef22f0f0fc73",
        "task": {
            "type": "ImageToTextTask",
            "body": encoded_file.decode('utf8'),
            "phrase": False,
            "case": False,
            "numeric": 0,
            "math": False,
            "minLength": 0,
            "maxLength": 0
        }
    }
    return json


def send_request(json):
    task_resp = post(url="http://api.anti-captcha.com/createTask", json=json)
    task_id = task_resp.json()["taskId"]
    return task_id


def create_query_body(task_id):
    json = {
        "clientKey": "c07cd9f7cb01c4274e40ef22f0f0fc73",
        "taskId": task_id
    }
    return json


def get_status(json):
    task = post(
        url="https://api.anti-captcha.com/getTaskResult", json=json)
    status = task.json()["status"]
    return status


def get_solution(json):
    task = post(
        url="https://api.anti-captcha.com/getTaskResult", json=json)
    solution_text = task.json()["solution"]["text"]
    return solution_text


def create_solution_file(solution_text):
    with open("solution.txt", "w") as solution_file:
        solution_file.write(solution_text)


def main():
    encoded_value = encode_file(argv[1])
    json = create_req_body(encoded_value)
    task_id = send_request(json)
    json = create_query_body(task_id)
    for i in range(30):
        status = get_status(json)
        if status == "processing":
            sleep(1)
        else:
            solution_text = get_solution(json)
            break
    create_solution_file(solution_text)


if __name__ == "__main__":
    main()
