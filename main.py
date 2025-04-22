from flask import Flask, redirect, url_for, request, render_template, session, flash
from flask import Flask, request, jsonify  # Ensure jsonify is imported
import mysql.connector
from mysql.connector import Error
from datetime import datetime,timedelta
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app = Flask(__name__, template_folder='template')
app.secret_key = "123456"

# Configure upload folder and size limit
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

def allowed_file(filename):
    """Check if a file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Create a database connection."""
    global connection
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='agroconnect',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/AboutUs')
def aboutus():
      return render_template('about.html')

@app.route('/admin_home')
def admin_home():
      return render_template('admin_home.html')

@app.route('/farmer_home')
def farmer_home():
      return render_template('farmer_home.html')


@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        pwd = request.form.get('password')

        # Get a new database connection
        connection = get_db_connection()
        if connection is None:
            return render_template('login.html', error="Database connection error.")

        mycursor = connection.cursor(buffered=True)
        try:
            query = "SELECT * FROM login WHERE username=%s AND password=%s"
            mycursor.execute(query, (uname, pwd))
            result = mycursor.fetchone()

            if result:
                reg_id = result[1]  # Assuming the second column is user ID
                session['userid'] = reg_id
                
                
                user_role = result[4]  # Assuming the fifth column is the user role
                
                if user_role == 'admin':
                    return render_template('admin_home.html')
                elif user_role == 'customer':
                    return render_template('customer_home.html')
                elif user_role == 'farmer':
                    return render_template('farmer_home.html')
                elif user_role == 'landowner':
                    return render_template('landowner_home.html')

            return render_template('login.html', error="Invalid username or password.")
        finally:
            mycursor.close()  # Ensure cursor is closed
            connection.close()  # Close the connection
    return render_template('login.html')

@app.route('/Customer')
def customer():
      connection = get_db_connection()
      mycursor = connection.cursor()
      query="SELECT * from area"
      mycursor.execute(query)
      area_obj=mycursor.fetchall()
      mycursor.close()
      return render_template('customer_registration.html',area_obj=area_obj)



@app.route('/contact')
def contact():
      return render_template('contact.html')

@app.route('/customer_home')
def customer_home():
      return render_template('customer_home.html')

@app.route('/landowner_home')
def landowner_home():
      return render_template('landowner_home.html')

@app.route('/customer_reg', methods=['GET', 'POST'])
def customer_reg():
    connection = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('cname')
        area = request.form.get('area')
        address = request.form.get('address')
        adhaar = request.form.get('adhaar')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        account_holder_name = request.form.get('account_holder_name')
        account_no = request.form.get('account_no')
        ifsc_code = request.form.get('ifsc_code')
        branch_name = request.form.get('branch_name')
        user_type = "customer"
        date = datetime.now()

        cursor = connection.cursor()

        

        # ✅ Check if Adhaar is already registered
        cursor.execute("SELECT * FROM customers WHERE adhaar = %s", (adhaar,))
        if cursor.fetchone():
            flash("This Adhaar number is already registered!", "error")
            return redirect(url_for('customer_reg'))
        
        # ✅ Check if Email is already registered
        cursor.execute("SELECT * FROM customers WHERE email = %s", (email,))
        if cursor.fetchone():
            flash("This Email is already registered!", "error")
            return redirect(url_for('customer_reg'))

        # ✅ If No Duplicates, Insert Data
        mySql_insert_query = """INSERT INTO customers(area_id, customer_name, address, adhaar, mobileno, email, account_holder_name, account_no, IFSC_code, branch_name, reg_date)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(mySql_insert_query, (area, name, address, adhaar, mobile, email,account_holder_name, account_no, ifsc_code, branch_name, date))
        connection.commit()
        row_id = cursor.lastrowid

        # ✅ Insert into Login Table
        my_log_qry = "INSERT INTO login(username, password, reg_id, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(my_log_qry, (email, password, row_id, user_type))
        connection.commit()

        flash("Record inserted successfully", "success")
        cursor.close()
        return redirect(url_for('login'))

    else:
        mycursor = connection.cursor()
        query = "SELECT * from area"
        mycursor.execute(query)
        area_obj = mycursor.fetchall()
        return render_template("customer_registration.html", area_obj=area_obj)



@app.route('/Land-Owner')
def landowner():
      connection = get_db_connection()
      mycursor = connection.cursor()
      query="SELECT * from area"
      mycursor.execute(query)
      area_obj=mycursor.fetchall()
      mycursor.close()
      return render_template('landowner_registration.html',area_obj=area_obj)


@app.route('/landowner_reg', methods=['GET', 'POST'])
def landowner_reg():
    connection = get_db_connection()
    if request.method == 'POST':
        name = request.form.get('name')
        area = request.form.get('area')
        address = request.form.get('address')
        adhaar = request.form.get('adhaar')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        account_holder_name = request.form.get('account_holder_name')
        account_no = request.form.get('account_no')
        ifsc_code = request.form.get('ifsc_code')
        branch_name = request.form.get('branch_name')
        file = request.files['upload']  # Get the uploaded file

        if file:
            filename = secure_filename(file.filename)  # Ensure the filename is safe
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file

        status = "Register"
        user_type = "landowner"
        
        date = datetime.now()

        mySql_insert_query = """INSERT INTO  land_owners(area_id,landowner_name,address,adhaar,mobile,email,reg_date,upload,account_holder_name, account_no, IFSC_code, branch_name, status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query, (area, name, address,adhaar, mobile, email, date, filename, account_holder_name, account_no, ifsc_code, branch_name, status))
        connection.commit()
       
        row_id = cursor.lastrowid

        my_log_qry = "INSERT INTO login(username, password, reg_id, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(my_log_qry, (email, password, row_id, user_type))
        connection.commit()

        flash("Record inserted successfully")
        cursor.close()
        return redirect(url_for('login'))
    
    else:
        mycursor = connection.cursor()
        query = "SELECT * from area"
        mycursor.execute(query)
        area_obj = mycursor.fetchall()
        return render_template("landowner_registration.html", area_obj=area_obj)
    

@app.route('/Farmer')
def farmer():
      connection = get_db_connection()
      mycursor = connection.cursor()
      query="SELECT * from area"
      mycursor.execute(query)
      area_obj=mycursor.fetchall()
      mycursor.close()
      return render_template("farmer_registration.html",area_obj=area_obj); 
  

@app.route('/farmer_reg', methods=['GET', 'POST'])
def farmer_reg():
    connection = get_db_connection()
    if request.method == 'POST':
        fname = request.form.get('name')
        area = request.form.get('area')
        address = request.form.get('address')
        adhaar = request.form.get('adhaar')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        account_holder_name = request.form.get('account_holder_name')
        account_no = request.form.get('account_no')
        ifsc_code = request.form.get('ifsc_code')
        branch_name = request.form.get('branch_name')
        file = request.files['upload']  # Get the uploaded file
        password = request.form.get('password')

        if file:
            filename = secure_filename(file.filename)  # Ensure the filename is safe
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file

        status = "Register"
        user_type = "farmer"
        
        date = datetime.now()

        mySql_insert_query = """INSERT INTO farmer(area_id, farmer_name, address,adhaarno, mobile, email, reg_date, upload, account_holder_name, account_no, IFSC_code, branch_name, status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = connection.cursor()
        result = cursor.execute(mySql_insert_query, (area, fname, address,adhaar, mobile, email, date, filename, account_holder_name, account_no, ifsc_code, branch_name, status))
        connection.commit()
       
        row_id = cursor.lastrowid

        my_log_qry = "INSERT INTO login(username, password, reg_id, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(my_log_qry, (email, password, row_id, user_type))
        connection.commit()

        flash("Record inserted successfully")
        cursor.close()
        return redirect(url_for('login'))
    
    else:
        mycursor = connection.cursor()
        query = "SELECT * from area"
        mycursor.execute(query)
        area_obj = mycursor.fetchall()
        return render_template("farmer_registration.html", area_obj=area_obj)


@app.route('/Area', methods=['GET', 'POST'])
def area():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == "POST":
        area_name = request.form.get('area_name')
        insert_query = "INSERT INTO area (area_name) VALUES (%s)"
        cursor.execute(insert_query, (area_name,))
        connection.commit()
        flash("Record inserted successfully")

        return redirect(url_for("area"))
    
    # Fetch all area records when the method is GET
    query = "SELECT * FROM area"
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('area.html', ar_obj=ar_obj)

@app.route('/admin_edit_area/<int:area_id>', methods=['POST'])
def admin_edit_area(area_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get form data
    area_name = request.form.get('area_name')

    # Update the database
    update_query = "UPDATE area SET area_name=%s WHERE area_id=%s"
    cursor.execute(update_query, (area_name,area_id))
    connection.commit()

    flash("Area updated successfully")
    cursor.close()
    connection.close()

    return redirect(url_for("area"))

@app.route('/admin_delete_area/<int:area_id>', methods=['POST'])
def admin_delete_area(area_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = " DELETE FROM area WHERE area_id = %s "
    cursor.execute(query,(area_id,))
    connection.commit()

    flash('Area deleted successfully')
    cursor.close()
    connection.close()

    return redirect(url_for("area"))

@app.route('/Product_Category', methods=['GET', 'POST'])
def pdtcategory():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == "POST":
        category_name = request.form.get('category_name')
        insert_query = "INSERT INTO product_category (category_name) VALUES (%s)"
        cursor.execute(insert_query, (category_name,))
        connection.commit()
        flash("Record inserted successfully")

        return redirect(url_for("pdtcategory"))
    
    # Fetch all area records when the method is GET
    query = "SELECT * FROM product_category"
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('pdtcategory.html', ar_obj=ar_obj)

@app.route('/farmer_complaint')
def farmer_complaint():

    return render_template('complaint_farmer.html')

@app.route('/get_against_options')
def get_against_options():
    """Fetch data for the Against select dropdown based on 'To' selection."""
    to = request.args.get('to')  # Get the 'to' parameter from the request
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        if to == "Customer":
            query = "SELECT customer_id AS id, customer_name AS name FROM customers"
        elif to == "Landowner":
            query = "SELECT landowner_id AS id, landowner_name AS name FROM land_owners"
        else:
            return jsonify([])  # Return empty list for invalid input

        cursor.execute(query)
        rows = cursor.fetchall()

        # Debug: Print rows to console
        print("Query Result:", rows)

        if not rows:
            return jsonify({"error": "No data found"}), 404  # No matching records

        # Format data for JSON response
        options = [{"id": row["id"], "name": row["name"]} for row in rows]
        return jsonify(options)

    except Error as e:
        print(f"Error ++during query execution: {e}")
        return jsonify({"error": "Failed to execute query"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
@app.route('/submit_complaint',methods=['POST'])
def submit_complaint():
    toSelect = request.form.get('toSelect')
    againstSelect = request.form.get('againstSelect')
    matter = request.form.get('matter')

    if not toSelect or not againstSelect or not matter:
        flash("All fields are required","error")
        return redirect('/farmer_complaint')
    
    sender_id = session.get('userid')
    sender_type = "Farmer"
    date = datetime.now()
    status = 'Register'
    
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """INSERT INTO complaints (sender_id, sender_type, to_person_id, to_person_type, complaint, date, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (sender_id, sender_type,againstSelect, toSelect, matter, date,status))
        connection.commit()

        flash("Complaint registered successfully","success")
        return redirect('/farmer_complaint')

    except mysql.connector.Error as err:
        print(f"Error inserting complaint: {err}")
        flash("An error occured while submitting your complaint.","error")
        return redirect('/farmer_complaint')

    finally:
         if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/landowner_complaint')
def landowner_complaint():
    return render_template('landowner_complaint.html')

