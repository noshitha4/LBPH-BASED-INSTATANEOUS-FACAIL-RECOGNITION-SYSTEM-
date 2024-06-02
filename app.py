import pickle
import winsound
from PIL import Image
from flask import Flask, render_template, request, session, redirect, url_for, flash,send_file
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from datetime import datetime,timezone
import cv2
import os
import numpy as np
import csv
import datetime
from sklearn.preprocessing import LabelEncoder
from flask import render_template, redirect, url_for, session
import cv2
import pickle
import pandas as pd
import datetime,time

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

import mysql.connector
db = mysql.connector.connect(
    user="root", password="", port=3306, database='messmanagement_db')
cur = db.cursor()

app = Flask(__name__)
app.secret_key = 'sfcyub76323rhwefewfwe1f234654csdcvksduy'

#home page
@app.route("/")
def index():
    return render_template("index.html")

#Admin login
@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == "noshitha4@gmail.com" and password == "admin":
            return render_template("adminhome.html", username="admin")
        else:
            msg = "Credentials are not Vlaid"
            return render_template("adminlogin.html", msg=msg)
    return render_template("adminlogin.html")


@app.route("/deleteuser/<id>")
def deleteuser(id=0):
    sql="delete from userinfo where id='"+id+"'"
    cur.execute(sql)
    sql1="delete from food_bill where id='"+id+"'"
    cur.execute(sql1)
    sql2="delete from feedback where id='"+id+"'"
    cur.execute(sql2)
    sql3="delete from payment where id='"+id+"'"
    cur.execute(sql3)
    db.commit()
    flash("data deleted",'success')
    return redirect(url_for('viewuser'))

#Add Users
@app.route("/adduser", methods=["POST", "GET"])
def adduser():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        address = request.form['address']
        if password == confirmpassword:
            sql = "select * from userinfo where Id='%s' and Password='%s'" % (
                id, password)
            cur.execute(sql)
            d = cur.fetchall()
            db.commit()
            if d == []:
                sql = "insert into userinfo(Id,Name,Email,Contact,Password,address) values('%s','%s','%s','%s','%s','%s')" % (
                    id,name, email, contact, password,address)
                cur.execute(sql)
                db.commit()
                content = "Username : " + id + "  Password : " + password
                sender_address = 'noshitha4@gmail.com'
                sender_pass = 'ngviyygsksvfiiaf'
                receiver_address = email
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = email
                message['Subject'] = "Smart Mess Management System"
                message.attach(MIMEText(content, 'plain'))
                ss = smtplib.SMTP('smtp.gmail.com', 587)
                ss.starttls()
                ss.login(sender_address, sender_pass)
                text = message.as_string()
                ss.sendmail(sender_address, receiver_address, text)
                ss.quit()
                msg = "Information Addedd Successfuly"
                return render_template("adduser.html", msg=msg)
            else:
                msg = "Details already Exists"
                return render_template("adduser.html", msg=msg)
        else:
            msg = "Password Not Matched"
            return render_template("adduser.html", msg=msg)
    return render_template("adduser.html")


#view users
@app.route("/viewuser")
def viewuser():
    sql = "select Id,Name,Email,Contact,Address,train_status from userinfo where Status='Accepted' and train_status IN ('pending','Completed')"
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return render_template('viewusers.html', data=data)


#train data
@app.route("/traindata/<id>")
def traindata(id=0):
    le = LabelEncoder()
    faces, Id = getImagesAndLabels("TrainingImage")
    Id = le.fit_transform(Id)
    output = open('label_encoder.pkl', 'wb')
    pickle.dump(le, output)
    output.close()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(Id))
    recognizer.save("Trained_Model/Trainner.yml")
    sql="update userinfo set train_status='Completed' where Id='"+id+"'"
    cur.execute(sql)
    db.commit()
    flash("Model Trained Successfully", "success")
    return redirect(url_for('viewuser'))

#login to user
@app.route("/userlogin", methods=["POST", "GET"])
def userlogin():
    if request.method == "POST":
        id = request.form['id']
        password = request.form['password']
        sql = "select * from userinfo where Id='%s' and Password='%s'" % (
            id, password)
        cur.execute(sql)
        dat = cur.fetchall()
        db.commit()
        if dat == []:
            msg = "Invalid Credentials"
            return render_template("userlogin.html", msg=msg)
        else:
            id =dat[0][0]
            name = dat[0][1]
            email = dat[0][2]
            session['userid'] = id
            session['username'] = name
            session['useremail'] = email
            msg = "Welcome {}".format(name)
            return render_template("userhome.html", msg=msg)
    return render_template("userlogin.html")

#view profile
@app.route("/viewprofile")
def viewprofile():
    sql = "select Id,Name,Email,Contact,Address,Status from userinfo where Id='%s'" % (session['userid'])
    data = pd.read_sql_query(sql, db)
    
    status=data.values[0][5]
    return render_template('viewprofile.html', cols=data.columns.values, rows=data.values.tolist(),status=str(status))

