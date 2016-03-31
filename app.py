#!/usr/bin/python
import os
from flask import Flask, render_template, request
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage
from flask import send_from_directory
import dateutil
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def main():
"""rendering the index page"""
    return render_template('index.html')


def create_mask(x):
"""creating subnet mask from CIDR"""
    mask=''
    for i in range(1,33):
        if int(i) <= int(x) :
            mask='1'+mask
        else:
            mask='0'+mask
    subnet_mask=''
    sum=0
    count=0
    digit_location=0
    for i in mask:
        #converting binary to decimal
        sum+=(2**digit_location)*int(i)
        digit_location+=1
        if digit_location%8==0:
            if count<=2:
                subnet_mask=str(sum)+subnet_mask   #adding to get the octal sum
                subnet_mask=str('.')+subnet_mask   #placing the '.'
                count+=1
            else:
                subnet_mask=str(sum)+subnet_mask
            sum=0
            digit_location=0
    return subnet_mask



def make_binary(x):
"""converting from decimal to binary"""
    binary=''
    while x>0:
        binary=str(x%2)+binary
        x=x/2
    return binary


#x = ip address y= subnet mask
def validate(x,y):
"""validating the ip address and subnet mask""" 
    x_group=x.split(".")
    y_group=y.split(".")  
    
    #checking id 4 groups are present
    if len(x_group) != 4:
        return bool(0)
    if len(y_group) != 4:
        return bool(0)
    err = bool(1)
    binary = ""
    #validating subnet mask
    for i in y_group:
        if i.isdigit():
            if not int(i) > 256:
                #converting to binary and checking for consecutive 1's
                binary =binary + str(make_binary(int(i)))
                if len(binary)<= 7:
                    for i in range (len(binary),9):
                        binary = binary + "0"
            else:                           #number is greater than 255
                return bool(0)
        else:                               #number is not a digit
            return bool(0)
    
    #found first occurence after 0th position 
    if binary.find("1") > 0:
        return bool(0)
    step1 = binary.find("1")
    if step1 != -1:
        # 1 is present in subnet mask
        if step1 != 0:
            return bool(0)
        step0 = binary.find("0")
        if step0 != -1:
            if binary.find("1",step0) != -1:
                return bool(0)               # found 1 after 0
    #validating ip address checking if it is in the range 0-255
    for i in x_group:
        if i.isdigit():
            if not int(i) > -1:
                err = bool(0)
            if not int(i) < 256:
                err = bool(0)
        else:
            err = bool(0)

    return err



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
"""upload the file and parse it to get  the required keywords"""
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        answer = ""
        error_format = 0
        count = 0
        for line in open(f.filename):  # opened in text-mode; all EOLs are converted to '\n'
            line = line.rstrip('\n')
            count += 1
            date_status = line[:line.find("[")].strip(" ")
            components = date_status.split(" ")
            log_level = ['ERROR','INFO','DEBUG']
            if not components[-1] in log_level:
                log_status = "false"
                error_format = 1
            else:
                #capturing log level
                log_status = components[-1]
                timelog = date_status[:date_status.find(components[-1])].strip(" ")
            #checking the time against the various formats
            try:
                datefield = datetime.utcnow().strptime(timelog,'%Y-%m-%d %H:%M:%S,%f')
            except:
                try:
                    datefield = dateutil.parser.parse(timelog)
                except:
                    try:
                        datefield = datetime.utcnow().strptime(timelog,'%d-%m-%Y %H:%M:%S,%f')
                    except:
                        try:
                            datefield = datetime.utcnow().strptime(timelog,'%m-%d-%Y %H:%M:%S,%f')
                        except:
                            try:
                                datefield = datetime.utcnow().strptime(timelog,'%Y-%d-%m %H:%M:%S,%f')
                            except:
                                datefield = "false"
            if datefield == "false":
                error_format = 1
            else:
                if timelog.find(',')!=-1:
                    milisec = int(timelog[timelog.find(',')+1:])
                #%f captures the microseconds, hence this test is necessary
                if milisec > 1000:     
                    datefield == "false"
                    error_format = 1
                else:
                    #timelog is captured the next field is the [user:main:sub] group which are tested together
                    rest=line[line.find("["):]
                    func_msg=rest.split(" ")
                    line1= func_msg[0]
                    main=""
                    user=""                           
                    subfunc=""
                    if line1.find('[') != 0:    # the bracket is missing
                        user_func = "false"     
                        error_format = 1
                    else:
                        if line1.find(':') == 1:            #user is absent
                            user = "false"
                            error_format = 1
                        else:
                            user = line1[1:line1.find(':')]
                            if(line1.count(':')) == 1:          #subfunc is absent
                                main = line[(line1.find(':')+1):line1.find(']')]
                                subfunc = "undefined"
                            else:
                                print user
                                if(line1.count(':'))==2:
                                    secondcolon = line1.find(':',(line1.find(':')+1))
                                    main = line1[(line1.find(':')+1):secondcolon]
                                    subfunc = line1[secondcolon+1:-1]
                                else:                           #invalid format
                                    user_func = "false"
                                    error_format = 1
                    if line1[-1] != ']':                #closing bracket missing
                        user_func = "false"
                        error_format = 1
                    if not main:                        #main function missing
                        main = "false"
                        error_format = 1
                    if not subfunc:
                        subfunc = "false"               
                        error_format = 1
                    msg=line[line.find(']')+1:].strip(" ")      #the rest of the line
                    # the flaf is not set
                    if error_format == 0:
                        answer += "<br><br>Line "+str(count)+") <strong>Date: </strong>"+str(timelog)+"<br><strong>Log Status: </STRONG><br>"+str(log_status)
                        answer+= "<br><strong>User: </strong>"+str(user)+"<br><strong>Main Function: </strong><br>"+str(main)+"<strong>Subfunction:  </strong>"+str(subfunc)                    
                        answer+= "<br><strong>Message: </strong><br>"+str(msg)
                    #flag is set                            
                    else:
                        answer+= "<br><br>Line "+ str(count)+") wrong log"
            
        return answer

