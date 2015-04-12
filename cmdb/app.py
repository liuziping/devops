from flask import Flask,url_for,request,render_template,redirect,make_response,session
import MySQLdb as mysql
import json

app = Flask(__name__)
db=mysql.connect(user='reboot',passwd='reboot123',db='liuziping',charset='utf8')
db.autocommit(True)
cur = db.cursor()

#login

@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
	        password = request.form.get('password')
		if username == "admin" and  password=="admin":
			session['username'] = username
			return redirect('/index')
		else:
			return redirect('/login')
	return render_template('login.html')
#logout
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))		
#index
@app.route('/',methods=['GET'])
@app.route('/index',methods=['GET'])
def index():
	if 'username' in session:
		username = session.get('username')
		return render_template('demo.html',username=username)
	else:
		return redirect('/login')
		
#graph
@app.route('/graph',methods=['GET'])
def graph():
	return render_template('highcharts.html',)
#add host
@app.route('/add',methods=['GET'])
def add():
	name = request.args.get('name')
	ip = request.args.get('ip')
	idc = request.args.get('idc')
	return_dict = {'error':1,'msg':''}
	if not name:
		return_dict['msg'] = 'need a name'
		return json.dumps(return_dict)
	if not ip:
		return_dict['msg'] = 'need a ip'
		return json.dumps(return_dict)
        sql="insert into cmdb_test (name,ip,idc) values ('%s','%s','%s')"%(name,ip,idc)
	cur.execute(sql)
	return_dict['error'] = 0
	return json.dumps(return_dict)
#select all 
@app.route('/list',methods=['GET'])
def list():
	cur.execute('select * from cmdb_test')
	str = ""
	for c in cur.fetchall():
		s = '<tr><td>%s</td> \
			<td>%s</td> \
			<td>%s</td> \
			<td>%s</td> \
			<td><span class="update-btn" data-id="%s">update</span></td> \
			<td><span  class="delete-btn" data-id="%s">delete</span></td>  \
			</tr>' % (c[0],c[1],c[2],c[3],c[0],c[0])   #get data and get id for update,delete 
		str = str+s
	return str
#get data from id  for  update
@app.route('/getbyid',methods=['GET'])
def getbyid():
	id = request.args.get('id')
        if not id:
		return "need an id"
	
	sql = "select * from cmdb_test where id=%s" % (id)   
	cur.execute(sql)
	dict = {}
	res=cur.fetchone()
	dict['id']=res[0]
	dict['name']=res[1]
        dict['ip']=res[2]
	return json.dumps(dict)
#update
@app.route('/update',methods=['GET'])
def update():
	name = request.args.get('name')
	ip = request.args.get('ip')
	id = request.args.get('id')
	idc = request.args.get('idc')
	return_dict = {'error':1,'msg':''}
	if not name:
		return_dict['msg'] = 'need a name'
		return json.dumps(return_dict)
	if not ip:
		return_dict['msg'] = 'need a ip'
		return json.dumps(return_dict)
        sql='update  cmdb_test set name="%s",ip="%s",idc="%s" where id="%s"' %(name,ip,idc,id)
	cur.execute(sql)
	return_dict['error'] = 0
	return json.dumps(return_dict)

#delete
@app.route('/delete',methods=['GET'])
def delete():
	id = request.args.get('id')
	if not id:
		return "need an id"
	sql = "delete from cmdb_test where id=%s" % (id)
	cur.execute(sql)
	return 'ok'
#select idc
@app.route('/idc',methods=['GET','POST'])
def idc():
	if request.method != 'GET':
		if 'username' in session:
			username = session.get('username')
			return render_template('idc.html',username)	
		else:
			return redirect('/login')
	else:
		sql = "select  * from idc";
		cur.execute(sql)
		str = ""
		for c in cur.fetchall():
			s = '<option value="%s">%s</option>' % (c[1],c[1])   #get data and get id for update,delete 
	 		str = str+s
		return str
	#return 'ok'

#code manage
@app.route('/code',methods=['GET'])
def code():
	if 'username' in session:
		username = session.get('username')
		return render_template('code.html',username=username)
	else:
		return redirect('/login')
#user manage
@app.route('/user',methods=['GET'])
def user():
	if 'username' in session:
		username = session.get('username')
		return render_template('user.html',username=username)
	else:
		return redirect('/login')
#up manage
@app.route('/up',methods=['GET'])
def up():
	if 'username' in session:
		username = session.get('username')
		return render_template('up.html',username=username)
	else:
		return redirect('/login')


#select  cabinet 
#@app.route('')
#main
if __name__=='__main__':
        # set the secret key.  keep this really secret:
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host='0.0.0.0',port=9199,debug=True)
