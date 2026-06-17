#!/usr/bin/env python3
"""GetNote 笔记归类脚本 - 批量处理不打扰用户"""
import subprocess, json, time, sys

API_KEY = "gk_live_4540ae62d59cd916.581bd7a644c6701207b2055c3226f72fcc7cbed8bc781577"
CLIENT_ID = "cli_3802f9db08b811f197679c63c078bacc"
BASE = "https://openapi.biji.com"
LOG_FILE = "/Users/hongliang/.openclaw/workspace/memory/getnote_organizer.log"

KB_IDS = {
    "📚 儿子日本留学": "d04W7zrY",
    "👨‍👦 亲子教育": "Q0G2PzDY",
    "🇯🇵 日本生活": "rYM6dQb0",
    "💼 工作职场": "7JbkKmNn",
    "🤖 AI应用与创作": "MJa3vLdY",
    "💰 投资理财": "EJXAa7ln",
    "🏋️ 生活健康": "EJl7XN10",
    "📖 读书笔记": "QYAx9gWn",
    "🎮 游戏开发": "pYLoBQ7n",
    "🍜 餐饮美食": "LYwDVeq0",
}

# 分类规则：关键词 -> 知识库
KB_RULES = {
    "📚 儿子日本留学": ["日本留学","留学","儿子","私塾","语言学校","考学","艺术留学","美术留学","留学生","儿子日本","接送儿子","在日本"],
    "👨‍👦 亲子教育": ["亲子","儿子闹肚子","亲子日常","孩子","家长","沟通","教育"],
    "🇯🇵 日本生活": ["日本","东京","日本生活","出行","购物","逛街","机场","出入境","日本办事","在日本"],
    "💼 工作职场": ["工作","职场","团队","同事","开会","出差","业务","老板","薪酬","裁员"],
    "🤖 AI应用与创作": ["AI","ChatGPT","人工智能","写作","小说","创作","AIGC","工具使用"],
    "💰 投资理财": ["投资","股票","炒股","理财","多瑞","收益","基金","融资"],
    "🏋️ 生活健康": ["健身","跑步","膝盖","身体","健康","减肥","运动"],
    "📖 读书笔记": ["得到","读书","专栏","课程","学习"],
    "🎮 游戏开发": ["游戏","Unity","开发","引擎","程序员"],
    "🍜 餐饮美食": ["美食","餐厅","用餐","吃饭","餐饮","烹饪","菜"],
}

# 补充标签规则
TAG_RULES = {
    "亲子日常": ["👨‍👦 亲子教育"],
    "日本留学": ["📚 儿子日本留学"],
    "AI应用": ["🤖 AI应用与创作"],
    "投资": ["💰 投资理财"],
    "生活周记": ["🏋️ 生活健康"],
    "得到": ["📖 读书笔记"],
    "游戏": ["🎮 游戏开发"],
    "餐饮": ["🍜 餐饮美食"],
    "职场": ["💼 工作职场"],
}

def log(msg):
    ts = time.strftime("%m-%d %H:%M")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE,"a") as f:
        f.write(line + "\n")

def api_get(path):
    r = subprocess.run(['curl','-s',f'{BASE}{path}',
        '-H',f'Authorization: {API_KEY}',
        '-H',f'X-Client-ID: {CLIENT_ID}'],
        capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except:
        return {}

def api_post(path, data):
    r = subprocess.run(['curl','-s','-X','POST',f'{BASE}{path}',
        '-H',f'Authorization: {API_KEY}',
        '-H',f'X-Client-ID: {CLIENT_ID}',
        '-H','Content-Type: application/json',
        '-d', json.dumps(data)],
        capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except:
        return {}

def classify_note(note):
    """根据标题+内容+标签 判断属于哪个知识库"""
    text = " ".join([
        note.get('title',''),
        note.get('content','')[:500],
        " ".join(t['name'] for t in note.get('tags',[]))
    ]).lower()
    
    matched = []
    for kb_name, keywords in KB_RULES.items():
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score > 0:
            matched.append((score, kb_name))
    
    matched.sort(reverse=True)
    return [m[1] for m in matched[:2]]  # 最多2个知识库

def add_tags(note_id, existing_tags, needed_tags):
    """添加缺失标签"""
    existing = {t['name'] for t in existing_tags}
    to_add = [t for t in needed_tags if t not in existing]
    if not to_add:
        return 0
    
    for tag in to_add:
        result = api_post('/open/api/v1/resource/note/tags/add', {
            "note_id": note_id,
            "tag_name": tag
        })
        time.sleep(0.3)
    return len(to_add)

def add_to_kb(note_id, kb_ids):
    """把笔记加入知识库"""
    for kb_id in kb_ids:
        result = api_post('/open/api/v1/resource/knowledge/note/batch-add', {
            "topic_id": kb_id,
            "note_ids": [note_id]
        })
        time.sleep(0.3)

def main():
    log("=== 开始归类任务 ===")
    cursor = "0"
    total = 0
    tagged = 0
    categorized = 0
    
    while True:
        log(f"获取笔记批次的cursor: {cursor}")
        data = api_get(f'/open/api/v1/resource/note/list?since_id={cursor}&limit=30')
        
        if not data.get('success'):
            log(f"API失败: {data}")
            break
        
        notes = data['data']['notes']
        if not notes:
            break
        
        has_more = data['data'].get('has_more', False)
        next_cursor = str(data['data'].get('next_cursor', data['data'].get('cursor', '0')))
        
        for note in notes:
            total += 1
            note_id = note['id']
            title = note.get('title','(无标题)')[:30]
            tags = note.get('tags', [])
            existing_tag_names = [t['name'] for t in tags]
            
            # 分类
            kbs = classify_note(note)
            
            # 补充标签
            needed_tags = []
            for kb in kbs:
                for t in TAG_RULES:
                    if t.lower() in " ".join(existing_tag_names).lower():
                        continue
                    if kb in KB_RULES and any(kw.lower() in note.get('content','')[:200].lower() for kw in KB_RULES[kb]):
                        needed_tags.append(t)
            
            if needed_tags:
                n = add_tags(note_id, tags, list(set(needed_tags)))
                if n > 0:
                    tagged += n
                    log(f"  +标签:{note_id} [{title}] +{n}个标签")
            
            # 加入知识库
            if kbs:
                kb_ids = [KB_IDS[kb] for kb in kbs if kb in KB_IDS]
                if kb_ids:
                    add_to_kb(note_id, kb_ids)
                    categorized += 1
                    log(f"  →归类:{note_id} [{title}] -> {[kbs]}")
            
            time.sleep(0.2)
        
        if not has_more:
            break
        cursor = next_cursor
        time.sleep(0.5)
    
    log(f"=== 完成 ===")
    log(f"总处理: {total}条 | 补标签:{tagged}次 | 归类:{categorized}条")

if __name__ == "__main__":
    main()
