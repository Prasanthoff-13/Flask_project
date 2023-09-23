from flask import *
from flask_mysqldb import MySQL
from flask_session import *
app = Flask(__name__)
app.config['SESSIONS_PERMANENT']=False
app.config['SESSION_TYPE']='filesystem'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='library_db'
app.config['MYSQL_CURSORCLASS']="DictCursor"
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('login.html')
# LOGIN PROCESS
@app.route('/dlogin',methods=['GET','POST'])
def dlogin():
    if request.method == "POST":
        u_name = request.form['u_name']
        pwd = request.form['password']
        con = mysql.connection.cursor()
        con.execute("select * from user where u_name=%s and password=%s;", [u_name, pwd])
        val = len(con.fetchall())
        con.close()
        if val == 1:
            session["name"] = u_name
            return redirect(url_for('dash'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('index'))
# Register process
@app.route('/dregister',methods=['GET','POST'])
def dregister():
    if request.method=="POST":
        u_name = request.form['u_name']
        email=request.form['email']
        pwd=request.form['password']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO user(u_name,email,password) values (%s,%s,%s);",(u_name,email,pwd))
        mysql.connection.commit()
        con.close()
        return redirect(url_for('login'))
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/logout')
def logout():
    session["name"] = None
    return redirect("/login")
@app.route('/dashboard')
def dash():
    con = mysql.connection.cursor()
    con.execute("select * from books;")
    a = len(con.fetchall())
    con.execute("select * from user;")
    b =len(con.fetchall())
    con.execute("select * from issue;")
    c = len(con.fetchall())
    con.execute("select * from transaction;")
    d = len(con.fetchall())
    con.close()
    if not session.get("name"):
        return redirect("/login")
    return render_template('dashboard.html',bc=a,uc=b,ic=c,tc=d)


@app.route('/profile')
def profile():
    if not session.get("name"):
        return redirect("/login")
    return render_template('profile.html')
@app.route('/books')
def books():
    con = mysql.connection.cursor()
    con.execute("select * from books;")
    x = con.fetchall()
    if not session.get("name"):
        return redirect("/login")
    return render_template('Books.html',data=x)
@app.route('/issuebook')
def issuebooks():
    con = mysql.connection.cursor()
    con.execute("select * from issue;")
    x = con.fetchall()
    if not session.get("name"):
        return redirect("/login")
    return render_template('IssueBooks.html',data=x)
@app.route('/transaction')
def transaction():
    con = mysql.connection.cursor()
    con.execute("select * from transaction")
    x = con.fetchall()
    if not session.get("name"):
        return redirect("/login")
    return render_template('Transaction.html', data=x)
@app.route('/userlist')
def userlist():
    con = mysql.connection.cursor()
    con.execute("select * from user;")
    x = con.fetchall()
    if not session.get("name"):
        return redirect("/login")
    return render_template('userlist.html',data=x)
@app.route('/ebooks/<string:idr>',methods=['GET','POST'])
# edit books
def ebooks(idr):
    con = mysql.connection.cursor()
    con.execute("select * from books where b_id=%s;",idr)
    x = con.fetchone()
    if not session.get("name"):
        return redirect("/login")
    return render_template('editbooks.html',idr=x)
@app.route('/eissuebook/<string:idr>',methods=['GET','POST'])
# edit issue
def eisuuebook(idr):
    con = mysql.connection.cursor()
    con.execute("select * from issue where is_id=%s;",idr)
    x = con.fetchone()
    if not session.get("name"):
        return redirect("/login")
    return render_template('editissues.html',idr=x)
@app.route('/etransaction/<string:idr>',methods=['GET','POST'])
def etransaction(idr):
    con = mysql.connection.cursor()
    con.execute("select * from transaction where t_id=%s",idr)
    x = con.fetchone()
    if not session.get("name"):
        return redirect("/login")
    return render_template('edittransaction.html',idr=x)
@app.route('/euserlist/<string:idr>',methods=['GET','POST'])
def euserlist(idr):
    con = mysql.connection.cursor()
    con.execute("select * from user where u_id=%s",idr)
    x = con.fetchone()
    if not session.get("name"):
        return redirect("/login")
    return render_template('editusers.html', idr=x)
@app.route('/updatebook',methods=['GET','POST'])
# update book
def updatebook():
    if request.method=="POST":
        idr = request.form['bid']
        name = request.form['bname']
        author = request.form['author']
        qnt = request.form['quantity']
        con = mysql.connection.cursor()
        con.execute("update books set b_id=%s,b_name=%s,author=%s,quantity=%s where b_id=%s;",(idr,name,author,qnt,idr))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('books'))
