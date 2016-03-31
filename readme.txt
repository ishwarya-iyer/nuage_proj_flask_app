PROCESS TO INSTALL FLASK FOR YOUR application:
1)Right Click on 'MY COMPUTER' OR 'THIS PC' icon present on the left column of your file system and choose Properties.
2)This will take you to a control panels page. Click on 'Advanced system settings' -> Environmental variables and search for the python path in 'System variables' It will have the variable name 'Path' and just choose the path starting from C:
(it will mostly be of the format C:\Python(version)\Scripts)
3)Open a cmd prompt do cd \
4)
C:\> pip install virtualenv
Create a directory for project that is-nuage_proj so place it in the C drive.
5)go inside the project by 
C:\> cd nuage_proj
C:\>virtualenv flask
6) Since flask and all libraries are already present you dont have to install them. In case interested then follow these steps:
	C:\>pipflask\Scripts\pip install flask
7) To run the file:
C:\>cd \
C:\>cd nuage_proj\flask\Scripts
C:\>activate
C:\> cd\
C:\> cd nuage_proj\app
C:\>python app.py
it will give a url when you go to the url, you can see the application working
Some test cases are available in the app->test