@app.route('/get_against_options_alternative')
def get_against_options_alternative():
    """Fetch data for the Against select dropdown based on 'To' selection."""
    to = request.args.get('to')  # Get the 'to' parameter from the request
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

       
        if to == "Farmer":
            query = "SELECT farmer_id AS id, farmer_name AS name FROM farmer"
        else:
            return jsonify([])  # Return empty list for invalid input

        cursor.execute(query)
        rows = cursor.fetchall()

        # Debug: Print rows to console
        print("Query Result:", rows)

        if not rows:
            return jsonify({"error": "No data found"}), 404  # No matching records

        # Format data for JSON response
        options = [{"id": row["id"], "name": row["name"]} for row in rows]
        return jsonify(options)

    except Error as e:
        print(f"Error during query execution: {e}")
        return jsonify({"error": "Failed to execute query"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/submit_complaint_alternative',methods=['POST'])
def submit_complaint_alternative():
    toSelect = request.form.get('toSelect')
    againstSelect = request.form.get('againstSelect')
    matter = request.form.get('matter')

    if not toSelect or not againstSelect or not matter:
        flash("All fields are required","error")
        return redirect('/landowner_complaint')

    sender_id = session.get('userid')
    sender_type = "landowner"
    date = datetime.now()
    status = 'Register'

    connection = get_db_connection()
    if not connection:
        return jsonify({"error","Database connection failed."}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """INSERT INTO complaints (sender_id, sender_type, to_person_id, to_person_type, complaint, date, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (sender_id, sender_type,againstSelect, toSelect, matter, date,status))
        connection.commit()
        
        flash("Complaint submitted successfully","success")
        return redirect('/landowner_complaint')

    except mysql.connector.Error as err:
        print(f"Error inserting complaint: {err}")
        flash("An error occured while submitting your complaint","error")
        return redirect('/landowner_complaint')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/customer_complaint')
def customer_complaint():
    return render_template('customer_complaint.html')

@app.route('/get_against_options_other')
def get_against_options_other():
    """Fetch data for the 'Against' select dropdown based on 'To' selection."""
    to = request.args.get('to')  # Get the 'to' parameter from the request
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        # Validate the 'to' parameter and prepare the query
    
        if to == "Farmer":
            query = "SELECT farmer_id AS id, farmer_name AS name FROM farmer"
        else:
            return jsonify({"error": "Invalid 'to' parameter"}), 400  # Invalid input

        # Execute the query and fetch results
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            return jsonify([])  # Return an empty list if no records found

        # Format data for JSON response
        options = [{"id": row["id"], "name": row["name"]} for row in rows]
        return jsonify(options)

    except Exception as e:
        # Log the error and return a generic message to the client
        print(f"Error during query execution: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

    finally:
        # Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/submit_complaint_other', methods=['POST'])
def submit_complaint_other():
    toSelect = request.form.get('toSelect')
    againstSelect = request.form.get('againstSelect')
    matter = request.form.get('matter')

    if not toSelect or not againstSelect or not matter:
        flash("All fields are required", "error")
        return redirect('/customer_complaint')

    sender_id = session.get('userid')
    sender_type = "customer"
    date = datetime.now()
    status = 'Register'

    connection = get_db_connection()
    if not connection:
        flash("Database connection failed.", "error")
        return redirect('/customer_complaint')

    try:
        cursor = connection.cursor(dictionary=True)
        query = """INSERT INTO complaints (sender_id, sender_type, to_person_id, to_person_type, complaint, date, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (sender_id, sender_type,againstSelect, toSelect, matter, date,status))
        connection.commit()

        flash("Complaint submitted successfully", "success")
        return redirect('/customer_complaint')

    except mysql.connector.Error as err:
        print(f"Error inserting complaint: {err}")
        flash("An error occurred while submitting your complaint", "error")
        return redirect('/customer_complaint')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/complaint_management' ,methods=['GET', 'POST'])
def complaint_management():
    connection = get_db_connection()
    cursor = connection.cursor()


    query = """
    SELECT 
    c.complaint_id,
    -- Determine the sender name based on sender_type
    CASE 
        WHEN c.sender_type = 'customer' THEN cu.customer_name
        WHEN c.sender_type = 'landowner' THEN lo.landowner_name
        WHEN c.sender_type = 'farmer' THEN f1.farmer_name
        ELSE 'Unknown Sender'
    END AS sender_name,
    c.sender_type,
    -- Determine the to_person_name based on to_person_type
    CASE 
        WHEN c.to_person_type = 'farmer' THEN f2.farmer_name
        WHEN c.to_person_type = 'landowner' THEN lo2.landowner_name
        WHEN c.to_person_type = 'customer' THEN cu2.customer_name
        ELSE 'Unknown Recipient'
    END AS to_person_name,
    c.to_person_type,
    c.complaint,
    c.date,
    COALESCE(c.admin_reply, 'No reply yet') AS admin_reply,
    c.status
FROM complaints c
-- Join the customers table for sender
LEFT JOIN customers cu ON c.sender_id = cu.customer_id AND c.sender_type = 'customer'
-- Join the farmers table for sender
LEFT JOIN farmer f1 ON c.sender_id = f1.farmer_id AND c.sender_type = 'farmer'
-- Join the land_owners table for sender
LEFT JOIN land_owners lo ON c.sender_id = lo.landowner_id AND c.sender_type = 'landowner'
-- Join the farmers table for recipient
LEFT JOIN farmer f2 ON c.to_person_id = f2.farmer_id AND c.to_person_type = 'farmer'
-- Join the customers table for recipient
LEFT JOIN customers cu2 ON c.to_person_id = cu2.customer_id AND c.to_person_type = 'customer'
-- Join the land_owners table for recipient
LEFT JOIN land_owners lo2 ON c.to_person_id = lo2.landowner_id AND c.to_person_type = 'landowner';
"""
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('complaint_mngmnt.html', ar_obj=ar_obj)



@app.route('/send_enquiry/<int:complaint_id>', methods=['POST'])
def send_enquiry(complaint_id):
    enquiry_message = request.form.get('enquiry_message')  # Enquiry message from form field

    # Validate form data
    if not (complaint_id and enquiry_message):
        flash("Both item ID and enquiry message are required.", "error")
        return redirect(url_for('complaint_management'))

    # Database connection
    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "error")
        return redirect(url_for('complaint_management'))

    try:
        cursor = connection.cursor()

        # Insert the enquiry into complaint_enquiries table
        query = """
            INSERT INTO complaint_enquiry (complaint_id, enquiry, date, status)
            VALUES (%s, %s, NOW(), 'Sent')
        """
        cursor.execute(query, (complaint_id, enquiry_message))
        connection.commit()

        update_query = " UPDATE complaints SET status = 'enquiry sent' where complaint_id=%s"
        cursor.execute(update_query, (complaint_id,))

        connection.commit()

        flash("Enquiry sent successfully.", "success")
    except Exception as e:
        print(f"Error sending enquiry: {e}")  # Replace with logging in production
        flash("Failed to send enquiry. Please try again.", "error")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('complaint_management'))




@app.route('/delete_complaint/<int:complaint_id>', methods=['GET', 'POST'])
def delete_complaint(complaint_id):

    connection = get_db_connection()
    mycursor = connection.cursor()
    try:
        query = "DELETE FROM complaints WHERE complaint_id = %s"
        mycursor.execute(query, (complaint_id,))
        connection.commit()
        flash('Complaint deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()  
        flash('An error occurred while deleting complaint.', 'error')
        print(e)
    finally:
        mycursor.close()
        connection.close()
    return redirect(url_for('complaint_management'))

# @app.route('/customer_view_products')
# def customer_view_products():
#     return render_template('customer_view_pdt.html')


@app.route('/farmer_view_enquiries')
def farmer_view_enquiries():
    user_id = session.get('userid')  # Safe way to fetch session variable

    user_type ="Farmer"

    login_type = "farmer"


    connection = get_db_connection()
    mycursor = connection.cursor()

    # Check if user exists and is a farmer
    check_query = "SELECT reg_id FROM login WHERE reg_id = %s AND type = %s"
    mycursor.execute(check_query, (user_id,login_type))
    result = mycursor.fetchone()

    if not result:
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    # Fetching farmer's enquiries
    query = """ 
        SELECT e.enquiry_id,e.enquiry, e.date, e.status 
        FROM complaint_enquiry e
        INNER JOIN complaints c ON e.complaint_id = c.complaint_id
        WHERE c.to_person_id = %s AND c.to_person_type = %s
        ORDER BY e.date DESC 
    """
    
    mycursor.execute(query, (user_id,user_type))
    ar_obj = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template('farmer_enquiry.html', ar_obj=ar_obj)  



@app.route('/landowner_view_enquiries')
def landowner_view_enquiries():
    user_id = session.get('userid')  # Safe way to fetch session variable

    user_type ="Landowner"

    login_type = "landowner"

    connection = get_db_connection()
    mycursor = connection.cursor()

    # # Check if user exists and is a farmer
    # check_query = "SELECT reg_id FROM login WHERE reg_id = %s AND type = %s"
    # mycursor.execute(check_query, (user_id,login_type))
    # result = mycursor.fetchone()

    # if not result:
    #     flash("Unauthorized access.", "error")
    #     return redirect(url_for('login'))

    # Fetching farmer's enquiries
    query = """ 
        SELECT e.enquiry_id,e.enquiry, e.date, e.status 
        FROM complaint_enquiry e
        INNER JOIN complaints c ON e.complaint_id = c.complaint_id
        WHERE c.to_person_id = %s AND c.to_person_type = %s
        ORDER BY e.date DESC 
    """
    
    mycursor.execute(query, (user_id,user_type))
    ar_obj = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template('landowner_enquiry.html', ar_obj=ar_obj) 


@app.route('/landowner_view_land_details')
def landowner_view_land_details():
    
    land_owner_id = session.get('userid')  # Safe way to fetch session variable

    connection = get_db_connection()
    mycursor = connection.cursor()

   
    # Fetching landowner's land details view
    query = """ 
        SELECT ld.*,a.area_id,a.area_name FROM land_details ld
        INNER JOIN area a ON ld.area_id = a.area_id
        WHERE ld.land_owner_id = %s """
    
    mycursor.execute(query, (land_owner_id,))
    ar_obj = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template('landowner_view_landdetails.html', ar_obj=ar_obj)


@app.route('/customer_view_enquiries')
def customer_view_enquiries():
    user_id = session.get('userid')  # Safe way to fetch session variable

    user_type ="Customer"

    login_type = "customer"

    connection = get_db_connection()
    mycursor = connection.cursor()

    # Check if user exists and is a farmer
    check_query = "SELECT reg_id FROM login WHERE reg_id = %s AND type = %s"
    mycursor.execute(check_query, (user_id,login_type))
    result = mycursor.fetchone()

    if not result:
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    # Fetching farmer's enquiries
    query = """ 
        SELECT e.enquiry_id,e.enquiry, e.date, e.status 
        FROM complaint_enquiry e
        INNER JOIN complaints c ON e.complaint_id = c.complaint_id
        WHERE c.to_person_id = %s AND c.to_person_type = %s
        ORDER BY e.date DESC 
    """
    
    mycursor.execute(query, (user_id,user_type))
    ar_obj = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template('customer_enquiry.html', ar_obj=ar_obj) 




@app.route('/farmer_send_reply/<int:enquiry_id>', methods=['POST'])
def farmer_send_reply(enquiry_id):
  
    reply_message = request.form.get('reply_message')  # Enquiry message from form field

    # Validate form data
    if not (enquiry_id and reply_message):
        flash("Both item ID and reply message are required.", "error")
        return redirect(url_for('farmer_view_enquiries'))

    # Database connection
    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "error")
        return redirect(url_for('farmer_view_enquiries'))

    try:
        cursor = connection.cursor()

        # Insert the enquiry into complaint_enquiries table
        query = """
            INSERT INTO enquiry_reply (enquiry_id,reply,date,status)
            VALUES (%s, %s, NOW(), 'Sent')
        """
        cursor.execute(query, (enquiry_id, reply_message))
        connection.commit()

        update_query = " UPDATE complaint_enquiry SET status = 'reply sent' where enquiry_id=%s"
        cursor.execute(update_query, (enquiry_id,))

        connection.commit()

        flash("Reply sent successfully.", "success")
    except Exception as e:
        print(f"Error sending reply: {e}")  # Replace with logging in production
        flash("Failed to send reply. Please try again.", "error")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('farmer_view_enquiries'))
@app.route('/landowner_send_reply/<int:enquiry_id>', methods=['POST'])
def landowner_send_reply(enquiry_id):
  
    reply_message = request.form.get('reply_message')  # Enquiry message from form field

    # Validate form data
    if not (enquiry_id and reply_message):
        flash("Both item ID and reply message are required.", "error")
        return redirect(url_for('landowner_view_enquiries'))

    # Database connection
    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "error")
        return redirect(url_for('landowner_view_enquiries'))

    try:
        cursor = connection.cursor()

        # Insert the enquiry into complaint_enquiries table
        query = """
            INSERT INTO enquiry_reply (enquiry_id,reply,date,status)
            VALUES (%s, %s, NOW(), 'Sent')
        """
        cursor.execute(query, (enquiry_id, reply_message))
        connection.commit()

        update_query = " UPDATE complaint_enquiry SET status = 'reply sent' where enquiry_id=%s"
        cursor.execute(update_query, (enquiry_id,))

        connection.commit()

        flash("Reply sent successfully.", "success")
    except Exception as e:
        print(f"Error sending reply: {e}")  # Replace with logging in production
        flash("Failed to send reply. Please try again.", "error")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('landowner_view_enquiries'))




@app.route('/customer_send_reply/<int:enquiry_id>', methods=['POST'])
def customer_send_reply(enquiry_id):
  
    reply_message = request.form.get('reply_message')  # Enquiry message from form field

    # Validate form data
    if not (enquiry_id and reply_message):
        flash("Both item ID and reply message are required.", "error")
        return redirect(url_for('customer_view_enquiries'))

    # Database connection
    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "error")
        return redirect(url_for('customer_view_enquiries'))

    try:
        cursor = connection.cursor()

        # Insert the enquiry into complaint_enquiries table
        query = """
            INSERT INTO enquiry_reply (enquiry_id,reply,date,status)
            VALUES (%s, %s, NOW(), 'Sent')
        """
        cursor.execute(query, (enquiry_id, reply_message))
        connection.commit()

        update_query = " UPDATE complaint_enquiry SET status = 'reply sent' where enquiry_id=%s"
        cursor.execute(update_query, (enquiry_id,))

        connection.commit()

        flash("Reply sent successfully.", "success")
    except Exception as e:
        print(f"Error sending reply: {e}")  # Replace with logging in production
        flash("Failed to send reply. Please try again.", "error")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('customer_view_enquiries'))

