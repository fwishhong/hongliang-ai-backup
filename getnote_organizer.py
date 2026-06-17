#!/usr/bin/env python3
import subprocess, json, time

API_KEY = "gk_live_4540ae62d59cd916.581bd7a644c6701207b2055c3226f72fcc7cbed8bc781577"
CLIENT_ID = "cli_3802f9db08b811f197679c63c078bacc"
BASE = "https://openapi.biji.com"

def api_get(path):
    r = subprocess.run(['curl','-s',f'{BASE}{path}',
        '-H',f'Authorization: {API_KEY}',
        '-H',f'X-Client-ID: {CLIENT_ID}'],
        capture_output=True, text=True)
    return json.loads(r.stdout)

def api_post(path, data):
    r = subprocess.run(['curl','-s','-X','POST',f'{BASE}{path}',
        '-H',f'Authorization: {API_KEY}',
        '-H',f'X-Client-ID: {CLIENT_ID}',
        '-H','Content-Type: application/json',
        '-d', json.dumps(data)],
        capture_output=True, text=True)
    return json.loads(r.stdout)

# 先看现有知识库
kb_list = api_get('/open/api/v1/resource/knowledge/list')
existing = {k['name']: k['id'] for k in kb_list.get('data',{}).get('topics',[])}
print(f"现有知识库: {list(existing.keys())}")

# 创建缺失的知识库
new_kbs = ["📚 儿子日本留学","👨‍👦 亲子教育","🇯🇵 日本生活","💼 工作职场",
           "🤖 AI应用与创作","💰 投资理财","🏋️ 生活健康","📖 读书笔记","🎮 游戏开发","🍜 餐饮美食"]

kb_ids = dict(existing)
for name in new_kbs:
    if name in existing:
        print(f"已有: {name}")
        continue
    result = api_post('/open/api/v1/resource/knowledge/create', {"name": name})
    if result.get('success'):
        kid = result['data']['id']
        kb_ids[name] = kid
        print(f"创建: {name} -> {kid}")
    else:
        print(f"创建失败: {name} -> {result}")
    time.sleep(0.5)

print("\n=== 知识库ID映射 ===")
for k,v in kb_ids.items():
    print(f"  {k}: {v}")
