
from flask import render_template, request, url_for, redirect, flash, jsonify, session
from functools import wraps
from app import app
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
engine = create_engine('sqlite:///school.db')
models.Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db = DBSession()


### Log in and log out function

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('categoryPage', category_id = 1))
	return wrap

@app.route('/login', methods=['GET','POST'])
def login():
	error =  None
	if request.method == 'POST':
		users = db.query(models.Parents).all()
		users = {i.name:i.children_id for i in users}
		print(users)
		if request.form['username'] == "admin" or request.form['password'] == "admin":
			session['logged_in'] = True
			return redirect(url_for('admin'))
		elif request.form['username'] in users.keys():
			return redirect(url_for('journal', children_id = users[request.form['username']]))
		else:
			error = "Username or password is not correct. Please try again"
			category = db.query(models.Category).filter_by(id= 1).one()
			return render_template('cateqgory.html', category = category, articles = [], error = error)			

	return render_template('category.html', category = category, articles = [])

@app.route('/logout', methods=['POST','GET'])
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('categoryPage', category_id = 1))

###! end Log in and log out function

### Admin function

@app.route('/admin')
@login_required
def admin():
	category = db.query(models.Category).all()
	return render_template('admin.html', category = category)

@app.route('/admin/')
@app.route('/admin/<int:category_id>')
@login_required
def adminCategory(category_id=1):
	category = db.query(models.Category).filter_by(id= category_id).one()
	articles = db.query(models.Article).filter_by(category_id = category_id).all()
	return render_template('adminmodels.Category.html', category = category,  articles = articles)

@app.route('/admin/new/<int:category_id>', methods=['GET','POST'])
@login_required
def adminNewArticle(category_id=1):
	if request.method == "POST":
		newArticle = models.Article(name = request.form['name'], text= request.form['text'], category_id = category_id)
		db.add(newArticle)
		db.commit()
		return redirect(url_for('adminmodels.Category', category_id = category_id))
	else:
		category = db.query(models.Category).filter_by(id = category_id).one()
		return render_template('adminNewArticle.html', category = category)

@app.route('/admin/edit/<int:category_id>/', methods=['GET','POST'])
@app.route('/admin/edit/<int:category_id>/<int:article_id>', methods=['GET','POST'])
@login_required
def adminEditArticle(category_id=1,article_id=1):
	article = db.query(models.Article).filter_by(id = article_id).one()
	if request.method == "POST":
		if request.form['name']:
			article.name = request.form['name']
		if request.form['text']:
			article.text = request.form['text']
		db.add(article)
		db.commit()
		return redirect(url_for('adminmodels.Category', category_id = category_id))
	else:
		category = db.query(models.Category).filter_by(id = category_id).one()
		return render_template('adminEditArticle.html', article = article, category = category)

@app.route('/admin/delete/<int:category_id>/', methods=['GET','POST'])
@app.route('/admin/delete/<int:category_id>/<int:article_id>', methods=['GET','POST'])
@login_required
def adminDeleteArticle(category_id=1,article_id=1):
	article = db.query(models.Article).filter_by(id = article_id).one()
	if request.method == "POST":
		db.delete(article)
		db.commit()
		return redirect(url_for('/admin/<int:category_id>', category_id = category_id))
	else:
		category = db.query(models.Category).filter_by(id = category_id).one()
		return render_template('adminDeleteArticle.html', article = article, category = category)


@app.route('/admin/newParent', methods=['GET','POST'])
def adminNewParent():
	if request.method == "POST":
		if request.form['parent'] and request.form['children_id']:
			newParent = models.Parents(name = request.form['parent'], children_id = request.form['children_id'])
			db.add(newParent)
			db.commit()
			print(newParent.name)
	return redirect(url_for('admin'))

@app.route('/admin/newChildren', methods=['GET','POST'])
def adminNewChildren():
	if request.method == "POST":
		if request.form['children'] and request.form['class_id']:
			class_id = int(request.form['class_id'])
			newChildren = models.Children(name = request.form['children'], class_id = class_id)
			db.add(newChildren)
			db.commit()
			print(newChildren.name)
	return redirect(url_for('admin'))

@app.route('/admin/newSubject', methods=['GET','POST'])
def adminNewSubject():
	if request.method == "POST":
		if request.form['subject']:
			newSubject = models.Subject(name = request.form['subject'])
			db.add(newSubject)
			db.commit()
			print(newSubject.name)
	return redirect(url_for('admin'))

@app.route('/admin/newClass', methods=['GET','POST'])
def adminNewClass():
	if request.method == "POST":
		if request.form['class']:
			newClass = models.Class(name = request.form['class'])
			db.add(newClass)
			db.commit()
			print(newClass.name)
	return redirect(url_for('admin'))

@app.route('/admin/newMark', methods=['GET','POST'])
def adminNewMark():
	if request.method == "POST":
		if request.form['mark'] and request.form['class_id'] and request.form['children_id'] and request.form['subject_id']:
			newMark = models.Marks(mark = request.form['mark'], subject_id = request.form['subject_id'], 
				children_id = request.form['children_id'], class_id = request.form['class_id'])
			db.add(newMark)
			db.commit()
			print(newMark.mark)
	return redirect(url_for('admin'))


###! end Admin function

@app.route('/')
@app.route('/index')
@app.route('/index/')
def indexPage():
	return render_template('index.html')

@app.route('/journal/<int:children_id>')
def journal(children_id = 1):
	category = db.query(models.Category).filter_by(id= 6).one()
	children = db.query(models.Children).filter_by(id = children_id).one()
	subject = db.query(models.Subject).all()
	sub_mark = {}
	sub = {i.id:i.name for i in subject}
	for i in sub.keys():
		marks = db.query(models.Marks).filter_by(subject_id=i,children_id=children.id)
		sub_mark[sub[i]] = [z.mark for z in marks]
	return render_template('article.html',category=category,children=children,
		cl=db.query(models.Class).filter_by(id = children.class_id).one(), sub_mark = sub_mark)



@app.route('/category')
@app.route('/category/')
@app.route('/category/<int:category_id>')
def categoryPage(category_id=1):
	category = db.query(models.Category).filter_by(id= category_id).one()
	articles = db.query(models.Article).filter_by(category_id = category_id).all()
	return render_template('category.html', category = category, articles = articles)

@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/<int:article_id>')
def articlePage(category_id=1,article_id=1):
	category = db.query(models.Category).filter_by(id = category_id).one()
	article = db.query(models.Article).filter_by(id = article_id).one()
	return render_template('article.html', article = article, category = category)