@app.route('/admin_view_reply', methods=['GET'])
def admin_view_reply():
    connection = get_db_connection()
    cursor = connection.cursor()

    if not connection:
        flash("Database connection failed.", "error")
        return redirect('/admin_view_reply')
    
    query = """ SELECT
    c.complaint_id,
    CASE
        WHEN c.sender_type = 'farmer' THEN f.farmer_name
        WHEN c.sender_type = 'landowner' THEN lo.landowner_name
        WHEN c.sender_type = 'customer' THEN cust.customer_name
        ELSE 'Unknown Sender'
    END AS sender_name,
    c.sender_type,
    CASE
        WHEN c.to_person_type = 'farmer' THEN f2.farmer_name
        WHEN c.to_person_type = 'landowner' THEN lo2.landowner_name
        WHEN c.to_person_type = 'customer' THEN cust2.customer_name
        ELSE 'Unknown Recipient'
    END AS recipient_name,
    c.to_person_type,
    c.complaint,
    e.enquiry,
    er.reply,
    er.status AS reply_status
FROM
    complaints c
JOIN complaint_enquiry e ON c.complaint_id = e.complaint_id
JOIN enquiry_reply er ON e.enquiry_id = er.enquiry_id
LEFT JOIN farmer f ON c.sender_id = f.farmer_id
LEFT JOIN land_owners lo ON c.sender_id = lo.landowner_id
LEFT JOIN customers cust ON c.sender_id = cust.customer_id
LEFT JOIN farmer f2 ON c.to_person_id = f2.farmer_id
LEFT JOIN land_owners lo2 ON c.to_person_id = lo2.landowner_id
LEFT JOIN customers cust2 ON c.to_person_id = cust2.customer_id;
"""
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('admin_view_reply.html', ar_obj=ar_obj)




@app.route('/admin_send_reply/<int:complaint_id>',methods = ['POST'])
def admin_send_reply(complaint_id):
    admin_reply = request.form.get('admin_reply')

    connection = get_db_connection()
    cursor = connection.cursor()

    if not connection:
        flash("Database connection failed.", "error")
        return redirect('/admin_view_reply')

    get_enquiry_query = """
            SELECT enquiry_id
            FROM complaint_enquiry
            WHERE complaint_id = %s
        """
    cursor.execute(get_enquiry_query, (complaint_id,))
    enquiry_id = cursor.fetchone()

    if not enquiry_id:
        flash("No enquiry found for the given complaint ID.", "error")
        return redirect('/admin_view_reply')

        # Fetch the enq_reply_id associated with the enquiry_id
    get_enquiry_reply_query = """
            SELECT enq_reply_id
            FROM enquiry_reply
            WHERE enquiry_id = %s
        """
    cursor.execute(get_enquiry_reply_query, (enquiry_id[0],))
    enq_reply_id = cursor.fetchone()

    if not enq_reply_id:
        flash("No reply found for the given enquiry ID.", "error")
        return redirect('/admin_view_reply')

        # Update the complaints table
    update_complaint_query = """
            UPDATE complaints
            SET admin_reply = %s, status = 'Completed'
            WHERE complaint_id = %s
        """
    cursor.execute(update_complaint_query, (admin_reply, complaint_id))

        # Update the enquiry_reply table
    update_enquiry_reply_query = """
            UPDATE enquiry_reply
            SET status = 'Replied'
            WHERE enq_reply_id = %s
        """
    cursor.execute(update_enquiry_reply_query, (enq_reply_id[0],))
  
    connection.commit()

    flash("Reply sent successfully.", "success")
    
    cursor.close()
    connection.close()

    return redirect('/admin_view_reply')



@app.route('/farmer_complaint_status',methods = ['GET'])
def farmer_complaint_status():
    sender_id = session.get('userid')  # Safe way to fetch session variable

    sender_type ="farmer"

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ 
        SELECT c.complaint,c.admin_reply,c.status
        FROM complaints c
        WHERE c.sender_id = %s AND c.sender_type = %s
    """
    cursor.execute(query, (sender_id,sender_type))
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('farmer_complaint_status.html',ar_obj = ar_obj)



@app.route('/landowner_complaint_status',methods = ['GET'])
def landowner_complaint_status():
    sender_id = session.get('userid')  # Safe way to fetch session variable

    sender_type ="landowner"

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ 
        SELECT c.complaint,c.admin_reply,c.status
        FROM complaints c
        WHERE c.sender_id = %s AND c.sender_type = %s
    """
    cursor.execute(query, (sender_id,sender_type))
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('land_complaint_status.html',ar_obj = ar_obj)
 



