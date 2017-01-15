from flask import Flask , request
from flask_cors import CORS, cross_origin
import json
import psycopg2

app = Flask(__name__)
CORS(app, supports_credentials=True)

#initialization data base
def dbthing(s):
    print s
    conn = psycopg2.connect("dbname='twitter' user='postgres' host='localhost' password='postgres'")
    db = conn.cursor()
    db.execute(s)
    result = db.fetchall()
    conn.close()
    return result

#initialization data base
def dbthing_i(s):
    print s
    conn = psycopg2.connect("dbname='twitter' user='postgres' host='localhost' password='postgres'")
    db = conn.cursor()
    db.execute(s)
    conn.commit()
    conn.close()

#check login and password
@app.route("/login", methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def login():
    asd=request.get_data()
    print "data:" + asd
    traffic = json.loads(asd)
    users = dbthing("SELECT id, login, pasword FROM users  WHERE login = \'" +traffic['login']+"\'") 
    if  len(users) > 0  and (traffic['login'] == users[0][1] and traffic['password'] == users[0][2]):
        return "{ \"logged\" : "+str(users[0][0])+" }"
    else:    
        return "{ \"logged\" : 0 }"

#enter emotional from radiobutton in db
@app.route("/radiobutton", methods=['GET', 'POST', 'OPTIONS'])
def radiobutton():
    userid = request.cookies.get('user_id')
    traffic = json.loads(request.get_data())
    dbthing_i('INSERT INTO apprisal(id_user, id_message, emotional_color, inf_color) VALUES('+userid+','+traffic['message_id']+','+traffic['emo_color']+','+traffic['inf_color']+')')
    return "ok"

#get text from db to lable
@app.route("/getmessage", methods=['GET', 'POST', 'OPTIONS'])
def getmessage():
    userid = request.cookies.get('user_id')
    print userid
    number_message = dbthing('SELECT COUNT(*) FROM apprisal WHERE id_user='+userid)
    results = dbthing('SELECT id, m_text FROM message WHERE id  IN (SELECT id_message FROM apprisal WHERE id_user <> '+userid+' ) ORDER BY RANDOM() LIMIT 1')
    if int(number_message[0][0]) % 2 == 0 or len(results) < 1 :
        results = dbthing('SELECT id, m_text FROM message WHERE id not in (SELECT id_message FROM apprisal) ORDER BY RANDOM() LIMIT 1')
    if len(results) < 1 :
        return ""
    return "{ \"message_id\" :   \""+str(results[0][0])+"\", \"message_text\" : \""+str(results[0][1])+"\" }"

#get object_or_sentiment from db to table
@app.route("/getoos", methods=['GET', 'POST', 'OPTIONS'])
def setmessage():
    message_id = request.cookies.get('id_message')
    results = dbthing('SELECT word FROM emotional_flag WHERE id_message='+message_id+' LIMIT 3')
    oos="{ "
    if (0<len(result)) :
        oos+="\"oos1\" : \""+results[0][0]+"\" , "
    else:
        oos+="\"oos1\" : \"\" , "
    if (1<len(result)) :
        oos+="\"oos2\" : \""+results[1][0]+"\" , "
    else:
        oos+="\"oos2\" : \"\" , "
    if (2<len(result)) :
        oos+="\"oos3\" : \""+results[2][0]+"\""
    else:
        oos+="\"oos3\" : \"\""
    oos+="}"


    return oos
 
#enter emotional, object/sentiment
@app.route("/selectmenu", methods=['GET', 'POST', 'OPTIONS'])
def selectmenu():
    userid = request.cookies.get('user_id')
    traffic2 = json.loads(request.get_data())
    dbthing_i('INSERT INTO  emotional_flag(id_message, object_or_sentiment, emotional_color, word) VALUES('+traffic2['message_id']+', \''+traffic2['object_or_sentiment']+'\', '+traffic2['emotional_color']+', \''+traffic2['lable_object_or_sentiment']+'\')');
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
