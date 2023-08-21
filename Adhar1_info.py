from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
# Establish the connection
conn = sqlite3.connect('adharcard.db')
cursor = conn.cursor()

# Creating table
cursor.execute('''CREATE TABLE IF NOT EXISTS ADHAR 
               (adhar_no INTEGER PRIMARY KEY NOT NULL,
               name VARCHAR(30),
               age INTEGER,
               mobile_no INTEGER,
               dob DATE,
               email_id TEXT,
               gender VARCHAR(6),
               address TEXT,
               dose INTEGER
               )''')
print("Table created successfully")




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enterdata')
def new_data():
    return render_template('covid.html')


@app.route('/insertdata', methods=['POST','GET'])
def insertdata():
 
    msg = ""
    if request.method == 'POST':
        
        try:
            adhar_no = request.form['adhar_no']
            name = request.form['name']
            age = request.form['age']
            mobile_no = request.form['mobile_no']
            dob = request.form['dob']
            email_id = request.form['email_id']
            gender = request.form['gender']
            address = request.form['address']
            dose = request.form['dose']
            with sqlite3.connect('adharcard.db') as conn:
             cursor = conn.cursor()
            # Inserting values
             cursor.execute('''INSERT INTO ADHAR (adhar_no, name, age, mobile_no, dob, email_id, gender, address, dose)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (adhar_no, name, age, mobile_no, dob, email_id, gender, address, dose))
             conn.commit()
             msg = 'Data added successfully '
        except:
            conn.rollback()
            msg = "Error. Adhar number already exists."
            
        finally:
           # return render_template("result.html", msg=msg)
           print("msg value:", msg)
           return render_template("result.html", msg=msg)

@app.route('/enteradharno')
def enter_aadhar():
   return render_template('enter_aadhar.html')

    
#@app.route('/viewdata/<int:aadhar_no>')
#def view(aadhar_no):
 #   conn = sqlite3.connect('adharcard.db')
  #  conn.row_factory= sqlite3.Row
  #  cursor = conn.cursor() 
  #  cursor.execute('SELECT * FROM ADHAR WHERE adhar_no = ?', (aadhar_no,))
  #  result = cursor.fetchone()
  #  return render_template("viewdata.html", result=result)
  
@app.route('/viewcontent')
def viewcontent():
   return render_template('viewdata.html')
  

@app.route('/viewdata',methods=['POST'])
def viewdata():
    adhar_no = request.form['adhar_no']
    conn = sqlite3.connect('adharcard.db')
    conn.row_factory= sqlite3.Row
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM ADHAR WHERE adhar_no = ?', (adhar_no,))
    result = cursor.fetchone()
    return render_template("viewdata.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