@app.route('/problem1')
def prob1():
"""rendering the page of the first problem"""    
    return render_template('problem1.html')

@app.route('/problem2')
def prob2():
"""rendering the page of the second problem"""
    return render_template('problem2.html')

@app.route('/prob1_solution',methods=['POST','GET'])
def index():
"""rendering the solution of the first problem"""
    # read the posted values from the UI
    _ip = request.form['ip']
    _mask = request.form['mask']
    _cidr = request.form['cidr']
    #convert cidr to subnet_mask usking create_mask() 
    if _cidr:
        if not _cidr.isnumeric():
            error = 'Invalid input formats</span><br><a href="/">Back</a>'
            return error
        _mask=create_mask(_cidr)
    
    
    # validate the received values
    valid = validate(_ip,_mask)
    
    if not valid:
        error = 'Invalid input formats</span><br><a href="/">Back</a>'
        print "The given format is invalid"
        return error
    else:
        print "The information given is valid"
    
    ip_groups=_ip.split(".")
    mask_groups=_mask.split(".")
    network_address = ""
    host_address = ""
    print "network_address"
    counter = 0
    #calculating the values that is ip & mask for network address and ip & ~mask for host address
    for x, y in map(None,ip_groups,mask_groups):
        print x , y
        network_address += str(int(x) & int(y))
        host_address += str(int(x) & ~int(y))
        counter += 1
        if counter <= 3:
            network_address += ":"
            host_address += ":"
            
            
    print "Network address=" + str(network_address)
    print "Host address=" + str(host_address)
    response="<span><strong>Network address: "+network_address+"</strong></span><br><span><strong>Host address: "+host_address+"</strong></span><br><br><a href='/'>Back</a>"
    
    return response
    
    
if __name__ == "__main__":
    app.run()
