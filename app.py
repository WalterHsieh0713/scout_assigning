from flask import Flask, request
import requests

app = Flask(__name__)

global_scout_count = 0
global_match_count = 0

def getScoutCount():
    return global_scout_count
def getMatchCount():
    return global_match_count
def addScoutCount():
    global global_scout_count
    global_scout_count = global_scout_count + 1
def addMatchCount():
    global global_match_count
    global_match_count = global_match_count + 1

def send_discord_notification(message):
    webhook_url = 'INSERT_DISCORD_WEBHOOK_URL'
    data = {
        'content': message,
    }
    requests.post(webhook_url, json=data)

@app.route('/', methods=['POST'])

def root():
    num_to_scout = 4           #change to control number of teams to scout
    scouter_ID = [
        "1014114774818226197", #ALEX
        "1147797652747079713", #BARNETT
        "915223123681505290",  #BENJAMIN
        "716094833890033774",  #LUKE
        "888711983489232946",  #MATT
        "960825266765176862",  #RAYMOND
    ]
    exclude = [
        # add teams to not scout (RANK 30 - 35) on Day 2
    ]
    data = request.get_json()
    message_type = data.get('message_type', '')
    message_data = data.get('message_data', {})

    if message_type == 'verification':
        verification_key = message_data.get('verification_key', '')
        print("Verification Key: ", verification_key)

    elif message_type == 'upcoming_match':
        event_key = message_data.get('event_key')
        match_key = ('match_key')
        match_num = match_key.replace(f"{event_key}_", '')
        match_type = "QUALS"
        team_keys = message_data.get('team_keys')
        if "qm" in match_num:
            match_num = match_num.replace("qm", "")
        elif "sf" in match_num:
            match_num = match_num.replace("sf", "").replace("m1", "")
            match_type = "SEMIFINALS"
        elif "f" in match_num:
            match_num = match_num.replace("m1f", "")
            match_type = "FINALS"
        rows = [
            f":mega: UPCOMING (~7min): {match_type} MATCH {match_num} SCOUTERS :mega:",
        ]
        temp = 0
        for team in team_keys:
            if temp >= num_to_scout:
                break
            if team[3:] not in exclude:
                rows.append(f"<@!{scouter_ID[getScoutCount() % 6]}> - {team[3:]} ")
                print(getScoutCount())
                addScoutCount()
                temp = temp + 1
        rows.append("")
        addMatchCount()
        send_discord_notification("\n".join(rows))

    elif message_type == "ping":
        print("PING")
    return '', 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Run the Flask app on port 8000





    # elif message_type == 'match_score':
    #     event_key = message_data.get('event_key', '')
    #     match_key = message_data.get('match_key', '')
    #     blue_score = message_data.get('match').get('alliances').get('blue').get('score')
    #     red_score = message_data.get('match').get('alliances').get('red').get('score')
    #     print("Event: ", event_key)
    #     print("Match: ", match_key)
    #     print("Scores ", blue_score, " - ", red_score)
    #     rows = [
    #         "SCORE UPDATE",
    #         f"Event: {event_key}",
    #         f"Match: {match_key}",
    #         f":blue_square: {blue_score} - {red_score} :red_square:"
    #     ]
    #     send_discord_notification("\n".join(rows))
