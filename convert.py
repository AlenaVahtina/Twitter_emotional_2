import json
import sqlite3

traffic = json.load(open('xxx.json'))
db = sqlite3.connect("tw.db")
items = traffic['list_docs']
c = db.cursor()
for someitem in items:
	id_message_py="select id from message where m_text=?";
	c.execute(id_message_py,(someitem['text'],))

	if c.fetchone() is not None:
		query = "insert into message (m_text) values (?)"
		keys = (someitem['text'],)
		c.execute(query, keys)
		db.commit()

	if len(someitem.keys())==3:
		c.execute(id_message_py,(someitem['text'],))
		id_message=c.fetchone()[0]

		query = "insert into apprisal(id_user, id_message, emotional_color) values (?,?,?)"
		keys = (someitem['user_id'],id_message, someitem['mark'])
		c.execute(query, keys)

c.close()

