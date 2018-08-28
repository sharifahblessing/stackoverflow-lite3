import json

class User_model:
    def __init__(self, userid, name, username, password):
        self.userid = userid
        self.name = name
        self.username = username
        self.password = password
    

    def my_json(self):
        return json.dumps({
            'userid':self.userid,
            'name':self.name,
            'username':self.username,
            'password':self.password,
    
        })

class Question_model:
    def __init__(self, questionid, title, body, tag, postedby, time):
        self.questionid = questionid
        self.title = title
        self.body = body
        self.tag = tag
        self.postedby = postedby
        

    def my_json(self):
        return json.dumps({
            'questionid':self.questionid,
            'title':self.title,
            'body':self.body,
            'tag':self.tag,
            'postedby':self.postedby,
            
        })


class Answer_model:
    def __init__(self, answerid, content , questionid):
        self.answerid = answerid
        self.content = content
        self.questionid = questionid
      

    def my_json(self):
        return json.dumps({
            'answerid':self.answerid,
            'content':self.content,
          
        })
