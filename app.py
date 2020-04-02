from Work import *
from flask import Flask, render_template,redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


##### CONSTANTS #####
DB_NAME = "SophieOpferman.db"
CATEGORIES = ("nonfiction", "original", "derivative")
#####################



@app.route("/")
def main():
    return render_template('index.html')

@app.route("/programming")
def programming():
    return render_template('programming.html', WORKS=getDatabaseEntries("programming"))

@app.route("/writing")
def writing():
    return render_template('writing.html', CATEGORIES=CATEGORIES, WORKS=getDatabaseEntries("writing"))

@app.route("/music")
def music():
    return render_template('music.html', WORKS=getDatabaseEntries("music"))

@app.route("/resume")
def resume():
    return render_template('resume.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/i-think-theyre-funny-okay")
def funny():
    return render_template('funny-things.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)


############################# database stuff ##########################
def openDB():
    engine = create_engine("sqlite:///" + DB_NAME)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def getDatabaseEntries(cat):
    session = openDB()
    return session.query(Work).filter(Work.category == cat).order_by(Work.updated.desc()).all()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
