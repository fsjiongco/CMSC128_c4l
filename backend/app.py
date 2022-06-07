import asyncio
from logging import root
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from queries import *
from csv_reader import *
from setup import *
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

client_dist_folder = "../frontend/dist"

app = Flask(__name__, static_folder=f"{client_dist_folder}/assets")
CORS(app)
jwt = JWTManager(app)

@app.route('/')
@app.route('/<path:path>')
def index(path=""):
    return send_from_directory(client_dist_folder, "index.html")

@app.route('/api/students')
def getStudents():
    args = request.args
    print(args.get("offset"))
    print(args)
    students = get_all_students('last_name', 'ASC', args.get("offset"),args.get("limit"))         # last_name kapag by name, # degree_program kapag by course | ASC or DESC
    student_count = get_num_of_students()
    #paged = get_all_students_by5(args.get("offset"),args.get("limit"))
    return {"students": students, "totalStudentCount": student_count}

@app.route('/api/students/<string:student_number>')
def getStudent(student_number):
    student = get_student(student_number)
    general_errors = get_student_flags(student_number)
    errors = get_student_data_flags(student_number)
    return {"student": student, "genError": general_errors, "dataFlags" :errors}

@app.route('/api/login', methods = ['POST'])
def get_credentials():
    
    creds = request.get_json()
    username = creds['email']
    password = creds['password']
    valid, faculty = check_credentials(username, password)
    # access_token = create_access_token(identity=username)
    print('test')
    return {"success": valid, "faculty":faculty}
        # return {'success': False}

@app.route('/api/students/<string:student_number>/courses/<string:course_code>', methods = ['DELETE'])
@jwt_required()
def delete_student_course(student_number, course_code):
    details = request.get_json()
    try:
        delete_studentData(details['student_number'], details['course_number'], details['semester'], details['academic_year'])
        return {'success': True}
    except:
        return {'success': False}

@app.route('/api/students', methods = ['POST'])
def add_student():
    details = request.get_json()
    try:
        # student_id, first_name, last_name, degree_program, gwa, total_units, req_units, total_cumulative
        insert_student(details['student_number'], details['first_name'], details['last_name'], details['degree_program'], details['gwa'], details['total_units'], details['req_units'], details['total_cumulative'])
        return {'success': True}
    except:
        return {'success': False} 

@app.route('/api/students/<string:student_number>', methods = ['PATCH'])
@jwt_required()
def edit_students(student_number):
    details = request.get_json()
    edit_student(details['student_id'], details['col_name'], details['new_data'])
    print(details["justification"])
    
    record_changelogs("initial test",details['student_id'],'to test the gwa verifier', details['col_name'],"10","10")
    return {'success': True}
        # return {'success': False}

@app.route('/api/students', methods = ['DELETE'])
@jwt_required()
def del_student():
    details = request.get_json()
    print("delete student")
    print(details)
    delete_student(details['student_number'])
    return {'success': True }

@app.route('/api/students/<string:student_number>/courses/<string:course_code>', methods = ['PATCH'])
@jwt_required()
def edit_student_course(student_number, course_code):
    details = request.get_json()
    print(details["student_number"])
    print(details["col_name"])
    print(details["new_data"])
    print(details["acad_year"])
    print(details["semester"])
    # print(details["justification"])
    try:
        # FORMAT from frontend: {'student_number': '5698-61298', 'course_number': 'ENG 1(AH)', 'grade': '2', 'units': 3, 'weight': 6, 'cumulative': 6}
        # EXAMPLE FORMAT NG JSON para sa BACKEND: {'student_number': '1234-12345', 'col_name': 'grade', 'new_data': 3, 'prev_data': 2, 'semester': '2', 'acad_year': '15/16'}
        # basically, yung parameters na need ng edit_studentData ay (student_number, col_name, new_data, prev_data, semester, acad_year)
        edit_studentData('studentData', details['student_number'], details['col_name'], details['new_data'], details['semester'], details['acad_year'], course_code)
        print("recording changelogs...")
        record_changelogs('helloworld', details['student_number'], 'justification', details['col_name'], details['prev_data'], details['new_data'])
        return {'success': True}
    except:
        return {'success': False}
    

# record_changelogs(faculty_id, student_id, justification, col_name, prev_data, new_data)


# for student data row (add row, edit row and delete row)

# PENDING
@app.route('/api/students/<string:id>/courses', methods = ['POST'])
def add_student_course(id):
    course_details = request.get_json()
    try:
        add_studentData(course_details['student_number'], course_details['course_number'], course_details['grade'], course_details['units'], course_details['weight'], course_details['cumulative'], course_details['semester'] )
        return {'success': True}
    except:
        return {'success': False}

@app.route('/api/students:file', methods = ['POST'])
def read_file(): 
    import tkinter as tk
    print("read file")
    from tkinter.filedialog import askopenfilenames
    # file = request.files.get("file")
    # fileData = file.read()
    root = tk.Tk()
    
    root.attributes('-topmost',True, '-alpha',0)
    filepath = askopenfilenames(parent=root, title='Choose a file/s')
    root.withdraw()
    for file in filepath:
        backend_setup(read_csv_xlsx(file))
    # root.mainloop()
    #student_data = read_csv_xlsx(filepath)
    
    
    return {'success': True}

@app.route('/api/change-logs', methods = ['GET'])
def get_all_changelogs():
    args = request.args
    print("get changelogs")
    print(args)
    changelogs = get_changelogs(args.get("sort_by"), 'ASC', args.get("offset"), args.get("limit"))
    return {"changelogs": changelogs, "totalChangeLogCount": changelogs.length}

@app.route('/api/users', methods = ['GET'])
def get_users():
    faculty = get_all_faculties()
    return {"staff": faculty}

@app.route('/api/users', methods = ['POST'])
def add_user():
    
    faculty = request.get_json()
    successful = add_faculty(faculty['email'], faculty['password'], faculty['faculty_id'], faculty['name'], faculty['department'], faculty['access_level'])
    return {'success': True} if successful else {'success': False}
    
@app.route('/api/users', methods = ['DELETE'])
def delete_users():
    faculty = request.get_json()
    successful = delete_faculty_member(faculty['faculty_id'])
    return {'success': True} if successful else {'success': False}

@app.route('/api/users/<string:faculty_id>', methods = ['PATCH'])
def edit_user(faculty_id):
    data = request.get_json()
    if(len(data) == 2):
        successful = edit_faculty_name(data['faculty_id'], data['student_id'], data['justification'], data['col_name'], data['prev_data'], data['new_data'])
    else:
        successful = edit_faculty_password(data['faculty_id'], data['old_pw'], data['new_pw'])
    return {'success': True} if successful else {'success': False}