#active the users
@app.route("/activatewebcam/<c>")
def activatewebcam(c=0):
    
    sql = "select Id,Name,Email from userinfo where Id='%s'" % (c)
    cur.execute(sql)
    dat = cur.fetchall()
    db.commit()
    #print(dat)
    id=dat[0][0]
    name = dat[0][1]
    Email = dat[0][2]
    cam = cv2.VideoCapture(0)
    harcascadePath = r"haarcascade\haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    sampleNum = 0
    (width, height) = (200, 200)  
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # incrementing sample number
            sampleNum = sampleNum + 1
            face_resize = cv2.resize(faces, (width, height)) 
            # saving the captured face in the dataset folder TrainingImage
            cv2.imwrite("TrainingImage/" + name +
                        "." + str(id) + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
            # display the frame
        else:
            cv2.imshow('frame', img)
            # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
            # break if the sample number is morethan 100
        elif sampleNum > 200:
            break
    cam.release()
    cv2.destroyAllWindows()
    res = "Roll Number : " + str(id) + " Name : " + name + "Email : " + Email
    row = [id, name, Email]
    with open('person_details\person_details.csv', 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    sq="update userinfo set Status='Accepted' where Id='"+c+"'"
    cur.execute(sq)
    db.commit()
    msg = "Your Image was Captured "
    return redirect(url_for("viewprofile", msg=msg))


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST':
        year = request.form['year']
        month = request.form['month']
        s="SELECT SUM(Amount) AS TotalAmount FROM food_bill  where Id='"+session['userid']+"' and status='pending'";
        cur.execute(s,db)
        totalcost=cur.fetchall()[0][0]
        return render_template('paybill.html',month=month,year=year,totalcost=totalcost)
       
    return render_template("payment.html")

@app.route('/payment_view')
def payment_view():
    sql="select * from payment where Id='"+session['userid']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('payment_view.html' , data=data)

@app.route('/paybill', methods=['POST','GET'])
def paybill():
    if request.method=="POST":
        year = request.form['year']
        month = request.form['month']
        cardnumber = request.form['cardnumber']
        cardname = request.form['cardname']
        amount = request.form['amount']
        dateInput = request.form['dateInput']
        cvv = request.form['cvv']
        import datetime
        current_datetime = datetime.datetime.now()
        current_date = current_datetime.date()
        print(current_date)
        sql="insert into payment(Id,Name,Email,CardName,CardNo,CVV,Date,Payed_date,Amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(session['userid'],session['username'],session['useremail'],cardname,cardnumber,cvv,dateInput,current_date,amount)
        cur.execute(sql,val)
        db.commit()
        sq="update food_bill set status='Completed' where Id='"+session['userid']+"'"
        cur.execute(sq,db)
        db.commit()
        msg="Payment completed successfully"
        return render_template('payment.html', msg=msg)
    return render_template('payment.html')

@app.route("/viewpayment")
def viewpayment():
    sql = "SELECT * FROM payment" 
    data = pd.read_sql_query(sql, db)
    print(data)
    return render_template("viewpayment.html", cols=data.columns.values, rows=data.values.tolist())


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = str(os.path.split(imagePath)[-1].split(".")[0])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

@app.route('/goto_mess')
def goto_mess():
    return  render_template('mess.html')

@app.route('/viewbill',methods=['POST','GET'])
def viewbill():
    if request.method=="POST":
        user_input=request.form['user_input']
        sq="SELECT * FROM food_bill where Date='"+user_input+"' or Month='"+user_input+"' and Id='"+session['userid']+"'";
        cur.execute(sq)
        data=cur.fetchall()
        s="SELECT SUM(Amount) AS TotalAmount FROM food_bill where Date='"+user_input+"' or Month='"+user_input+"' and Id='"+session['userid']+"'";
        cur.execute(s,db)
        totalcost=cur.fetchall()[0][0]
        return render_template('viewbill.html',data=data,totalcost=totalcost)
    

    sql="SELECT * FROM food_bill where Id='"+session['userid']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    sql1="SELECT SUM(Amount) AS TotalAmount FROM food_bill where Id='"+session['userid']+"'"
    cur.execute(sql1,db)
    totalcost=cur.fetchall()[0][0]
    print("total cost: ",totalcost)
    return render_template('viewbill.html',data=data,totalcost=totalcost)


@app.route('/view_foodbill',methods=['POST','GET'])
def view_foodbill():
    if request.method=="POST":
        user_input=request.form['user_input']
        food_type=request.form['food_type']
        sq="SELECT * FROM food_bill where Date='"+user_input+"' or Month='"+user_input+"' and Food_Type='"+food_type+"' ";
        cur.execute(sq)
        data=cur.fetchall()
        s="SELECT SUM(Amount) AS TotalAmount FROM food_bill where Date='"+user_input+"' or Month='"+user_input+"' and Food_Type='"+food_type+"'";
        cur.execute(s,db)
        totalcost=cur.fetchall()[0][0]
        # print(data)
        return render_template('foodbill.html',data=data,totalcost=totalcost)
    

    sql="SELECT * FROM food_bill where Id='"+session['userid']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    sql1="SELECT SUM(Amount) AS TotalAmount FROM food_bill where Id='"+session['userid']+"'"
    cur.execute(sql1,db)
    totalcost=cur.fetchall()[0][0]
    print(data)
    print("total cost: ",totalcost)
    return render_template('foodbill.html',data=data,totalcost=totalcost)

@app.route('/feedback', methods=['POST','GET'])
def feedback():
    if request.method=='POST':
        feedback = request.form['feedback']
        sql="insert into feedback(Id,Name,Email,feedback) values(%s,%s,%s,%s)"
        val=(session['userid'],session['username'],session['useremail'],feedback)
        cur.execute(sql,val)
        msg="Your feedback submitted"
        return  render_template('feedback.html',msg=msg)
    return render_template('feedback.html')

@app.route('/feedback_view')
def feedback_view():
    sql="select * from feedback where Id='"+session['userid']+"'"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('feedback_view.html',data=data)


@app.route('/viewfeedback')
def viewfeedback():
    sql="select * from feedback "
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('viewfeedback.html',data=data)

@app.route('/view_payment')
def view_payment():
    sql="select * from payment"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('view_payment.html',data=data)

@app.route('/foodbill')
def foodbill():
    sql="select * from food_bill"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('foodbill.html', data=data)
@app.route("/TrackImages", methods=['GET','POST'])
def TrackImages():
    if request.method=='POST':
        d1=request.form['d1']
        food_type=request.form['food_type']
        from datetime import datetime
        date_obj = datetime.strptime(d1, '%Y-%m-%d')
        month_name = date_obj.strftime('%B')
        date_object = datetime.strptime(d1, "%Y-%m-%d")
        year = date_object.year
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("Trained_Model\Trainner.yml")
        harcascadePath = "Haarcascade\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Load the label encoder
        pkl_file = open('label_encoder.pkl', 'rb')
        le = pickle.load(pkl_file)
        pkl_file.close()

        # Load the DataFrame

        # Open the camera
        cam = cv2.VideoCapture(0)

        flag = 0
        global det
        det = 0
         
        while True:
            _, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                print(conf)
                if conf < 50:
                    tt = le.inverse_transform([Id])[0]
                    r1 = str(tt)
                    print(r1)
                    print(type(r1))
                    det +=1
                    df = pd.read_csv(r"person_details/person_details.csv")
                    data = df[df['username'] == r1]
                    print(data)
                    email = data['Email']
                    print(email)
                    user_email= list(email)
                    print(user_email)
                    user_email=user_email[0]
                    id=data['id']
                    print(id)
                    user_id=list(id)
                    print(user_id)
                    user_id = user_id[0]
                    if det==20:
                        ts = time.time()
                        timeStamp = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        if food_type=='Break Fast':
                            amount=40
                        else:
                            amount=80
                        sq="select count(*) from food_bill where Date='"+d1+"' and Month='"+month_name+"' and Food_Type='"+food_type+"' and Id='"+user_id+"'"
                        foodtype_count=pd.read_sql_query(sq,db)
                        foodtype_count=foodtype_count.values[0][0]
                        if foodtype_count!=0:
                            msg="already data taken"
                            return render_template('mess.html',msg=msg)
                        sql="insert into food_bill(Id,Name, Email, Food_Type, Date, Month, Year, Time, Amount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        val=(user_id,r1, user_email, food_type, d1, month_name, year, timeStamp, amount)
                        cur.execute(sql,val)
                        db.commit()
                        cam.release()
                        cv2.destroyAllWindows()
                        msg="Bill generated Successfully"
                        return render_template('mess.html', msg=msg)


                else:
                    tt = 'Unknown'
                    flag += 1
                    print(tt)
                    frequency = 2000
                    duration = 3000
                    winsound.Beep(frequency, duration)
                    content="Unkonwn person entered into your mess."
                    sender_address = 'noshitha4@gmail.com'
                    sender_pass = 'ngviyygsksvfiiaf'
                    receiver_address = sender_address
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = sender_address
                    message['Subject'] = "Smart Mess Management System"
                    message.attach(MIMEText(content, 'plain'))
                    ss = smtplib.SMTP('smtp.gmail.com', 587)
                    ss.starttls()
                    ss.login(sender_address, sender_pass)
                    text = message.as_string()
                    ss.sendmail(sender_address, receiver_address, text)
                    ss.quit()
                    cam.release()
                    cv2.destroyAllWindows()
                    msg="Unknown person"
                    return render_template('mess.html', msg=msg)
                cv2.putText(frame, tt, (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('im', frame)
            if cv2.waitKey(3) == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()

    # Redirect to a different route or return a response as needed
    return redirect(url_for('goto_mess'))

# @app.route('/payment')
# def payment():
#     return render_template('payment.html')


@app.route("/userlogout")
def userlogout():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
