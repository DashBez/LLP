from flask import Flask,render_template
#from webapp_fashion.data_upload  import get_info_goods
from webapp_fashion.model import db,News


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    

    @app.route('/') 
    def index():
        title = 'Магазин' 
        result_info = News.query.all()
        #get_info_goods()               
        return render_template('index.html',page_title=title,result_info=result_info)
    return  app

   # def Cut_name():
        # if len(Name)>40:
            # Name = Name[0:40]

    #    return "Name"
        # return render_template('index.html',clever_function=clever_function)
   
    #app.jinja_env.globals.update(Cut_name=Cut_name) 