@app.route('/customer_complaint_status',methods = ['GET'])
def customer_complaint_status():
    sender_id = session.get('userid')  # Safe way to fetch session variable

    sender_type ="customer"

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ 
        SELECT c.complaint,c.admin_reply,c.status
        FROM complaints c
        WHERE c.sender_id = %s AND c.sender_type = %s
    """
    cursor.execute(query, (sender_id,sender_type))
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('cust_complaint_status.html',ar_obj = ar_obj)




@app.route('/admin_view_approval',methods = ['GET'])
def admin_view_approval():
    
    connection = get_db_connection()
    cursor = connection.cursor()

    query= """
        SELECT farmer_id, farmer_name, 'farmer', status, 
               address, adhaarno, mobile, email, reg_date 
        FROM farmer
    """
    cursor.execute(query)
    farmers = cursor.fetchall()

    # Fetch Landowners with all details
    query = """
        SELECT landowner_id, landowner_name, 'landowner', status, 
               address, adhaar, mobile, email, reg_date 
        FROM land_owners
    """
    cursor.execute(query)
    landowners = cursor.fetchall()

    # Combine both lists
    ar_obj = farmers + landowners
    cursor.close()
    connection.close()
   
    return render_template('admin_register_approval.html',ar_obj = ar_obj)




@app.route('/approve_user/<int:user_id>/<string:user_type>',methods =['POST'])
def approve_user(user_id,user_type):

    connection = get_db_connection()
    cursor = connection.cursor()

    if user_type == "farmer":
        query = "UPDATE farmer SET status = 'approved' WHERE farmer_id = %s"
        cursor.execute(query,(user_id,))
        connection.commit()
        query = "SELECT farmer_id, email, farmer_name FROM farmer WHERE farmer_id = %s"
        cursor.execute(query,(user_id,))

    elif user_type == "landowner":
        query = "UPDATE land_owners SET status = 'approved' WHERE landowner_id = %s"
        cursor.execute(query,(user_id,))
        connection.commit()
        query = "SELECT landowner_id, email, landowner_name FROM land_owners WHERE landowner_id = %s"
        cursor.execute(query,(user_id,))

    else:
        cursor.close()
        connection.close()
        flash("Invalid user type!", "danger")
        return redirect(url_for('admin_view_approval'))

    user = cursor.fetchone()

    if user:
        reg_id, email, username = user
        password = f"{username}@123"

        # Insert login details
        query = "INSERT INTO login (reg_id, username, password, type) VALUES (%s, %s, %s, %s)"
        cursor.execute(query,(reg_id, email, password, user_type))

        connection.commit()
        flash(f"{username} has been approved!", "success")
    else:
        flash("User not found!", "danger")

    cursor.close()
    connection.close()

    return redirect(url_for('admin_view_approval'))



@app.route('/land_registration', methods=['GET', 'POST'])
def land_registration():
    connection = get_db_connection()
    cursor = connection.cursor()

    landowner_id = session.get('userid')

    # Fetch area list for dropdown
    cursor.execute("SELECT area_id, area_name FROM area")
    area_obj = cursor.fetchall()

    if request.method == 'POST':
        # Fetch form data
        area = request.form.get('area')
        village = request.form.get('village')
        total_area = request.form.get('total_area')
        survey_no = request.form.get('survey_no')
        land_type = request.form.get('land_type')
        remark = request.form.get('remark')
        date = datetime.now()

        # ✅ Initialize filename to avoid UnboundLocalError
        filename = None

        # Handle file upload
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = "no_file_uploaded"  # Default value if no file is uploaded

        # ✅ Insert into MySQL
        insert_query = """INSERT INTO land_details(land_owner_id, area_id, village_name, total_area, survey_no, land_type, upload, remark, status, date)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Added', %s)"""
        values = (landowner_id, area, village, total_area, survey_no, land_type, filename, remark, date)

        try:
            cursor.execute(insert_query, values)
            connection.commit()
            flash("Land details inserted successfully", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    cursor.close()
    connection.close()

    return render_template('land_registration.html', area_obj=area_obj)



@app.route('/admin_land_details',methods = ['GET'])
def admin_land_details():
    connection = get_db_connection()
    cursor = connection.cursor()

    query= """
      SELECT 
        ld.land_details_id,
        lo.landowner_name,  -- Fetching landowner name from Land_Owners table
        a.area_name,        -- Fetching area name from Area table
        ld.total_area,
        ld.status,
        ld.village_name,
        ld.survey_no,
        ld.land_type,
        ld.upload,
        ld.remark,
        ld.date
      FROM land_details ld
      JOIN land_owners lo ON ld.land_owner_id = lo.landowner_id
      JOIN area a ON ld.area_id = a.area_id;

    """

    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_land_approval.html',ar_obj=ar_obj)

@app.route('/land_approval/<int:land_details_id>',methods = ['POST'])
def land_approval(land_details_id):
    matter = request.form.get('remark') 

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "UPDATE land_details SET status='approved' where land_details_id=%s"
    cursor.execute(query,(land_details_id,))
    connection.commit()

    flash("Land has been approved", "success")

    cursor.close()
    connection.close()

    return redirect(url_for('admin_land_details'))


@app.route('/customer_view_products', methods=['GET', 'POST']) 
def customer_view_products():

    connection = get_db_connection()

    mycursor = connection.cursor()
    query = """SELECT p.*,pc.pcategory_id,pc.category_name FROM products p 
                inner join product_category pc on p.pcategory_id = pc.pcategory_id """
    mycursor.execute(query)
    pdts=mycursor.fetchall()

    mycursor.close()
    connection.close()
 
    return render_template("customer_products.html",pdts=pdts); 


# Function to check if cart id exists for customer_id in cart table.
def is_cart(customer_id):

    connection = get_db_connection()

    cursor = connection.cursor()
    query = "SELECT cart_id FROM cart WHERE customer_id = %s"
    cursor.execute(query, (customer_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    if result:
        return result[0]
    else:
        None

def update_product_quantity(product_id, purchased_quantity):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Deduct purchased quantity from the available quantity
    cursor.execute(
        "UPDATE products SET quantity = quantity - %s WHERE product_id = %s AND quantity >= %s",
        (purchased_quantity, product_id, purchased_quantity)
    )
    connection.commit()
    
    cursor.close()
    connection.close()

# Function For Adding items into cart log
def add_cart_log(cart_id, product_id, quantity, rate):
    if cart_id is not None:

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO cart_log(cart_id, product_id, quantity, rate) VALUES(%s, %s, %s, %s)",
            (cart_id, product_id, quantity, rate)
        )
        connection.commit()

        cursor.close()
        connection.close()

        flash("Product successfully added to the cart")
        print("Record inserted successfully into cart_log")
    else:
        flash("Failed to add to cart. Please try again.")
        print("Failed to insert into cart. Please try again.")



@app.route("/customer_add_cart", methods=['GET', 'POST'])
def customer_add_cart():

    customer_id = session.get("userid")  # Retrieve 'Customer Id' from the session
    print("Customer Id:", customer_id)
    date = datetime.now()
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        rate = float(request.form.get('rate'))
        quantity = int(request.form.get('quantity'))
        total_amount = rate*quantity

        status = "send"

        # Check if a cart exists for the user in the current session
        cart_id = is_cart(customer_id)
        
        # If a cart already exists, use the existing cart_id
        if  cart_id is not None:
            # Function For Adding items into cart log
            add_cart_log(cart_id, product_id, quantity, rate)

            #Calling function for updating the total amount in cart
            update_total_amount(cart_id)

        else:
            # If not, create a new cart entry

            connection = get_db_connection()

            cursor = connection.cursor()
            query = "INSERT INTO cart(customer_id,total_amount,date,status) values(%s,%s,%s,%s)"
            cursor.execute(query, (customer_id, total_amount, date, status))
            connection.commit()

            # Get the last inserted cart_id
            last_cart_id = cursor.lastrowid

            cursor.close()
            connection.close()
             
            # Function For Adding items into cart log
            add_cart_log(last_cart_id, product_id, quantity, rate)

        return redirect(url_for('customer_view_products'))



# Function to update total amount in cart according to the cart log
def update_total_amount(cart_id):
    
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT SUM(quantity * rate) FROM cart_log WHERE cart_id = %s"
    cursor.execute(query, (cart_id,))
    total_amount = cursor.fetchone()[0]
    query = "UPDATE cart SET total_amount = %s WHERE cart_id = %s"
    cursor.execute(query, (total_amount, cart_id))
    connection.commit()
    cursor.close()
    connection.close()




@app.route("/customer_cart")
def customer_cart():

      connection = get_db_connection()       
      customer_id = session.get("userid")
      print("Customer Id:", customer_id)
      query = """SELECT c.*, cl.*, p.product_id, p.product_name, p.image, p.quantity as stock_quantity
           FROM cart_log cl 
           LEFT JOIN cart c ON cl.cart_id = c.cart_id
           LEFT JOIN products p ON cl.product_id = p.product_id
           WHERE c.customer_id = %s and c.status = 'send'
        """
   
      mycursor = connection.cursor(dictionary=True)
      mycursor.execute(query, (customer_id,))
      result = mycursor.fetchall()

      mycursor.close()
      connection.close()            

      return render_template("cart.html", cart_items = result)  


# Context processor to make cart_count available globally
@app.context_processor
def view_cart_count():
    customer_id = session.get("userid")
    connection = get_db_connection()   
    mycursor = connection.cursor()

    # Fetch the count of items in the cart for the customer
    count_query = """
                SELECT COUNT(cl.product_id) 
                FROM cart_log cl
                LEFT JOIN cart c ON cl.cart_id = c.cart_id
                WHERE c.customer_id = %s
    """
    mycursor.execute(count_query, (customer_id,))
    count_result = mycursor.fetchone()
    cart_count = count_result[0] if count_result else 0

    mycursor.close()
    connection.close()

    return dict(cart_count=cart_count)



@app.route('/customer_delete_cart_item/<int:cart_log_id>', methods=['GET','POST'])
def customer_delete_cart_item(cart_log_id):
    
    # Create cursor
    connection = get_db_connection() 
    mycursor = connection.cursor()

    # Fetch the cart_id and product_id associated with the cart_log_id
    fetch_query = "SELECT cart_id, product_id FROM cart_log WHERE cart_log_id = %s"
    mycursor.execute(fetch_query, (cart_log_id,))
    result = mycursor.fetchone()

    if result:
        cart_id = result[0]

        # Delete from cart_log table
        delete_query =  "DELETE FROM cart_log WHERE cart_log_id = %s"
        mycursor.execute(delete_query, (cart_log_id,))
        connection.commit()

        # Check if the deletion from cart_log table was successful
        if mycursor.rowcount > 0:
            flash("Item successfully removed from the cart.")

            # Check if there are no more items with the same cart_id in cart_log
            check_query = "SELECT COUNT(*) AS count FROM cart_log WHERE cart_id = %s"
            mycursor.execute(check_query, (cart_id,))
            count_result = mycursor.fetchone()

            if count_result[0] == 0:
                # If there are no more items with the same cart_id, delete from cart table
                delete_cart_query = "DELETE FROM cart WHERE cart_id = %s"
                mycursor.execute(delete_cart_query, (cart_id,))
                connection.commit()

                # Check if the deletion from cart table was successful                
                if mycursor.rowcount > 0:
                    flash("Item successfully removed from the cart.")
                else:
                    flash("Failed to remove item from the cart.")
        

        else:       
            flash("Item not found in the cart.")
                
        return redirect(url_for('customer_cart'))




@app.route("/customer_update_cart", methods=["GET", "POST"])
def customer_update_cart():

      customer_id = session.get("userid")
      cart_items = []  # Define cart_items outside the route function to maintain its state

      connection = get_db_connection() 

    # Print entire form data for debugging
      print("Form Data:", request.form)
      cart_total = request.form.get('cart_total')
      cart_id = request.form.get('cart_id')
      date = datetime.now()

      if request.method == "POST":
            # Iterate over the form data to update the quantities of cart items
            for key, value in request.form.items():
                  if key.startswith('quantity_'):
                        cart_log_id = key.split('_')[-1]  # Extract the cart_log_id from the key
                        quantity = int(value)
                        # Update the quantity of the corresponding cart item
                        cart_item = {
                              'cart_log_id': cart_log_id,
                              'quantity': quantity
                        }
                        cart_items.append(cart_item)
                        cart_update_query = "UPDATE cart SET total_amount = %s, date = %s WHERE cart_id = %s AND customer_id = %s"
                        query_values = (cart_total, date, cart_id, customer_id)
                        with connection.cursor() as mycursor:
                              mycursor.execute(cart_update_query, query_values)
                              connection.commit()
                              print("Rcord updated successfully in cart table")

                        with connection.cursor() as logcursor:
                              cart_log_update_query = "UPDATE cart_log SET quantity = %s WHERE cart_log_id = %s AND cart_id = %s"
                              # log_query_values = (quantity, cart_log_id, cart_id)
                              logcursor.execute(cart_log_update_query, (quantity, cart_log_id, cart_id))
                              connection.commit()
                              print("Rcord updated successfully in cart log table")


                  
      print("cart_items", cart_items)
      print("cart_total", cart_total)
      print("cart_id", cart_id)

      return "Cart updated successfully"



@app.route("/customer_order", methods=["GET", "POST"])
def customer_order():

    connection = get_db_connection()
    cursor = connection.cursor()
    
    customer_id = session.get("userid")


    # Retrieve the last order number from the database
    cursor.execute("SELECT order_no FROM orders ORDER BY order_no DESC LIMIT 1")
    last_order = cursor.fetchone()

    if last_order:
        # Extract the numeric part of the order number (remove the "ORD00" prefix)
        last_order_number = last_order[0]
        # Assuming the order_no follows the pattern 'ODR-001', 'ODR-002', etc.
        order_prefix = 'ODR-'
        current_number = int(last_order_number.split('-')[1])  # Get the number part
        # Increment the order number by 1
        next_number = current_number + 1
        
        new_order_no = f"{order_prefix}{next_number:03d}"  # Format it with leading zeros
        
    else:
        # If no previous orders exist, start with order number "ORD0001"
        
        new_order_no = "ODR-001"
        cursor.close()

        cursor = connection.cursor()

    if request.method == "POST":
        cart_total = request.form.get('cart_total')
        cart_id = request.form.get('cart_id')
        date = datetime.now()

        status = "order placed"
     
        cursor.execute(
            "INSERT INTO orders(cart_id,customer_id,order_no,total_amount, date,status) VALUES(%s, %s, %s, %s,%s,%s)",
            (cart_id,customer_id, new_order_no, cart_total, date, status)
        )

        last_orderid = cursor.lastrowid
        
        connection.commit()
        cursor.close()
        mycursor = connection.cursor()
        query =  "DELETE FROM cart WHERE cart_id = %s"
        mycursor.execute(query, (cart_id,))
        connection.commit()
       
        connection.close()

        flash("Order placed successfully")
        print("Record inserted successfully into orders")
    else:
        flash("Failed to place order. Please try again.")
        print("Failed to insert into orders. Please try again.") 

    return redirect(url_for('customer_bill',order_id=last_orderid, total=cart_total))  




from decimal import Decimal
from flask import flash, redirect, url_for

@app.route("/customer_bill/<int:order_id>/<float:total>", methods=["GET", "POST"])
def customer_bill(order_id, total):
    connection = get_db_connection()
    cursor = connection.cursor()

    status = "Generated"
    order_status = "Bill Generated"

    # Fetch the current highest bill number from the customer_bill table
    cursor.execute("SELECT bill_no FROM customer_bill ORDER BY bill_no DESC LIMIT 1")
    last_bill = cursor.fetchone()

    if last_bill:
        last_bill_no = last_bill[0]
        bill_prefix = 'INV-'
        current_number = int(last_bill_no.split('-')[1])
        next_number = current_number + 1
        new_bill_no = f"{bill_prefix}{next_number:03d}"
    else:
        new_bill_no = "INV-001"
    
    cursor.close()
    mycursor = connection.cursor()
    mycursor.execute(
        "INSERT INTO customer_bill(order_id, bill_no, bill_amount, payment_status) VALUES(%s, %s, %s, %s)",
        (order_id, new_bill_no, total, status)
    )

    last_billid = mycursor.lastrowid

    bill_id_int = int(last_billid)
    connection.commit()

    flash("Bill generated successfully")
    print(f"Record inserted successfully into customer bills with Bill No: {new_bill_no}")

    # Update order status
    mycursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (order_status, order_id))
    connection.commit()

    mycursor.close()

    # Now, get the product details for this bill to calculate the farmer-wise totals
    cursor = connection.cursor()

    sel_query = """
        SELECT od.*, cl.*, CAST(cl.quantity AS DECIMAL(10,2)) AS quantity, p.product_id, p.pcategory_id,
        p.farmer_id, p.product_code, p.image, p.product_name, CAST(p.rate AS DECIMAL(10,2)) AS rate,
        p.quantity AS proqty, f.farmer_id, cb.bill_id, cb.order_id, cb.bill_no, cb.bill_amount
        FROM orders od
        INNER JOIN cart_log cl ON od.cart_id = cl.cart_id
        INNER JOIN products p ON cl.product_id = p.product_id
        INNER JOIN farmer f ON p.farmer_id = f.farmer_id
        INNER JOIN customer_bill cb ON od.order_id = cb.order_id
        WHERE cb.bill_id = %s
        ORDER BY f.farmer_id ASC;
    """

    cursor.execute(sel_query, (last_billid,))
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Now calculate the total for each farmer
    farmer_totals = {}

    for order in result:
        farmer_id = order['farmer_id']
        quantity = Decimal(order['quantity']) if order['quantity'] is not None else Decimal(0)
        rate = Decimal(order['rate']) if order['rate'] is not None else Decimal(0)
        amount = quantity * rate

        if farmer_id in farmer_totals:
            farmer_totals[farmer_id] += amount  # Add to the farmer's total
        else:
            farmer_totals[farmer_id] = amount  # Initialize the farmer's total

    # Insert the farmer-wise totals into the `farmerwisebill` table
    for farmer_id, total_amount in farmer_totals.items():
        mycursor = connection.cursor()
        mycursor.execute(
            "INSERT INTO farmerwisebill(bill_id,order_id,farmer_id,amount,status) VALUES(%s, %s, %s, %s, %s)",
            (last_billid,order_id,farmer_id,total_amount,status)
        )
        connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Redirect to the view bill page
    return redirect(url_for('customer_view_singlebill', bill_id=bill_id_int))

   


@app.route("/customer_view_billDetails")
def customer_view_billDetails():

    connection = get_db_connection()
    cursor = connection.cursor()

    customer_id = session.get("userid")
   
    # Fetch the current highest bill number from the customer_bill table
    sel_query="""SELECT cb.bill_id,cb.bill_no, cb.order_id, cb.bill_amount, cb.payment_status, 
                    od.order_id AS order_id_2,od.customer_id FROM customer_bill cb
                    INNER JOIN orders od ON cb.order_id = od.order_id
                    WHERE od.customer_id =%s """

    cursor.execute(sel_query, (customer_id,))

    
    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
    # result = cursor.fetchall()
    
    # cursor.close()
    
    connection.close()
    
    return render_template("customer_billDetails.html", bill_details = result)  




@app.route("/customer_view_singlebill/<int:bill_id>", methods=["GET", "POST"])
def customer_view_singlebill(bill_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Fetch the bill details and associated products from the database
    sel_query = """
        SELECT cb.bill_id, cb.bill_no, cb.order_id, cb.bill_amount, cb.payment_status,
               od.order_id AS order_id_2,od.order_no, cl.cart_id, cl.product_id, cl.quantity, cl.rate,
               p.product_code, p.product_name
        FROM customer_bill cb
        INNER JOIN orders od ON cb.order_id = od.order_id
        INNER JOIN cart_log cl ON od.cart_id = cl.cart_id
        INNER JOIN products p ON cl.product_id = p.product_id
        WHERE cb.bill_id = %s
    """
    
    cursor.execute(sel_query, (bill_id,))
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Calculate total amount
    total_amount = sum(item['quantity'] * item['rate'] for item in result)

    connection.close()
    return render_template("generate_bill.html", bill_items=result, total =total_amount )






from flask import jsonify

@app.route("/customer_viewbill/<int:bill_id>", methods=["GET", "POST"])
def customer_viewbill(bill_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the bill details and associated products from the database
    sel_query = """
        SELECT cb.bill_id, cb.bill_no, cb.order_id, cb.bill_amount, cb.payment_status,
               od.order_id AS order_id_2, cl.cart_id, cl.product_id, cl.quantity, cl.rate,
               p.product_code, p.product_name
        FROM customer_bill cb
        INNER JOIN orders od ON cb.order_id = od.order_id
        INNER JOIN cart_log cl ON od.cart_id = cl.cart_id
        INNER JOIN products p ON cl.product_id = p.product_id
        WHERE cb.bill_id = %s
    """
    
    cursor.execute(sel_query, (bill_id,))
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Calculate total amount
    total_amount = sum(item['quantity'] * item['rate'] for item in result)

    connection.close()

    # Return the bill items and total amount as JSON
    return jsonify({
        'items': result,
        'totalAmount': total_amount
    })


@app.route("/customer_bill_payment", methods=["POST"])
def customer_bill_payment():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        bill_amount = request.form.get('bill_amount')
        bill_id = request.form.get('bill_id')
        payment_method = request.form.get('payment_method')
        date = datetime.now()
        status = "Paid"
        
        # Dummy Payment (You can replace this with actual payment gateway logic)
        if payment_method == 'upi':
            upi_id = request.form.get('upi_id')
            print(f"Payment received via UPI with ID: {upi_id}")
        elif payment_method == 'card':
            card_number = request.form.get('card_number')
            expiry_date = request.form.get('expiry_date')
            cvv = request.form.get('cvv')
            print(f"Payment received via Card - Card Number: {card_number}, Expiry: {expiry_date}, CVV: {cvv}")
        
        try:
            # Insert payment details into the database
            cursor.execute(
                "INSERT INTO bill_payment (bill_id, amount, payment_date) VALUES (%s, %s, %s)",
                (bill_id, bill_amount, date)
            )
            connection.commit()

            # Update the bill status to "Paid"
            cursor.execute(
                "UPDATE customer_bill SET payment_status = %s WHERE bill_id = %s",
                (status, bill_id)
            )
            connection.commit()

            # Return success response
            return jsonify({'success': True})

        except Exception as e:
            # Handle errors and rollback the transaction
            connection.rollback()
            print(f"Error occurred: {e}")
            return jsonify({'success': False})

        finally:
            cursor.close()
            connection.close()

    return jsonify({'success': False})




@app.route("/customer_singleBill_payment", methods=["POST"])
def customer_singleBill_payment():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == "POST":
            # Use request.get_json() to parse JSON data
            data = request.get_json()

            bill_amount = data.get('bill_amount')
            bill_id = data.get('bill_id')
            date = datetime.now()
            status = "Paid"

            # Insert payment details into the database
            cursor.execute(
                "INSERT INTO bill_payment (bill_id, amount, payment_date) VALUES (%s, %s, %s)",
                (bill_id, bill_amount, date)
            )
            connection.commit()

            # Update bill status
            cursor.execute(
                "UPDATE customer_bill SET payment_status = %s WHERE bill_id = %s",
                (status, bill_id)
            )
            connection.commit()

            cursor.execute(
                "UPDATE farmerwisebill SET status = %s WHERE bill_id = %s",
                (status, bill_id)
            )
            connection.commit()

            cursor.close()
            connection.close()

            return jsonify({'success': True})

    except Exception as e:
        # Log the error for debugging
        print(f"Error processing payment: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500




@app.route('/customer_delete_bill/<int:bill_id>', methods=['GET', 'POST'])
def customer_delete_bill(bill_id):

    connection = get_db_connection()
    mycursor = connection.cursor()
    try:
        query = "DELETE FROM customer_bill WHERE bill_id = %s"
        mycursor.execute(query, (bill_id,))
        connection.commit()
        flash('Bill deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()  
        flash('An error occurred while deleting bill.', 'error')
        print(e)
    finally:
        mycursor.close()
        connection.close()
    return redirect(url_for('customer_view_billDetails'))



# @app.route("/customer_view_Orders")
# def customer_view_Orders():

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     customer_id = session.get("userid")
   
#     # Fetch the current highest bill number from the customer_bill table
#     sel_query="""SELECT od.*,COUNT(cl.cart_log_id) AS item_count FROM orders od
#                  LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id 
#                     WHERE od.customer_id =%s GROUP BY od.order_id, od.cart_id, od.customer_id, 
#                     od.order_no, od.total_amount, od.date, od.status ORDER BY od.order_id DESC; """

#     cursor.execute(sel_query, (customer_id,))

#     columns = [desc[0] for desc in cursor.description]  # Get column names
#     result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
#     # result = cursor.fetchall()
    
#     # cursor.close()
    
#     connection.close()
    
#     return render_template("customer_viewOrders.html", order_details = result)  




# @app.route("/admin_view_Orders")
# def admin_view_Orders():

#     connection = get_db_connection()
#     cursor = connection.cursor()
   
#     sel_query="""SELECT od.*,c.customer_id,c.customer_name,COUNT(cl.cart_log_id) AS item_count FROM orders od
#                  LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id inner join customers c on od.customer_id = c.customer_id
#                  GROUP BY od.order_id, od.cart_id, od.customer_id, 
#                  od.order_no, od.total_amount, od.date, od.status ORDER BY od.order_id DESC; """

#     cursor.execute(sel_query)

#     columns = [desc[0] for desc in cursor.description]  # Get column names
#     result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
#     # result = cursor.fetchall()
    
#     # cursor.close()
    
#     connection.close()
    
#     return render_template("admin_viewOrders.html", order_details = result)  



@app.route("/admin_view_orderDetails/<int:order_id>", methods=["GET", "POST"])
def admin_view_orderDetails(order_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query to fetch order details based on order_id
    sel_query = """
        SELECT od.*, cl.*, CAST(cl.quantity AS DECIMAL(10,2)) AS quantity, p.product_id, p.pcategory_id,
        p.farmer_id, p.product_code, p.image, p.product_name, CAST(p.rate AS DECIMAL(10,2)) AS rate,
        p.quantity as proqty, f.farmer_id, f.farmer_name
        FROM orders od
        INNER JOIN cart_log cl ON od.cart_id = cl.cart_id
        INNER JOIN products p ON cl.product_id = p.product_id
        INNER JOIN farmer f ON p.farmer_id = f.farmer_id
        WHERE od.order_id = %s
        ORDER BY f.farmer_id ASC;  -- Sort by farmer_id in ascending order
    """

    # Execute the query
    cursor.execute(sel_query, (order_id,))

    # Fetch the result
    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Convert rows to dictionaries

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Render only the HTML for the modal content
    return render_template("admin_order_items_modal.html", order_details=result)




# @app.route("/customer_view_Orders")
# def customer_view_Orders():

#     connection = get_db_connection()
#     cursor = connection.cursor()

#     customer_id = session.get("userid")
   
#     # Fetch the current highest bill number from the customer_bill table
#     sql_query="""SELECT od.*,COUNT(cl.cart_log_id) AS item_count FROM orders od
#                  LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id 
#                     WHERE od.customer_id =%s GROUP BY od.order_id, od.cart_id, od.customer_id, 
#                     od.order_no, od.total_amount, od.date, od.status ORDER BY od.order_id DESC; """

#     cursor.execute(sql_query, (customer_id),multi=True)

#     columns = [desc[0] for desc in cursor.description]  # Get column names
#     result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
#     # result = cursor.fetchall()
    
#     # cursor.close()
    
#     connection.close()
    
#     return render_template("customer_viewOrders.html", order_details = result)  



@app.route("/customer_view_Orders")
def customer_view_Orders():
    connection = get_db_connection()
    cursor = connection.cursor()

    customer_id = session.get("userid")

    sql_query = """
        SELECT od.*, COUNT(cl.cart_log_id) AS item_count 
        FROM orders od
        LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id 
        WHERE od.customer_id = %s 
        GROUP BY od.order_id, od.cart_id, od.customer_id, 
                 od.order_no, od.total_amount, od.date, od.status 
        ORDER BY od.order_id DESC;
    """

    cursor.execute(sql_query, (customer_id,))  # ✅ No multi=True

    result = cursor.fetchall()  

    # Handle empty result
    if not result:
        result = []

    # Get column names
    columns = [desc[0] for desc in cursor.description] if cursor.description else []

    # Convert to dictionary
    result = [dict(zip(columns, row)) for row in result]

    connection.close()

    return render_template("customer_viewOrders.html", order_details=result)





@app.route("/admin_view_Orders")
def admin_view_Orders():

    connection = get_db_connection()
    cursor = connection.cursor()
   
    sel_query="""SELECT od.*,c.customer_id,c.customer_name,COUNT(cl.cart_log_id) AS item_count FROM orders od
                 LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id inner join customers c on od.customer_id = c.customer_id
                 GROUP BY od.order_id, od.cart_id, od.customer_id, 
                 od.order_no, od.total_amount, od.date, od.status ORDER BY od.order_id DESC; """

    cursor.execute(sel_query)

    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
    # result = cursor.fetchall()
    
    # cursor.close()
    
    connection.close()
    
    return render_template("admin_viewOrders.html", order_details = result)  




@app.route('/customer_view_orderDetails/<int:order_id>')
def customer_view_order_details(order_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
        query = """
            SELECT p.product_name, p.image, c.quantity, p.rate, 
                   (c.quantity * p.rate) AS total 
            FROM cart_log c
            JOIN products p ON c.product_id = p.product_id
            JOIN `orders` o ON c.cart_id = o.cart_id
            WHERE o.order_id = %s
        """
        cursor.execute(query, (order_id,))
        order_items = cursor.fetchall()  # Fetch all results
        cursor.close()
        
        return render_template("customer_order_details_modal.html", order_items=order_items)

    except Error as e:
        print(f"Error: {e}")
        return "An error occurred while fetching order details", 500

    


@app.route("/admin_view_CustomerBills", methods=["GET", "POST"])
def admin_view_CustomerBills():

    connection = get_db_connection()
    cursor = connection.cursor()
   
    # Fetch the current highest bill number from the customer_bill table
    sel_query="""SELECT cb.bill_id,cb.bill_no, cb.order_id, cb.bill_amount, cb.payment_status, 
                    od.order_id AS order_id_2,od.order_no,od.customer_id FROM customer_bill cb
                    INNER JOIN orders od ON cb.order_id = od.order_id
                   """

    cursor.execute(sel_query)

    
    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
    # result = cursor.fetchall()
    
    # cursor.close()
    
    connection.close()
    
    return render_template("admin_ViewBillDetails.html", bill_details = result)



@app.route('/admin_delete_bill/<int:bill_id>', methods=['GET', 'POST'])
def admin_delete_bill(bill_id):

    connection = get_db_connection()
    mycursor = connection.cursor()
    try:
        query = "DELETE FROM customer_bill WHERE bill_id = %s"
        mycursor.execute(query, (bill_id,))
        connection.commit()
        flash('Bill deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()  
        flash('An error occurred while deleting bill.', 'error')
        print(e)
    finally:
        mycursor.close()
        connection.close()
    return redirect(url_for('admin_view_CustomerBills'))




@app.route('/admin_send_notification/<int:land_details_id>', methods=['POST'])
def admin_send_notification(land_details_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # ✅ Check if the land is approved
    cursor.execute("SELECT status FROM land_details WHERE land_details_id = %s", (land_details_id,))
    status = cursor.fetchone()

    if status and status[0].lower() == "approved":  # Only send notification if approved
        if request.method == "POST":
            matter = request.form.get('admin_remark')
            date = datetime.now()
            insert_query = "INSERT INTO notification (land_details_id, matter, date) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (land_details_id, matter, date))
            connection.commit()

            flash('Notification sent successfully.', 'success')
    else:
        flash('The land is not approved yet.', 'danger')  # Show error message if not approved

    cursor.close()
    connection.close()

    return redirect(url_for('admin_land_details'))


@app.route('/notification_management',methods=['GET'])
def notification_management():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM notification"
    cursor.execute(query)
    ar_obj=cursor.fetchall()

    return render_template('admin_notification.html',ar_obj=ar_obj)


@app.route('/farmer_land_notification',methods = ['GET'])
def farmer_land_notification():
    
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch all notifications (both seen and unseen)
    query = """
    SELECT n.not_id, n.matter, n.date, ld.upload 
    FROM notification n
    JOIN land_details ld ON n.land_details_id = ld.land_details_id
    """
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    # Fetch only UNSEEN notifications for the count
    count_query = "SELECT COUNT(*) FROM notification"
    cursor.execute(count_query)
    notification_count = cursor.fetchone()[0]  # Get unread count

    cursor.close()
    connection.close()

    return render_template('farmer_land_notification.html', ar_obj=ar_obj, count=notification_count)



@app.context_processor
def inject_notification_count():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT COUNT(*) FROM notification"
    cursor.execute(query)
    notification_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return dict(notification_count=notification_count)  # Available in all templates



@app.route('/send_land_enquiry/<int:not_id>', methods=['POST'])
def send_land_enquiry(not_id):
    enquiry_message = request.form.get('enquiry_message')  # Enquiry message from form field
    farmer_id = session.get('userid') 

    if not farmer_id:
        flash("Session expired. Please log in again.", "error")
        return redirect(url_for('login'))  
 
    
    # Validate form data
    if not (enquiry_message):
        flash("Enquiry message are required.", "error")
        return redirect(url_for('farmer_land_notification'))

    # Database connection
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
            INSERT INTO land_enquiry (not_id,farmer_id,matter,date,status)
            VALUES (%s,%s,%s,NOW(),'Sent')
        """
    try:
        cursor.execute(query, (not_id, farmer_id, enquiry_message))
        connection.commit()
        flash("Enquiry sent successfully.", "success")
    except Exception as e:
        print("Database Insertion Error:", e)  # Print any errors
        flash("Error inserting enquiry. Try again.", "error")
    
    cursor.close()
    connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('farmer_land_notification'))



@app.route('/view_land_enquiry')
def view_land_enquiry():
    land_owner_id = session.get('userid') 
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT 
    f.farmer_id,
    f.farmer_name,  -- Get farmer name
    le.matter,      -- Enquiry matter
    le.date,        -- Enquiry date
    le.status       -- Enquiry status
    FROM land_enquiry le
    JOIN notification n ON le.not_id = n.not_id  -- Link enquiry to notifications
    JOIN land_details ld ON n.land_details_id = ld.land_details_id  -- Link to land details
    JOIN farmer f ON le.farmer_id = f.farmer_id  -- Get farmer details
    WHERE ld.land_owner_id = %s  """
    cursor.execute(query,(land_owner_id,))
    ar_obj=cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('land_enquiry.html',ar_obj=ar_obj)



@app.route('/send_land_reply/<int:land_enquiry_id>',methods = ['POST'])
def send_land_reply(land_enquiry_id):
    reply = request.form.get('reply_message')
    lease_amount = request.form.get('lease_amount')
    file = request.files.get('upload')  # Get the uploaded file

    # Validate form data
    if not (reply):
        flash("reply message are required.", "error")
        return redirect(url_for('view_land_enquiry'))

    if file:
        filename = secure_filename(file.filename)  # Ensure the filename is safe
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file

    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """ INSERT into land_enquiry_reply (land_enquiry_id,reply,date,MOU,lease_amount)values(%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(query,(land_enquiry_id,reply,datetime.now(),filename,lease_amount))
        connection.commit()
        flash("Enquiry sent successfully.", "success")
    except Exception as e:
        print("Database Insertion Error:", e)  # Print any errors
        flash("Error inserting enquiry. Try again.", "error")
    
    cursor.close()
    connection.close()

    return redirect(url_for('view_land_enquiry'))



@app.route('/view_land_reply',methods = ['GET'])
def view_land_reply():
    farmer_id = session.get('userid')
    connection = get_db_connection()
    cursor = connection.cursor()

    if not farmer_id:
        return "Error: No farmer ID found in session", 400

    print("Farmer ID:", farmer_id)  # Debugging

    query = """ SELECT
    ler.enquiry_reply_id,
    lo.landowner_name, 
    ld.village_name, 
    ld.total_area, 
    ld.land_type, 
    ld.upload AS land_image, 
    ler.reply, 
    ler.date, 
    ler.MOU,
    ler.lease_amount 
    FROM 
    land_enquiry le
    JOIN 
    land_details ld ON le.not_id = ld.land_details_id
    JOIN 
    land_owners lo ON ld.land_owner_id = lo.landowner_id
    JOIN  -- Change from LEFT JOIN to JOIN
    land_enquiry_reply ler ON le.land_enquiry_id = ler.land_enquiry_id
    WHERE 
    le.farmer_id = %s
    AND ler.reply IS NOT NULL"""
    cursor.execute(query,(farmer_id,))
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close() 
    
    return render_template('view_land_reply.html',ar_obj=ar_obj)

@app.route('/farmer_add_products',methods = ['GET','POST'])
def farmer_add_products():
    connection = get_db_connection()
    cursor = connection.cursor()

    farmer_id = session.get('userid')

    # Fetch area list for dropdown
    cursor.execute("SELECT pcategory_id,category_name FROM product_category")
    pdtcategory_obj = cursor.fetchall()

    if request.method == 'POST':
        # Fetch form data
        pdtcategory = request.form.get('pdtcategory')
        product_code = request.form.get('product_code')
        product_name = request.form.get('product_name')
        rate = request.form.get('rate')
        quantity = request.form.get('quantity')

        # ✅ Initialize filename to avoid UnboundLocalError
        filename = None

        # Handle file upload
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
        else:
            filename = "no_file_uploaded"  # Default value if no file is uploaded

        # ✅ Insert into MySQL
        insert_query = """INSERT INTO products(pcategory_id, farmer_id, product_code,product_name, image,rate, quantity)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (pdtcategory, farmer_id, product_code,product_name, filename,rate, quantity)

        try:
            cursor.execute(insert_query, values)  
            connection.commit()
            flash("Product inserted successfully", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    cursor.close()
    connection.close()

    return render_template('farmer_add_products.html',pdtcategory_obj=pdtcategory_obj)



@app.route('/upload_mou', methods=['POST'])
def upload_mou():
    if 'mou_file' not in request.files:
        flash('No file selected')
        return redirect(request.referrer)

    file = request.files['mou_file']
    landreply_id = request.form.get('landreply_id')

    status = "confirm"
    if file.filename == '':
        flash('No file selected')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to confirmation table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO land_enquiry_confirmation (enquiry_reply_id, mou_upload,status) VALUES (%s, %s, %s)", (landreply_id, filename,status))
        connection.commit()
        cursor.close()
        connection.close()

        flash('MOU uploaded successfully!')
        return redirect(url_for('view_land_reply'))
    
    flash('Invalid file format')
    return redirect(request.referrer)




@app.route('/view_mou')
def view_mou():
    land_owner_id = session['userid']
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT 
    f.farmer_id,
    f.farmer_name,  -- Get farmer name
    lec.mou_upload,      -- Enquiry matter
    lec.status       -- Enquiry status
    FROM land_enquiry_confirmation lec
    JOIN land_enquiry_reply ler ON lec.enquiry_reply_id = ler.enquiry_reply_id
    JOIN land_enquiry le ON ler.land_enquiry_id = le.land_enquiry_id
    JOIN notification n ON le.not_id = n.not_id  -- Link enquiry to notifications
    JOIN land_details ld ON n.land_details_id = ld.land_details_id  -- Link to land details
    JOIN farmer f ON le.farmer_id = f.farmer_id  -- Get farmer details
    WHERE ld.land_owner_id = %s """
    cursor.execute(query,(land_owner_id,))
    ar_obj=cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('view_mou.html',ar_obj=ar_obj)


@app.route("/download_mou")
def download_mou():
    connection = get_db_connection()
    cursor = connection.cursor()
    # Fetch the latest MOU filename from the database
    cursor.execute("SELECT mou_upload FROM lease_agreement_form")
    result = cursor.fetchone()

    cursor.close()
    connection.close()
 
    flash('MOU downloaded successfully.')
   
    return redirect(url_for('landowner_home'))



@app.route('/get_lease_agreements')
def get_lease_agreements():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Fetch data as a dictionary

    query = "SELECT * FROM lease_agreement_form"
    cursor.execute(query)
    lease_agreements = cursor.fetchall()
    
    cursor.close()
    connection.close()

    return jsonify(lease_agreements)



@app.route('/lease_payment/<int:enquiry_reply_id>',methods = ['GET','POST'])
def lease_payment(enquiry_reply_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """SELECT lec.confirmation_id
               FROM land_enquiry_confirmation lec
               JOIN land_enquiry_reply ler
               ON ler.enquiry_reply_id = lec.enquiry_reply_id
               WHERE ler.enquiry_reply_id = %s"""
    cursor.execute(query,(enquiry_reply_id,))
    confirmation_result = cursor.fetchone()

    if confirmation_result:
        confirmation_id = confirmation_result[0]  # Extract confirmation_id from tuple
    else:
        flash("No confirmation found for this enquiry!", "error")
        cursor.close()
        connection.close()
        return redirect(url_for('view_land_reply'))
    

    if request.method == 'POST':
       lease_amount = request.form.get('lease_amount')
       date = datetime.now()

       insert_query ="INSERT into lease_payment(confirmation_id,amount,date)values(%s,%s,%s)"

       try:
        cursor.execute(insert_query,(confirmation_id,lease_amount,date))
        connection.commit()
        flash(" Payment sent successfully.", "success")
       except Exception as e:
        print("Database Insertion Error:", e)  # Print any errors
        flash("Error inserting enquiry. Try again.", "error")
    
       update_query = """UPDATE land_enquiry 
        SET status = 'completed'  
        WHERE land_enquiry_id = (
        SELECT land_enquiry_id FROM land_enquiry_reply WHERE enquiry_reply_id = %s
        )"""
       cursor.execute(update_query,(enquiry_reply_id,))
       connection.commit()

       cursor.close()
       connection.close()

       return redirect(url_for('view_land_reply'))




@app.route("/farmer_view_Orders")
def farmer_view_Orders():

    connection = get_db_connection()
    cursor = connection.cursor()

    farmer_id = session.get("userid")
   
    sel_query="""SELECT od.*,c.customer_id,c.customer_name,COUNT(cl.cart_log_id) AS item_count,p.product_id,p.farmer_id
                 FROM orders od LEFT JOIN cart_log cl ON od.cart_id = cl.cart_id 
                 inner join customers c on od.customer_id = c.customer_id
                 inner join products p
                 on cl.product_id = p.product_id where p.farmer_id = %s
                 GROUP BY od.order_id, od.cart_id, od.customer_id, 
                 od.order_no, od.total_amount, od.date, od.status ORDER BY od.order_id DESC; """

    cursor.execute(sel_query,(farmer_id,))

    columns = [desc[0] for desc in cursor.description]  # Get column names
    result = [dict(zip(columns, row)) for row in cursor.fetchall()] #Convert to dicts
    # result = cursor.fetchall()
    
    # cursor.close()
    
    connection.close()
    
    return render_template("farmer_viewOrders.html", order_details = result)  



from decimal import Decimal
from flask import render_template, session

@app.route("/farmer_view_orderDetails/<int:order_id>", methods=["GET", "POST"])
def farmer_view_orderDetails(order_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    farmer_id = session.get("userid")
    
    sel_query = """
        SELECT od.*, cl.*, CAST(cl.quantity AS DECIMAL(10,2)) AS quantity, p.product_id, p.pcategory_id,
        p.farmer_id, p.product_code, p.image, p.product_name, CAST(p.rate AS DECIMAL(10,2)) AS rate,
        p.quantity AS proqty, f.farmer_id
        FROM orders od
        INNER JOIN cart_log cl ON od.cart_id = cl.cart_id
        INNER JOIN products p ON cl.product_id = p.product_id
        INNER JOIN farmer f ON p.farmer_id = f.farmer_id
        WHERE od.order_id = %s and p.farmer_id = %s
        ORDER BY f.farmer_id ASC;
    """

    cursor.execute(sel_query, (order_id, farmer_id))

    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in cursor.fetchall()]

    grand_total = Decimal(0)
    
    for order in result:
        quantity = Decimal(order['quantity']) if order['quantity'] is not None else Decimal(0)
        rate = Decimal(order['rate']) if order['rate'] is not None else Decimal(0)
        print(f"Product: {order['product_name']}, Quantity: {quantity}, Rate: {rate}")
        amount = quantity * rate
        grand_total += amount

    cursor.close()
    connection.close()

    return render_template("farmer_order_items_modal.html", order_details=result, grand_total=grand_total)



@app.route('/farmer_view_billDetails', methods=['GET'])
def farmer_view_billDetails():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve the farmer_id from the session
    farmer_id = session.get("userid")

    if not farmer_id:
        print("farmer_id not found in session")  # Debug log
        return jsonify({'error': 'Unauthorized', 'message': 'Farmer ID not found in session.'}), 401

    print(f"farmer_id found in session: {farmer_id}")  # Debug log

    # SQL query to fetch bill details with proper join
    query = """
        SELECT fb.farmer_bill_id, fb.bill_id, fb.order_id, fb.farmer_id, fb.amount, fb.status, cb.bill_no,
            cb.bill_amount,od.order_id,od.order_no FROM farmerwisebill fb
            INNER JOIN customer_bill cb ON fb.bill_id = cb.bill_id 
            inner join orders od on fb.order_id = od.order_id
            WHERE fb.farmer_id = %s;
    """
    cursor.execute(query, (farmer_id,))
    result = cursor.fetchall()

    # Transform the result to a list of dictionaries (for easier access in Jinja templates)
    bill_details = []
    for row in result:
        bill_details.append({
            'farmer_bill_id': row[0],
            'bill_id': row[1],
            'order_id': row[2],
            'farmer_id': row[3],
            'amount': row[4],
            'status': row[5],
            'bill_no': row[6],
            'bill_amount': row[7],
            'order_no':row[9]
        })

    cursor.close()
    connection.close()

    return render_template("farmer_viewBillDetails.html", bill_details=bill_details)



@app.route('/Product_Category', methods=['GET', 'POST'])
def Product_Category():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == "POST":
        category_name = request.form.get('category_name')
        insert_query = "INSERT INTO product_category (category_name) VALUES (%s)"
        cursor.execute(insert_query, (category_name,))
        connection.commit()
        flash("Record inserted successfully")

        return redirect(url_for("pdtcategory"))
    
    # Fetch all area records when the method is GET
    query = "SELECT * FROM product_category"
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('pdtcategory.html', ar_obj=ar_obj)


@app.route('/admin_insurance_management', methods=['GET', 'POST'])
def admin_insurance_management():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == "POST":
        insurance_type_name = request.form.get('insurance_type_name')
        premium_amount = request.form.get('premium_amount')
        coverage_amount = request.form.get('coverage_amount')
        policy_terms = request.form.get('policy_terms')
        insert_query = "INSERT INTO insurance_type(insurance_type_name,premium_amount,coverage_amount,policy_terms) VALUES (%s,%s,%s,%s)"
        cursor.execute(insert_query, (insurance_type_name,premium_amount,coverage_amount,policy_terms))
        connection.commit()
    
        flash("Record inserted successfully")
        return redirect(url_for("admin_insurance_management"))

    query = "SELECT * FROM insurance_type"
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return render_template('admin_insurance_mgmt.html', ar_obj=ar_obj) 



@app.route('/admin_edit_insurance/<int:insurance_type_id>', methods=['POST'])
def admin_edit_insurance(insurance_type_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get form data
    insurance_type_name = request.form.get('insurance_type_name')
    premium_amount = request.form.get('premium_amount')
    coverage_amount = request.form.get('coverage_amount')
    policy_terms = request.form.get('policy_terms')

    # Update the database
    update_query = """
        UPDATE insurance_type 
        SET insurance_type_name=%s, premium_amount=%s, coverage_amount=%s, policy_terms=%s
        WHERE insurance_type_id=%s
    """
    cursor.execute(update_query, (insurance_type_name, premium_amount, coverage_amount, policy_terms, insurance_type_id))
    connection.commit()

    flash("Insurance record updated successfully")
    cursor.close()
    connection.close()

    return redirect(url_for("admin_insurance_management"))



@app.route('/admin_delete_insurance/<int:insurance_type_id>', methods=['POST'])
def admin_delete_insurance(insurance_type_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = " DELETE FROM insurance_type WHERE insurance_type_id = %s "
    cursor.execute(query,(insurance_type_id,))
    connection.commit()

    flash('Record deleted successfully')
    cursor.close()
    connection.close()

    return redirect(url_for("admin_insurance_management"))



@app.route('/farmer_view_products')
def farmer_view_products():
    farmer_id = session['userid']
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch products
    query = """ 
    SELECT
        p.product_id,    
        pc.category_name,
        p.product_code,
        p.product_name,
        p.image AS image,
        p.rate,
        p.quantity
    FROM products p
    JOIN product_category pc ON pc.pcategory_id = p.pcategory_id
    WHERE farmer_id = %s
    """
    cursor.execute(query, (farmer_id,))
    ar_obj = cursor.fetchall()

    # Fetch product categories
    cursor.execute("SELECT pcategory_id, category_name FROM product_category")
    pdtcategory_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    # ✅ Pass `pdtcategory_obj` to the template
    return render_template('farmer_view_pdts.html', ar_obj=ar_obj, pdtcategory_obj=pdtcategory_obj)

    

@app.route('/farmer_edit_product/<int:product_id>', methods=['POST'])
def farmer_edit_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    farmer_id = session['userid']

    cursor.execute("SELECT pcategory_id,category_name FROM product_category")
    pdtcategory_obj = cursor.fetchall()

    if request.method == 'POST':
        # Fetch form data
        pdtcategory = request.form.get('pdtcategory')
        product_code = request.form.get('product_code')
        product_name = request.form.get('product_name')
        rate = request.form.get('rate')
        quantity = request.form.get('quantity')


        # ✅ Insert into MySQL
        update_query = "UPDATE products SET pcategory_id=%s, farmer_id=%s, product_code=%s,product_name=%s,rate=%s,quantity=%s WHERE product_id=%s"
        values = (pdtcategory, farmer_id, product_code,product_name, rate, quantity,product_id)

        try:
            cursor.execute(update_query, values)  
            connection.commit()
            flash("Product updated successfully", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    cursor.close()
    connection.close()

    return redirect(url_for('farmer_view_products'))



@app.route('/farmer_delete_product/<int:product_id>', methods=['POST'])
def farmer_delete_product(product_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = " DELETE FROM products WHERE product_id = %s "
    cursor.execute(query,(product_id,))
    connection.commit()

    flash('Product deleted successfully')
    cursor.close()
    connection.close()

    return redirect(url_for("farmer_view_products"))


@app.route('/admin_loan_management', methods=['GET', 'POST'])
def admin_loan_management():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    if request.method == "POST":
        scheme_name = request.form.get('scheme_name')
        maximum_amount = request.form.get('maximum_amount')
        maturity_period = request.form.get('maturity_period')
        file = request.files.get('terms_and_conditions')

        # Save policy document
        filename = None
        if file and file.filename:
           filename = secure_filename(file.filename)
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           file.save(file_path)

        # Insert into policy table
        insert_query = """
              INSERT INTO loan_type(scheme_name,terms_and_conditions,maximum_amount,maturity_period)
              VALUES (%s, %s, %s, %s)"""
        values = (scheme_name, filename, maximum_amount, maturity_period)

        try:
           cursor.execute(insert_query, values)
           connection.commit()
           flash("Record inserted successfully", "success")
        except Exception as e:
           flash(f"Error: {str(e)}", "danger")

        return redirect(url_for("admin_loan_management"))

    query = "SELECT * FROM loan_type"
    cursor.execute(query)
    ar_obj = cursor.fetchall()
    connection.commit()

    cursor.close()
    connection.close()
    
    return render_template('admin_loan_mgmt.html', ar_obj=ar_obj) 

@app.route('/admin_edit_loan/<int:loan_type_id>', methods=['POST'])
def admin_edit_loan(loan_type_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get form data
    scheme_name = request.form.get('scheme_name')
    maximum_amount = request.form.get('maximum_amount')
    maturity_period = request.form.get('maturity_period')
    
    # Update the database
    update_query = """
        UPDATE loan_type 
        SET scheme_name=%s, maximum_amount=%s, maturity_period=%s
        WHERE loan_type_id=%s
    """
    cursor.execute(update_query, (scheme_name, maximum_amount, maturity_period, loan_type_id))
    connection.commit()

    flash("Loan record updated successfully")
    cursor.close()
    connection.close()

    return redirect(url_for("admin_loan_management"))

@app.route('/admin_delete_loan/<int:loan_type_id>', methods=['POST'])
def admin_delete_loan(loan_type_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = " DELETE FROM loan_type WHERE loan_type_id = %s "
    cursor.execute(query,(loan_type_id,))
    connection.commit()

    flash('Record deleted successfully')
    cursor.close()
    connection.close()

    return redirect(url_for("admin_loan_management"))


@app.route('/admin_upload_mou', methods=['POST'])
def admin_upload_mou():
    if 'mou_file' not in request.files:
        flash('No file selected')
        return redirect(request.referrer)

    file = request.files['mou_file']
    type = "lease agreement"

    if file.filename == '':
        flash('No file selected')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to confirmation table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO lease_agreement_form (mou_upload,type) VALUES (%s,%s)", (filename,type))
        connection.commit()
        cursor.close()
        connection.close()

        flash('MOU uploaded successfully!')
        return redirect(url_for('admin_home'))
    
    flash('Invalid file format')
    return redirect(request.referrer)


@app.route('/admin_upload_forms', methods=['POST'])
def admin_upload_forms():
    if 'form_file' not in request.files:
        flash('No file selected')
        return redirect(request.referrer)

    file = request.files['form_file']
    type = request.form.get('form_type')

    if file.filename == '':
        flash('No file selected')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to confirmation table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO forms(form_type,upload_form) VALUES (%s,%s)", (type,filename))
        connection.commit()
        cursor.close()
        connection.close()

        flash('Form uploaded successfully!')
        return redirect(url_for('admin_home'))
    
    flash('Invalid file format')
    return redirect(request.referrer)    


@app.route('/admin_view_insurance_application')
def admin_view_insurance_application():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT
    pa.p_application_id, 
    it.insurance_type_name,
    f.farmer_name,
    pa.upload,
    pa.admin_reply,
    pa.farmer_confirmation,
    pa.status,
    pa.date
    FROM policy_application pa 
    JOIN insurance_type it ON pa.insurance_type_id = it.insurance_type_id
    JOIN farmer f ON pa.farmer_id = f.farmer_id """
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_view_ins_appln.html',ar_obj=ar_obj)

# @app.route('/farmer_download_ins_form')
# def farmer_download_ins_form():

#     connection = get_db_connection()
#     cursor = connection.cursor()
#     # Fetch available forms
#     cursor.execute("SELECT * FROM forms WHERE form_type='insurance'")
#     result_data = cursor.fetchall()  # ✅ Fetch results immediately
#     cursor.close()
    
#     cursor = connection.cursor()
#     # Fetch insurance types
#     cursor.execute("SELECT * FROM insurance_type")
#     insurance_obj = cursor.fetchall()  # ✅ Fetch results immediately
#     cursor.close()
#     connection.close()

#     return render_template('farmer_download_ins_form.html',result_data=result_data,insurance_obj=insurance_obj)



@app.route('/farmer_download_ins_form')
def farmer_download_ins_form():

    connection = get_db_connection()
    if connection is None:
        return "Failed to connect to the database."

    cursor = connection.cursor()
    try:
        # Fetch available forms
        cursor.execute("SELECT * FROM forms WHERE form_type='insurance'")
        result_data = cursor.fetchall()  # ✅ Fetch results immediately

        # Fetch insurance types
        cursor.execute("SELECT * FROM insurance_type")
        insurance_obj = cursor.fetchall()  # ✅ Fetch results immediately
    except Exception as e:
        cursor.close()
        connection.close()
        return f"Error executing queries: {str(e)}"

    cursor.close()
    connection.close()

    return render_template('farmer_download_ins_form.html', result_data=result_data, insurance_obj=insurance_obj)


@app.route('/upload_insurance_form', methods=['POST'])
def upload_insurance_form():
    if 'form_file' not in request.files:
        flash('No file selected')
        return redirect(request.referrer)
    
    farmer_id = session['userid']
    insurance_type_id = request.form.get('insurance_type')
    file = request.files['form_file']
    form_id = request.form.get('form_id')
    status = 'sent'
    date = datetime.now()

    if file.filename == '':
        flash('No file selected')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to confirmation table
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO policy_application (insurance_type_id, farmer_id,upload,status,date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query,(insurance_type_id,farmer_id,filename,status,date))
        connection.commit()
        flash('Form uploaded successfully!')

        cursor.close()
        connection.close()

        return redirect(url_for('farmer_download_ins_form'))
    
    flash('Invalid file format')
    return redirect(request.referrer)


@app.route('/farmer_view_policy_reply')
def farmer_view_policy_reply():
    farmer_id = session['userid']
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT p.policy_id,
    p.p_application_id,
    p.policy_number,
    p.policy_details,
    p.start_date,
    p.end_date,
    it.premium_amount,
    pa.status,
    p.policy_document
    FROM policy p
    JOIN policy_application pa ON p.p_application_id = pa.p_application_id
    JOIN insurance_type it ON pa.insurance_type_id = it.insurance_type_id
    WHERE farmer_id=%s """
    cursor.execute(query,(farmer_id,))
    ar_obj = cursor.fetchall()

    cursor.execute("SELECT upload_form FROM forms WHERE form_type = 'certificate'")
    certificate = cursor.fetchone()
    certificate_file = certificate[0] if certificate else None 
    
    cursor.close
    connection.close

    return render_template('farmer_view_policy_reply.html',ar_obj=ar_obj,certificate_file=certificate_file)

@app.route('/policy_payment/<int:policy_id>',methods = ['POST'])
def policy_payment(policy_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    amount = request.form.get('policy_payment')
    date = datetime.now()
    
    query = " INSERT INTO policy_payment (policy_id,amount,date)VALUES(%s,%s,%s) "
    cursor.execute(query,(policy_id,amount,date))
    connection.commit()
    
    flash("Payment sent successfully")

    update_query =""" UPDATE policy_application pa
    JOIN policy p ON pa.p_application_id = p.p_application_id
    SET pa.farmer_confirmation = 'confirmed',
    pa.status = 'completed'
    WHERE p.policy_id = %s """
    cursor.execute(update_query,(policy_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for('farmer_view_policy_reply'))




@app.route('/farmer_view_loan_types')
def farmer_view_loan_types():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch insurance types
    cursor.execute("SELECT * FROM loan_type")
    loan_obj = cursor.fetchall()  # ✅ Fetch results immediately

    cursor.close()
    connection.close()

    return render_template('farmer_view_loans.html',loan_obj=loan_obj)




@app.route('/farmer_download_loan_form')
def farmer_download_loan_form():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch available forms
    cursor.execute("SELECT * FROM forms WHERE form_type='loan'")
    result_data = cursor.fetchall()  # ✅ Fetch results immediately

    # Fetch insurance types
    cursor.execute("SELECT * FROM loan_type")
    loan_obj = cursor.fetchall()  # ✅ Fetch results immediately

    cursor.close()
    connection.close()

    return render_template('farmer_download_loan_form.html',result_data=result_data,loan_obj=loan_obj)

@app.route('/upload_loan_form', methods=['POST'])
def upload_loan_form():
    if 'form_file' not in request.files:
        flash('No file selected')
        return redirect(request.referrer)
    
    farmer_id = session['userid']
    loan_type_id = request.form.get('loan_type')
    loan_amount = request.form.get('loan_amount')
    file = request.files['form_file']
    form_id = request.form.get('form_id')
    status = 'sent'
    date = datetime.now()

    if file.filename == '':
        flash('No file selected')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save to confirmation table
        connection = get_db_connection()
        cursor = connection.cursor()

        query = "INSERT INTO loan_application (loan_type_id, farmer_id,loan_amount,upload,date,status) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(loan_type_id,farmer_id,loan_amount,filename,date,status))
        connection.commit()
        flash('Form uploaded successfully!')

        cursor.close()
        connection.close()

        return redirect(url_for('farmer_download_loan_form'))
    
    flash('Invalid file format')
    return redirect(request.referrer)

@app.route('/admin_view_loan_application')
def admin_view_loan_application():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT
    la.loan_app_id, 
    lt.scheme_name,
    f.farmer_name,
    la.loan_amount,
    la.upload,
    la.date,
    la.status
    FROM loan_application la 
    JOIN loan_type lt ON la.loan_type_id = lt.loan_type_id
    JOIN farmer f ON la.farmer_id = f.farmer_id """
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_view_loan_appln.html',ar_obj=ar_obj)    



@app.route('/view_mou_confirmation')
def view_mou_confirmation():
    land_owner_id = session['userid']
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """ SELECT 
    f.farmer_id,
    f.farmer_name,  -- Get farmer name
    lec.mou_upload,      -- Enquiry matter
    lec.status       -- Enquiry status
    FROM land_enquiry_confirmation lec
    JOIN land_enquiry_reply ler ON lec.enquiry_reply_id = ler.enquiry_reply_id
    JOIN land_enquiry le ON ler.land_enquiry_id = le.land_enquiry_id
    JOIN notification n ON le.not_id = n.not_id  -- Link enquiry to notifications
    JOIN land_details ld ON n.land_details_id = ld.land_details_id  -- Link to land details
    JOIN farmer f ON le.farmer_id = f.farmer_id  -- Get farmer details
    WHERE ld.land_owner_id = %s """
    cursor.execute(query,(land_owner_id,))
    ar_obj=cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('landowner_view_mou.html',ar_obj=ar_obj)




@app.route('/landowner_delete_landdetails/<int:land_details_id>', methods=['GET', 'POST'])
def landowner_delete_landdetails(land_details_id):

    connection = get_db_connection()
    mycursor = connection.cursor()
    try:
        query = "DELETE FROM land_details WHERE land_details_id = %s"
        mycursor.execute(query, (land_details_id,))
        connection.commit()
        flash('Land_details deleted successfully!', 'success')
    except Exception as e:
        connection.rollback()  
        flash('An error occurred while deleting land details.', 'error')
        print(e)
    finally:
        mycursor.close()
        connection.close()
    return redirect(url_for('landowner_view_land_details'))





@app.route('/admin_policy_approval/<int:p_application_id>',methods =['POST'])
def admin_policy_approval(p_application_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Get insurance_type_id from policy_application table
    cursor.execute("SELECT insurance_type_id FROM policy_application WHERE p_application_id = %s", (p_application_id,))
    insurance_type = cursor.fetchone()

    if not insurance_type:
        flash("Invalid application ID", "danger")
        return redirect(url_for('admin_view_insurance_application'))

    insurance_type_id = insurance_type[0]

    # Fetch policy terms from insurance_type table
    cursor.execute("SELECT policy_terms FROM insurance_type WHERE insurance_type_id = %s", (insurance_type_id,))
    policy_term = cursor.fetchone()

    if not policy_term:
        flash("Invalid insurance type", "danger")
        return redirect(url_for('admin_view_insurance_application'))

    policy_term = policy_term[0]  # Extract value

    # Convert policy terms to number of days
    term_days = {
        "6 months": 180,
        "1 year": 365
    }.get(policy_term, 0)  # Default to 0 if not found

    if term_days == 0:
        flash("Invalid policy term format", "danger")
        return redirect(url_for('admin_view_insurance_application'))

    # Calculate start_date and end_date
    start_date = datetime.today()
    end_date = start_date + timedelta(days=term_days)  # Add days directly

     # Generate a new policy number
    policy_number = generate_policy_number()

    # Get form data
    policy_details = request.form.get('policy_details')
    file = request.files.get('form_file')

    # Save policy document
    filename = None
    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    # Insert into policy table
    insert_query = """
    INSERT INTO policy (p_application_id,policy_number, policy_details, start_date, end_date, policy_document)
    VALUES (%s, %s,%s, %s, %s, %s)
    """
    values = (p_application_id,policy_number, policy_details, start_date, end_date, filename)

    try:
        cursor.execute(insert_query, values)
        connection.commit()
        flash("Policy approved successfully", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")

    update_query = "UPDATE policy_application SET admin_reply = 'replied' WHERE p_application_id = %s"
    cursor.execute(update_query, (p_application_id,))
    connection.commit()  # Commit only if update was successful

    cursor.close()
    connection.close()

    return redirect(url_for('admin_view_insurance_application'))

def generate_policy_number():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Count the number of policies in the policy table
    cursor.execute("SELECT COUNT(*) FROM policy")
    policy_count = cursor.fetchone()[0]

    policy_prefix = "PLC-"
    next_number = policy_count + 1  # Auto-increment based on existing records

    new_policy_number = f"{policy_prefix}{next_number:03d}"  # Format with leading zeros
    cursor.close()
    connection.close()
    
    return new_policy_number





@app.route('/admin_view_insurance_claim')
def admin_view_insurance_claim():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    farmer_id = session['userid']

    # Fetch available forms
    query = """SELECT f.farmer_name, icr.claim_id, icr.policy_number, icr.reason, 
               icr.upload, icr.remark, icr.date, icr.status
               FROM insurance_claim_request icr
               JOIN farmer f ON icr.farmer_id = f.farmer_id"""
    cursor.execute(query)           
    result_data = cursor.fetchall()  # ✅ Fetch results immediately

    cursor.close()
    connection.close()

    return render_template('admin_view_ins_claim.html',result_data = result_data)




@app.route('/admin_send_insclaim_reply/<int:claim_id>', methods=['POST'])
def admin_send_insclaim_reply(claim_id):
  
    remark = request.form.get('remark')  # Enquiry message from form field

    # Database connection
    connection = get_db_connection()
    if not connection:
        flash("Database connection error.", "error")
        return redirect(url_for('admin_view_insurance_claim'))

    try:
        cursor = connection.cursor()

        # Insert the enquiry into complaint_enquiries table
        query = " UPDATE insurance_claim_request SET remark = %s WHERE claim_id = %s "
        cursor.execute(query, (remark, claim_id))
        connection.commit()

        update_query = " UPDATE insurance_claim_request SET status = 'claimed' where claim_id=%s"
        cursor.execute(update_query, (claim_id,))
        connection.commit()

        flash("Reply sent successfully.", "success")
    except Exception as e:
        print(f"Error sending reply: {e}")  # Replace with logging in production
        flash("Failed to send reply. Please try again.", "error")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Redirect to complaints page or another appropriate page
    return redirect(url_for('admin_view_insurance_claim'))




@app.route('/admin_loan_processing/<int:loan_app_id>',methods = ['POST'])
def admin_loan_processing(loan_app_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    admin_reply = request.form.get('admin_reply')
    date = datetime.now()

    query = " INSERT INTO application_process(loan_app_id,admin_reply,date) values(%s,%s,%s) "
    cursor.execute(query,(loan_app_id,admin_reply,date))
    connection.commit()

    update_query = "UPDATE loan_application SET status = 'admin replied' WHERE loan_app_id = %s "
    cursor.execute(update_query,(loan_app_id,))

    flash("Record inserted successfully.")

    cursor.close()
    connection.close()

    return redirect(url_for('admin_view_loan_application'))

@app.route('/admin_view_processing_loans',methods =['GET','POST'])
def admin_view_processing_loans():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """SELECT 
    ap.process_id,
    f.farmer_id,
    lt.scheme_name,
    f.farmer_name,
    la.loan_amount
    FROM application_process ap
    JOIN loan_application la ON la.loan_app_id = ap.loan_app_id
    JOIN loan_type lt ON lt.loan_type_id = la.loan_app_id
    JOIN farmer f ON la.farmer_id = f.farmer_id"""
    cursor.execute(query)
    ar_obj = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_loan_sanction.html',ar_obj=ar_obj)

@app.route('/admin_loan_sanction/<int:process_id>',methods = ['GET','POST'])
def admin_loan_sanction(process_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'GET':
        # Render a form page (create a 'loan_sanction.html' file)
        return redirect(url_for('admin_loan_sanction', process_id=process_id))

    elif request.method == 'POST':

       query = """SELECT lt.maturity_period
       FROM loan_type lt 
       JOIN loan_application la ON la.loan_type_id = lt.loan_type_id
       JOIN application_process ap ON ap.loan_app_id = la.loan_app_id
       WHERE process_id = %s"""
       cursor.execute(query,(process_id,))
       maturity_period = cursor.fetchone()

       if not maturity_period:
          flash("Invalid ", "danger")
          return redirect(url_for('admin_view_processing_loans'))

       maturity_period = maturity_period[0]  # Extract value

       try:
          years = int(maturity_period.split()[0])  # Extract first part (e.g., "1" from "1 year")
          period_days = years * 365  # Convert years to days
       except ValueError:
          flash(f"Invalid maturity period format: {maturity_period}", "danger")
          return redirect(url_for('admin_view_processing_loans'))

       # Calculate start_date and end_date
       start_date = datetime.today()
       loan_end_date = start_date + timedelta(days=period_days)  # Add days directly
    
       loan_amount = request.form.get('loan_amount')
       sanctioned_date = datetime.now()
       emi_amount = request.form.get('emi_amount')
       remark = request.form.get('remark')

       insert_query = "INSERT INTO loans(process_id,loan_amount,sanctioned_date,loan_end_date,emi_amount,remark)values(%s,%s,%s,%s,%s,%s)"
       cursor.execute(insert_query,(process_id,loan_amount,sanctioned_date,loan_end_date,emi_amount,remark))
       connection.commit()

       update_query = """ UPDATE loan_application la
       JOIN application_process ap ON la.loan_app_id = ap.loan_app_id
       JOIN loans l ON ap.process_id = l.process_id
       SET la.status = 'sanctioned'
       WHERE ap.process_id = %s """
       cursor.execute(update_query,(process_id,))
       connection.commit()

       flash("Loan sanctioned successfully.")
    
       cursor.close()
       connection.close()

       return redirect(url_for('admin_view_loan_application', process_id=process_id))






@app.route('/farmer_send_insurance_claim')
def farmer_send_insurance_claim():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Fetch available forms
    cursor.execute("SELECT * FROM forms WHERE form_type='insurance_claim'")
    result_data = cursor.fetchall()  # ✅ Fetch results immediately

    # Fetch insurance types
    cursor.execute("SELECT * FROM insurance_type")
    insurance_obj = cursor.fetchall()  # ✅ Fetch results immediately

    return render_template('farmer_send_insurance_claim.html',result_data=result_data,insurance_obj=insurance_obj)

@app.route('/upload_insurance_claim_form', methods=['POST'])
def upload_insurance_claim_form():
    if 'form_file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(request.referrer)
    
    if 'userid' not in session:
        flash('Please log in first', 'danger')
        return redirect(url_for('login'))

    farmer_id = session['userid']
    insurance_type_id = request.form.get('insurance_type')
    reason = request.form.get('reason')  # Assuming a reason field exists in the form
    status = 'sent'
    date = datetime.now()

    # Connect to database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch policy_number for the logged-in farmer
    query = """SELECT p.policy_number, it.insurance_type_name
               FROM policy p
               JOIN policy_application pa ON p.p_application_id = pa.p_application_id
               JOIN insurance_type it ON pa.insurance_type_id = it.insurance_type_id
               WHERE pa.farmer_id = %s;"""
    cursor.execute(query, (farmer_id,))
    policy_number = cursor.fetchone()

    if not policy_number:
        flash('No policy found for this farmer', 'danger')
        return redirect(request.referrer)

    policy_number = policy_number[0]  # Extract policy_number from tuple

    file = request.files['form_file']
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Insert into insurance_claim_table
            query2 = """
                INSERT INTO insurance_claim_request (farmer_id, policy_number, reason, upload, date, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query2, (farmer_id, policy_number, reason, filename, date, status))

            connection.commit()
            flash('Insurance claim form uploaded successfully!', 'success')

        except Exception as e:
            connection.rollback()
            flash(f"Error: {str(e)}", 'danger')

        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('farmer_send_insurance_claim'))

    flash('Invalid file format', 'danger')
    return redirect(request.referrer)




@app.route('/farmer_view_claim_reply')
def farmer_view_claim_reply():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch remark, date, and status
    query = """SELECT icr.remark, icr.date, icr.status
               FROM insurance_claim_request icr"""
    
    cursor.execute(query)  # ✅ Execute the query
    ar_obj = cursor.fetchall()  # ✅ Fetch results

    cursor.close()
    connection.close()

    return render_template('farmer_view_claim_reply.html', ar_obj=ar_obj)


@app.route('/admin_report')
def admin_report():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """SELECT ld.land_owner_id,l.landowner_name,ld.area_id,a.area_name,ld.village_name,ld.total_area,ld.survey_no,ld.land_type,le.farmer_id,f.farmer_name,lp.amount,le.status 
    FROM land_details ld 
    JOIN notification n ON ld.land_details_id = n.land_details_id 
    JOIN land_enquiry le ON n.not_id = le.not_id 
    JOIN land_enquiry_reply ler ON le.land_enquiry_id = ler.land_enquiry_id 
    JOIN land_enquiry_confirmation lec ON ler.enquiry_reply_id = lec.enquiry_reply_id 
    JOIN lease_payment lp ON lec.confirmation_id = lp.confirmation_id 
    JOIN area a ON a.area_id = ld.area_id 
    JOIN farmer f ON f.farmer_id = le.farmer_id 
    JOIN land_owners l ON l.landowner_id = ld.land_owner_id;"""
    cursor.execute(query)
    lease_obj = cursor.fetchall()  # ✅ Fetch results

    policy_query = """SELECT pa.insurance_type_id,i.insurance_type_name,pa.farmer_id,f.farmer_name,pa.admin_reply,pa.farmer_confirmation,
    p.policy_number,p.start_date,p.end_date,pp.amount,pp.date,pa.status 
    FROM insurance_type i 
    JOIN policy_application pa ON i.insurance_type_id = pa.insurance_type_id 
    JOIN policy p ON pa.p_application_id = p.p_application_id  
    JOIN policy_payment pp ON p.policy_id = pp.policy_id  
    JOIN farmer f ON f.farmer_id = pa.farmer_id;"""
    cursor.execute(policy_query)
    policy_obj = cursor.fetchall()  # ✅ Fetch results

    bill_query = """ SELECT 
            o.order_id,
            c.customer_name,
            c.address,
            o.order_no,
            COUNT(cl.product_id) AS total_products,
            o.total_amount,
            o.date AS payment_date,
            o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN cart_log cl ON o.cart_id = cl.cart_id
        GROUP BY o.order_id
        ORDER BY o.date DESC"""

    cursor.execute(bill_query)
    orders = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('admin_reports.html', lease_obj=lease_obj,policy_obj=policy_obj,orders=orders)



# Ensure this block is executed only when the script is run directly
if __name__ == '__main__':
    app.run(debug=True)
