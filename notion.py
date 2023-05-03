import requests
from notion_client import Client
from datetime import datetime, timezone
import time

# Notion Integrationのトークンを設定
# APIキーをセットアップします。
notion = Client(auth="secret_wBTEjpVx4zifSZGypDyYVMH2HF3WbcrDFceBh2CHnJf")
NOTION_API_KEY = "secret_wBTEjpVx4zifSZGypDyYVMH2HF3WbcrDFceBh2CHnJf"

# NotionのデータベースIDを設定

# NotionデータベースのIDと名前を指定します。
DATABASE_ID = "b87bc474cb8e436b875b1655c6e2c121"
DATABASE_NAME = "ABC 精進リスト"

# Notionデータベースを取得
results = notion.search(query=DATABASE_NAME, filter={"property": "object", "value": "database"}).get("results")
if len(results) == 0:
    raise ValueError(f"No Notion database was found with name {DATABASE_NAME}")
if len(results) > 1:
    raise ValueError(f"Multiple Notion databases were found with name {DATABASE_NAME}")
database = results[0]

# Notionデータベースのページを取得
pages = notion.databases.query(
    **{
        "database_id": DATABASE_ID,
    }
).get("results")

# ページからタスクを取得してリストに格納
existing_problems = set()
for page in pages:
    task = {
        "id": page["id"],
        "name": page["properties"]["名前"]["title"][0]["text"]["content"],
        # "status": page["properties"]["ステータス"]["status"]["name"],
    }
    existing_problems.add(task["name"])

# print(existing_problems)

# AtCoder Problemsからの情報取得

# 6問になったABC126以降の問題一覧の中からC/D/E問題を取得
url = "https://kenkoooo.com/atcoder/resources/problems.json"

# APIリクエストを送信し、レスポンスを取得
response = requests.get(url)

tmp_adding_problems = []
if response.status_code == 200:
    results = response.json()
    for result in results:
        id = result["contest_id"]
        problem_idx = result["problem_index"]
        # ABCのCDE問題をフィルタ
        if id[:3] == "abc" and problem_idx in ["C","D","E"]:
            num = int(id[3:])
            if num >= 126:
                tmp_adding_problems.append(result)
else:
    print("Failed to retrieve data")

# print(tmp_adding_problems)

# 6問になったABC126以降の問題一覧の中からAC済のC/D/E問題を取得
def get_accepted_problems(user_id, from_date):
    from_second = int((from_date - datetime(1970, 1, 1)).total_seconds())
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={from_second}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch submissions: {response.status_code} - {response.text}")

    submissions = response.json()
    accepted_problems = set()
    for submission in submissions:
        if submission["result"] == "AC":
            contest_id = submission["problem_id"][:3]
            if contest_id == "abc":
                problem_idx = submission["problem_id"][-1]
                if problem_idx in ["c","d", "e"]:
                    accepted_problems.add(submission["problem_id"])
    
    return accepted_problems

ac_problems = set()
for year in [2021]:
    for month in [4]:
# for year in [2021,2022]:
#     for month in [1,4,7,10]:
        time.sleep(2)
        ac_problems |= get_accepted_problems("otsuneko", datetime(year, month, 1))
        print(year,month)

# print(ac_problems)
# print(len(ac_problems))


# Notionにタスクを追加
# adding_problemsの全問題からexisting_problemsを除いた問題を
# Notionに今回追加する問題と判定。AC済なら要復習に入れる。
adding_problems = []
for problem in tmp_adding_problems:
    if problem["title"] not in existing_problems:
        adding_problems.append(problem)
        
for problem in adding_problems:
    if problem["problem_index"] in ac_problems:
        url = f"https://atcoder.jp/contests/{problem['contest_id']}/tasks/{problem['problem_id']}"
        new_task = {
            "名前": {"title": [{"text": {"content": problem["title"]}}]},
            "ステータス": {"status": {"name": {"select": {"name": "要復習"}}}},
            "URL": {"url": url}
        }
    else:
        new_task = {
            "名前": {"title": [{"text": {"content": problem["title"]}}]},
            "ステータス": {"status": {"name": {"select": {"name": "未AC"}}}},
            "URL": {"url": url}
        }

    # タスクをNotionデータベースに追加します。
    notion.pages.create(parent={"database_id": DATABASE_ID}, properties=new_task)