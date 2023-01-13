from util.response import res
from util.dbconnect import mongoConnect
from flask import request, Blueprint

from datetime import datetime

app: Blueprint = Blueprint("routes", __name__)

cluster = mongoConnect()
stats = cluster["stats"]["general"]
props = cluster["props-v2"]["info"]

@app.route('/summary', methods=['GET'])
def summary():
    staffs = []
    boosters = []
    result = stats.find_one({"_id": "0"})

    for member in result['specialMembers']:
        memberInfo = props.find_one({"member_id": member['member']["id"]}) or {"occupation": None, "bio": None, "github": None, "skills": None}
    
        memberObject = {
            'id': member['member']['id'],
            'role': member['role'],
            'avatar': member['member']['avatarUrl'],
            'name': member['member']['name'],
            'occupation': memberInfo['occupation'] if memberInfo['occupation'] else "Sem ocupação",
            'bio': memberInfo['bio'] if memberInfo['bio'] else "Descrição não definida",
            'github': memberInfo['github'] if memberInfo['github'] else "https://github.com/codify-community",
            'technologies': memberInfo['skills'] if memberInfo['skills'] else ['n/a']
        }

        if member['role'] in ['admin', 'mod']:
            staffs.append(memberObject)
        elif member['role'] == 'booster':
            boosters.append(memberObject)
    
    d1 = datetime.strptime(datetime.fromisoformat("2020-08-13T03:00:00.000+00:00").strftime("%Y/%m/%d"), "%Y/%m/%d")
    d2 = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
    delta = (d2 - d1).days // 365

    response = {
        'details': [
            {'title': 'Canais', 'value': result['channelCount']},
            {'title': 'Membros', 'value': result['memberCount']},
            {'title': 'Staffs', 'value': len(staffs)},
            {'title': 'Anos', 'value': delta},
        ],
        'staffs': staffs,
        'boosters': boosters
    }

    return res(data=response, status=200)