@app.route('/updateissue',methods=['GET','POST'])
#update issue
def updateissue():
    if request.method=="POST":
        idr = request.form['is_id']
        name = request.form['is_name']
        book = request.form['is_book']
        idate = request.form['is_date']
        edate = request.form['ex_date']
        rdate = request.form['re_date']
        con = mysql.connection.cursor()
        con.execute("update issue set is_id=%s,is_user=%s,is_book=%s,is_date=%s,ex_date=%s,re_date=%s where is_id=%s;",(idr,name,book,idate,edate,rdate,idr))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('issuebooks'))
@app.route('/updatetrans',methods=['GET','POST'])
# update transaction
def updatetrans():
    if request.method=="POST":
        idr = request.form['t_id']
        name = request.form['t_name']
        book = request.form['t_book']
        due = request.form['due']
        sta = request.form['status']
        con = mysql.connection.cursor()
        con.execute("update transaction set t_id=%s,t_user=%s,t_book=%s,due=%s,status=%s where t_id=%s;",(idr,name,book,due,sta,idr))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('transaction'))
@app.route('/updateuser',methods=['GET','POST'])
# update user
def updateuser():
    if request.method=="POST":
        idr = request.form['uid']
        name = request.form['uname']
        email=request.form['uemail']
        pwd=request.form['password']
        con = mysql.connection.cursor()
        con.execute("update user set u_id=%s,u_name=%s,email=%s,password=%s where u_id=%s;",(idr,name,email,pwd,idr))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('userlist'))
@app.route('/deletebook/<string:idr>', methods=['GET', 'POST'])
# delete book
def deletebook(idr):
    con = mysql.connection.cursor()
    con.execute("delete from books where b_id=%s",idr)
    mysql.connection.commit()
    con.close()
    if not session.get("name"):
        return redirect("/login")
    return redirect(url_for('books'))
@app.route('/deleteuser/<string:idr>',methods=['GET','POST'])
# delete user
def deleteuser(idr):
    con = mysql.connection.cursor()
    con.execute("delete from user where u_id=%s;",idr)
    mysql.connection.commit()
    con.close()
    if not session.get("name"):
        return redirect("/login")
    return redirect(url_for('userlist'))
@app.route('/deleteissue/<string:idr>',methods=['GET','POST'])
# delete issue
def deleteissue(idr):
    con = mysql.connection.cursor()
    con.execute("delete from issue where is_id=%s;",idr)
    mysql.connection.commit()
    con.close()
    if not session.get("name"):
        return redirect("/login")
    return redirect(url_for('issuebooks'))
@app.route('/deletetrans/<string:idr>',methods=['GET','POST'])
# delete Transaction
def deletetrans(idr):
    con = mysql.connection.cursor()
    con.execute("delete from transaction where t_id=%s",idr)
    mysql.connection.commit()
    con.close()
    if not session.get("name"):
        return redirect("/login")
    return redirect(url_for('transaction'))
@app.route('/addbook',methods=['GET','POST'])
# add book
def addbook():
    if request.method == "POST":
        idr = request.form['bid']
        name = request.form['bname']
        author = request.form['author']
        qnt = request.form['quantity']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO books(b_id,b_name,author,quantity) values (%s,%s,%s,%s);", (idr,name,author,qnt))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('books'))
@app.route('/addissue',methods=['GET','POST'])
# add issue
def addissue():
    if request.method == "POST":
        idr = request.form['is_id']
        name = request.form['is_name']
        book = request.form['is_book']
        idate = request.form['is_date']
        edate = request.form['ex_date']
        rdate = request.form['re_date']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO issue(is_id,is_user,is_book,is_date,ex_date,re_date) values (%s,%s,%s,%s,%s,%s);",(idr,name,book,idate,edate,rdate))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('issuebooks'))
@app.route('/addtrans',methods=['GET','POST'])
def addtrans():
    if request.method == "POST":
        idr = request.form['t_id']
        name = request.form['t_name']
        book = request.form['t_book']
        due = request.form['due']
        sta = request.form['status']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO transaction(t_id,t_user,t_book,due,status) values (%s,%s,%s,%s,%s)",(idr,name,book,due,sta))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('transaction'))
@app.route('/adduser',methods=['GET','POST'])
#adduser
def adduser():
    if request.method=="POST":
        idr = request.form['uid']
        name = request.form['uname']
        email=request.form['uemail']
        pwd=request.form['password']
        con = mysql.connection.cursor()
        con.execute("INSERT INTO user(u_id,u_name,email,password) values (%s,%s,%s,%s);",(idr,name,email,pwd))
        mysql.connection.commit()
        con.close()
        if not session.get("name"):
            return redirect("/login")
        return redirect(url_for('userlist'))
if __name__=='__main__':
    app.secret_key = 'pr1234'
    app.run(debug=True)

