from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
import json
import traceback
import models as models
from models import *
from sqlalchemy import or_, and_

from forms import SignupForm, LoginForm, HeroForm, PlayerForm, AchievementForm, RewardForm, DeleteForm

views = Blueprint('views', __name__)


@views.route('/') 
def index():
	""" Returns Welcome Page """
	return render_template('index.html')

@views.route("/ov_loader")
def ov_loader():
	return render_template('ov_loader.html')

@views.route('/tests/run')
def run_tests():
	""" Runs all the unittests and returns the text result with verbosity 2 """
	import test_runner as test_runner
	return test_runner.run_tests()


@views.route('/api/players', methods=['GET'])
def players():
	""" Returns Players Page """
	if ("player page" not in session):
		session["player page"] = 1
	if ("player order" not in session):
		session["player order"] = "ascending"
	if ("player filter" not in session):
		session["player filter"] = "non"
	
	if type(request.args.get('page')) is unicode:
		session["player page"] = int(request.args.get('page'))
	if type(request.args.get('order')) is unicode:
		session["player order"] = str(request.args.get('order'))
	if type(request.args.get('filter')) is unicode:
		session["player filter"] = str(request.args.get('filter'))

	""" Returns Players Page """
	if session["player order"] == "ascending":
		if session["player filter"] == "non":
			data = models.Player.query.order_by(models.Player.name.asc()).all()
		elif session["player filter"] == "us":
			data = models.Player.query.order_by(models.Player.name.asc()).filter(Player.server == 'us').all()
		elif session["player filter"] == "kr":
			data = models.Player.query.order_by(models.Player.name.asc()).filter(Player.server == 'kr').all()
		else:
			data = models.Player.query.order_by(models.Player.name.asc()).filter(Player.server == 'eu').all()
	else:
		if session["player filter"] == "non":
			data = models.Player.query.order_by(models.Player.name.desc()).all()
		elif session["player filter"] == "us":
			data = models.Player.query.order_by(models.Player.name.desc()).filter(Player.server == 'us').all()
		elif session["player filter"] == "kr":
			data = models.Player.query.order_by(models.Player.name.desc()).filter(Player.server == 'kr').all()
		else:
			data = models.Player.query.order_by(models.Player.name.desc()).filter(Player.server == 'eu').all()
		
	
	if not data:
		return render_template('404.html', thing='Players')
	output = data[9 * (session["player page"] - 1): 9 * session["player page"]]

	return render_template('players.html', data=data, output=output, page = session["player page"], order = session["player order"], filter = session["player filter"])
	


@views.route('/api/players/<int:player_id>', methods=['GET'])
def player(player_id):
	""" Returns Page for a single Player """
	data = models.Player.query.get(player_id)
	if not data:
		return render_template('404.html', thing='Player')

	return render_template('players_instance.html', data=data)


@views.route('/api/heroes', methods=['GET'])
def heroes():
	if ("hero page" not in session):
		session["hero page"] = 1
	if ("hero order" not in session):
		session["hero order"] = "ascending"
	if ("hero filter" not in session):
		session["hero filter"] = "non"
	
	if type(request.args.get('page')) is unicode:
		session["hero page"] = int(request.args.get('page'))
	if type(request.args.get('order')) is unicode:
		session["hero order"] = str(request.args.get('order'))
	if type(request.args.get('filter')) is unicode:
		session["hero filter"] = str(request.args.get('filter'))

	""" Returns Heroes Page """
	if session["hero order"] == "ascending":
		if session["hero filter"] == "non":
			data = models.Hero.query.order_by(models.Hero.name.asc()).all()
		elif session["hero filter"] == "Overwatch":
			data = models.Hero.query.order_by(models.Hero.name.asc()).filter(Hero.affiliation == 'Overwatch').all()
		else:
			data = models.Hero.query.order_by(models.Hero.name.asc()).filter(Hero.affiliation != 'Overwatch').all()
	else:
		if session["hero filter"] == "non":
			data = models.Hero.query.order_by(models.Hero.name.desc()).all()
		elif session["hero filter"] == "Overwatch":
			data = models.Hero.query.order_by(models.Hero.name.desc()).filter(Hero.affiliation == 'Overwatch').all()
		else:
			data = models.Hero.query.order_by(models.Hero.name.desc()).filter(Hero.affiliation != 'Overwatch').all()
		
	
	if not data:
		return render_template('404.html', thing='Heroes')
	output = data[9 * (session["hero page"] - 1): 9 * session["hero page"]]

	return render_template('heroes.html', data=data, output=output, page = session["hero page"], filter = session["hero filter"], order = session["hero order"])


@views.route('/api/heroes/<int:hero_id>', methods=['GET'])
def hero(hero_id):
	""" Returns Page for a single Hero """
	data = models.Hero.query.get(hero_id)
	if not data:
		return render_template('404.html', thing='Hero')
	
	return render_template('heroes_instance.html', data=data)


@views.route('/api/rewards', methods=['GET'])
def rewards():
	if ("reward page" not in session):
		session["reward page"] = 1
	if ("reward order" not in session):
		session["reward order"] = "Low Cost"
	if ("reward filter" not in session):
		session["reward filter"] = "non"
	
	if type(request.args.get('page')) is unicode:
		session["reward page"] = int(request.args.get('page'))
	if type(request.args.get('order')) is unicode:
		session["reward order"] = str(request.args.get('order'))
	if type(request.args.get('filter')) is unicode:
		session["reward filter"] = str(request.args.get('filter'))

	""" Returns Rewards Page """
	if session["reward order"] == "Low Cost":
		if session["reward filter"] == "non":
			data = models.Reward.query.order_by(models.Reward.cost.asc()).all()
		elif session["reward filter"] == "From Achievements":
			data = models.Reward.query.order_by(models.Reward.cost.asc()).filter(Reward.achievement_id != None).all()
		else:
			data = models.Reward.query.order_by(models.Reward.cost.asc()).filter(Reward.achievement_id == None).all()
	else:
		if session["reward filter"] == "non":
			data = models.Reward.query.order_by(models.Reward.cost.desc()).all()
		elif session["reward filter"] == "From Achievements":
			data = models.Reward.query.order_by(models.Reward.cost.desc()).filter(Reward.achievement_id != None).all()
		else:
			data = models.Reward.query.order_by(models.Reward.cost.desc()).filter(Reward.achievement_id == None).all()
	
	if not data:
		return render_template('404.html', thing='Rewards')
	output = data[16 * (session["reward page"] - 1): 16 * session["reward page"]]

	return render_template('rewards.html', data=data, output=output, page= session["reward page"], order =  session["reward order"], filter = session["reward filter"])


@views.route('/api/rewards/<int:reward_id>', methods=['GET'])
def reward(reward_id):
	""" Returns Page for a single Reward """
	data = models.Reward.query.get(reward_id)
	if not data:
		return render_template('404.html', thing='Reward')
	
	return render_template('rewards_instance.html', data=data)



@views.route('/api/achievements', methods=['GET'])
def achievements():
	""" Returns Achievements Page """
	if ("achievement page" not in session):
		session["achievement page"] = 1
	if ("achievement order" not in session):
		session["achievement order"] = "ascending"
	if ("achievement filter" not in session):
		session["achievement filter"] = "non"
	
	if type(request.args.get('page')) is unicode:
		session["achievement page"] = int(request.args.get('page'))
	if type(request.args.get('order')) is unicode:
		session["achievement order"] = str(request.args.get('order'))
	if type(request.args.get('filter')) is unicode:
		session["achievement filter"] = str(request.args.get('filter'))

	""" Returns Achievement Page """
	if session["achievement order"] == "ascending":
		if session["achievement filter"] == "non":
			data = models.Achievement.query.order_by(models.Achievement.name.asc()).all()
		elif session["achievement filter"] == "Linked to Hero":
			data = models.Achievement.query.order_by(models.Achievement.name.asc()).filter(Achievement.hero_id != None).all()
		else:
			data = models.Achievement.query.order_by(models.Achievement.name.asc()).filter(Achievement.hero_id == None).all()
	else:
		if session["achievement filter"] == "non":
			data = models.Achievement.query.order_by(models.Achievement.name.desc()).all()
		elif session["achievement filter"] == "Linked to Hero":
			data = models.Achievement.query.order_by(models.Achievement.name.desc()).filter(Achievement.hero_id != None).all()
		else:
			data = models.Achievement.query.order_by(models.Achievement.name.desc()).filter(Achievement.hero_id == None).all()
	
	if not data:
		return render_template('404.html', thing='Rewards')
	output = data[12 * (session["achievement page"] - 1): 12 * session["achievement page"]]

	return render_template('achievements.html', data=data, output=output, page = session["achievement page"], order = session["achievement order"], filter = session["achievement filter"])

@views.route('/api/achievements/<int:achievement_id>', methods=['GET'])
def achievement(achievement_id):
	""" Returns Page for a single Achievement """
	data = models.Achievement.query.get(achievement_id)
	if not data:
		return render_template('404.html', thing='Reward')
	
	return render_template('achievements_instance.html', data=data)



@views.route('/about/')
def about():
	""" Returns About Page """
	return render_template('about.html')


# Usage example: "http://127.0.0.1:5000/api/search?search_string=her&page=1"
@views.route('/api/search', methods=['GET'])
def search(search_string="", page=1):
	if request.form.get('search_string') is not None :
		search_string = request.form.get('search_string') 
	else:
		search_string = request.args.get('search_string')
	print(search_string)
	# Disabling because of switch to client-side pagination
	# if request.form.get('page') is not None :
	#	 page = request.form.get('page')
	# else :
	#	 page = int(request.args.get('page'))
	page = 1
	if not search_string :
		return render_template('search.html', data=[[], []])

	# Find the AND search matches in the tables
	like_search_string = "%" + search_string + "%"
	data = [[], []]
	data[0] += models.Achievement.query.filter(or_(Achievement.name.like(like_search_string),
											   Achievement.description.like(like_search_string))).all()
	data[0] += models.Reward.query.filter(or_(Reward.name.like(like_search_string),
										   Reward.quality.like(like_search_string))).all()
	data[0] += models.Player.query.filter(or_(Player.name.like(like_search_string),
										   Player.server.like(like_search_string),
										   Player.level.like(like_search_string),
										   Player.server.like(like_search_string))).all()
	data[0] += models.Hero.query.filter(or_(Hero.name.like(like_search_string),
										 Hero.age.like(like_search_string),
										 Hero.description.like(like_search_string),
										 Hero.affiliation.like(like_search_string))).all()

	# Find the OR search matches in the tables
	for word in search_string.split():
		word = "%" + word + "%"
		data[1] += models.Achievement.query.filter(or_(Achievement.name.like(word),
												   Achievement.description.like(word))).all()
		data[1] += models.Reward.query.filter(or_(Reward.name.like(word),
											   Reward.quality.like(word))).all()
		data[1] += models.Player.query.filter(or_(Player.name.like(word),
											   Player.server.like(word),
											   Player.level.like(word),
											   Player.server.like(word))).all()
		data[1] += models.Hero.query.filter(or_(Hero.name.like(word),
											 Hero.age.like(word),
											 Hero.description.like(word),
											 Hero.affiliation.like(word))).all()

	# Get the data into usable dicts
	data = [[d.serialize() for d in data[0]], [d.serialize() for d in data[1]]]

	search_results = [[], []]
	# Search through the results for the context of search terms as well as format the search results into usable values
	for result in data[0]:
		context = []
		for value in [getContext(val, search_string) for val in result.values()]:
			if (value != []):
				context += value
		search_results[0].append({"name": result["name"], "search_url": result["search_url"], "matches": context})
	for result in data[1]:
		context = []
		for word in search_string.split():
			for value in [getContext(val, word) for val in result.values()]:
				if (value != []):
					context += value
		search_results[1].append({"name": result["name"], "search_url": result["search_url"], "matches": context})

	# Get the results for the specified page
	# search_results = [search_results[0][10 * (page - 1):10 * page], search_results[1][10 * (page - 1):10 * page]]
	return render_template('search.html', data=search_results)

# Method to find context in the values of the table entries
def getContext(val, search):
	context_amount = 5
	results = []
	if (type(val) is int):
		try:
			if (val == int(search)):
				return [val]
		except Exception:
			return results
	if (type(val) is unicode or type(val) is str):
		index = val.find(search)
		while (index != -1):
			front = index
			back = index
			frontCount = context_amount + 1
			backCount = context_amount + 1
			while (frontCount > 0 or backCount > 0):
				if (front > 0 and frontCount > 0):
					front -= 1
				if (back < len(val) and backCount > 0):
					back += 1
				if (val[front] == ' ' or front == 0):
					frontCount -= 1
				if (back == len(val) or val[back] == ' '):
					backCount -= 1
			results.append(val[front:back].encode('utf-8'))
			frontCount = context_amount + 1
			backCount = context_amount + 1
			val = val[back::]
			index = val.find(search)
	return results

#Signup, Login, Logout ---------

@views.route("/signup", methods=["GET", "POST"])
def signup():
	if 'email' in session:
		return redirect(url_for('views.index'))

	form = SignupForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
		return redirect(url_for('views.index'))

	elif request.method == "GET":
		return render_template('signup.html', form=form)


@views.route("/login", methods=["GET","POST"])
def login():
	if 'email' in session:
		return redirect(url_for('views.index'))

	form = LoginForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

		user = models.User.query.filter_by(email=email).first()
		if user is not None and user.check_password(password):
			session['email'] = form.email.data
			return redirect(url_for('views.contentManager'))
		else:
			return redirect(url_for('views.login'))

	elif request.method == "GET":
		return render_template('login.html', form=form)


@views.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('views.index'))




#Content Manager Tools --------

adminUser = "admin@overwatchdb.me"; # pass is admin123

@views.route('/api/contentManager', methods=["GET"])
def contentManager():
	if 'email' not in session:
		return redirect(url_for('views.login'))

	user = str(session['email'])
	data = [[], [], [], []]
	data[0] = models.Achievement.query.filter(Achievement.creator == user).all()
	data[1] = models.Reward.query.filter(Reward.creator == user).all()
	data[2] = models.Player.query.filter(Player.creator == user).all()
	data[3] = models.Hero.query.filter(Hero.creator == user).all()

	return render_template('contentManager.html', data=data, user=user) 
		#output=output)

	


#Create Hero -----
@views.route("/createHero", methods=["GET", "POST"])
def createHero():
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))

	form = HeroForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('createHero.html', form=form)
		else:
			hero = models.Hero(form.name.data, form.description.data, form.affiliation.data, form.age.data, form.url.data, session['email'])
			db.session.add(hero)
			db.session.commit()
			return redirect(url_for('views.contentManager'))

	elif request.method == "GET":
		return render_template('createHero.html', form=form)

@views.route("/createPlayer", methods=["GET", "POST"])
def createPlayer():
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))

	form = PlayerForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('createPlayer.html', form=form)
		else:
			player = Player(form.name.data, form.server.data, form.level.data, form.url.data, session['email'])
			db.session.add(player)
			db.session.commit()
			return redirect(url_for('views.contentManager'))

	elif request.method == "GET":
		return render_template('createPlayer.html', form=form)


@views.route("/createAchievement", methods=["GET", "POST"])
def createAchievement():
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))

	form = AchievementForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('createAchievement.html', form=form)
		else:
			achievement = Achievement(form.name.data, form.description.data, form.type.data, form.url.data, session['email'])
			db.session.add(achievement)
			db.session.commit()
			return redirect(url_for('views.contentManager'))

	elif request.method == "GET":
		return render_template('createAchievement.html', form=form)
		
@views.route("/btn/delete", methods=["GET", "POST"])
def delete_btn():
	if 'email' not in session:
		return redirect(url_for('views.login'))
	id = request.args.get('id')
	type = request.args.get('type')
	user = str(session['email']);
	if (type == "achievement"):
		models.Achievement.query.filter_by(and_(Achievement.creator == user, Achievement.id == id)).delete()
	if (type == "hero"):
		models.Hero.query.filter_by(and_(Hero.creator == user, Hero.id == id)).delete()
	if (type == "player"):
		models.Player.query.filter_by(and_(Player.creator == user, Player.id == id)).delete()
	if (type == "reward"):
		models.Reward.query.filter_by(and_(Reward.creator == user, Reward.id == id)).delete()
	db.session.commit()
	return redirect(url_for('views.contentManager'))	
	

@views.route("/delete", methods=["GET", "POST"])
def delete():
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))
	
	form = DeleteForm()

	if form.validate() == False:
		data = [[], [], [], []]
		data[0] = models.Achievement.query.filter(Achievement.creator == session['email']).all()
		data[1] = models.Reward.query.filter(Reward.creator == session['email']).all()
		data[2] = models.Player.query.filter(Player.creator == session['email']).all()
		data[3] = models.Hero.query.filter(Hero.creator == session['email']).all()
		return render_template('delete.html', form=form, data=data)
	if str(form.model.data).lower() == "hero":
		models.Hero.query.filter(and_(Hero.name == form.name.data, Hero.creator == session['email'])).delete()
	elif str(form.model.data).lower() == "achievement":
		models.Achievement.query.filter(and_(Achievement.name == form.name.data, Achievement.creator == session['email'])).delete()
	elif str(form.model.data).lower() == "reward":
		models.Reward.query.filter(and_(Reward.name == form.name.data, Reward.creator == session['email'])).delete()
	elif str(form.model.data).lower() == "player":
		models.Player.query.filter(and_(Player.name == form.name.data, Player.creator == session['email'])).delete()

	db.session.commit()
	return redirect(url_for('views.contentManager'))	


@views.route("/createReward", methods=["GET", "POST"])
def createReward():
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))

	form = RewardForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template('createReward.html', form=form)
		else:
			reward = Reward(form.name.data, form.quality.data, form.cost.data, form.url.data, session['email'])
			db.session.add(reward)
			db.session.commit()
			return redirect(url_for('views.contentManager'))

	elif request.method == "GET":
		return render_template('createReward.html', form=form)

@views.route("/editHero/<int:hero_id>", methods=["GET", "POST"])
def editHero(hero_id = 0 ):
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))
	form = HeroForm()
	if form.validate() == False:
		if hero_id == 0:
			heroes = models.Hero.query.filter(Hero.creator == session['email']).all()
			return render_template('editHero.html', heroes=heroes, show_form =0, show_heroes =1, show_hero = 0)
		else: 
			hero = models.Hero.query.filter(and_(Hero.id == hero_id, Hero.creator == session['email'])).all()
			return render_template('editHero.html', hero=hero, form =form, show_form =1, show_heroes =0, show_hero = 1 )
	else:
		models.Hero.query.filter(and_(Hero.id == hero_id, Hero.creator == session['email'])).delete()
		hero = models.Hero(form.name.data, form.description.data, form.affiliation.data, form.age.data, form.url.data, session['email'])
		db.session.add(hero)
		db.session.commit()
		return redirect(url_for('views.contentManager'))

@views.route("/editAchievement/<int:achievement_id>", methods=["GET", "POST"])
def editAchievement(achievement_id = 0 ):
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))
	form = AchievementForm()
	if form.validate() == False:
		if achievement_id == 0:
			achievements = models.Achievement.query.filter(Achievement.creator == session['email']).all()
			return render_template('editAchievement.html', achievements=achievements, show_form =0, show_achievements =1, show_achievement = 0)
		else: 
			achievement = models.Achievement.query.filter(and_(Achievement.id == achievement_id, Achievement.creator == session['email'])).all()
			return render_template('editAchievement.html', achievement=achievement, form =form, show_form =1, show_achievements =0, show_achievement = 1 )
	else:
		models.Achievement.query.filter(and_(Achievement.id == achievement_id, Achievement.creator == session['email'])).delete()
		achievement = Achievement(form.name.data, form.description.data, form.type.data, form.url.data, session['email'])
		db.session.add(achievement)
		db.session.commit()
		return redirect(url_for('views.contentManager'))

@views.route("/editReward/<int:reward_id>", methods=["GET", "POST"])
def editReward(reward_id = 0 ):
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))
	form = RewardForm()
	if form.validate() == False:
		if reward_id == 0:
			rewards = models.Reward.query.filter(Reward.creator == session['email']).all()
			return render_template('editReward.html', rewards=rewards, show_form =0, show_rewards =1, show_reward = 0)
		else: 
			reward = models.Reward.query.filter(and_(Reward.id == reward_id, Reward.creator == session['email'])).all()
			return render_template('editReward.html', reward=reward, form =form, show_form =1, show_rewards =0, show_reward = 1 )
	else:
		models.Reward.query.filter(and_(Reward.id == reward_id, Reward.creator == session['email'])).delete()
		reward = Reward(form.name.data, form.quality.data, form.cost.data, form.url.data, session['email'])
		db.session.add(reward)
		db.session.commit()
		return redirect(url_for('views.contentManager'))

@views.route("/editPlayer/<int:player_id>", methods=["GET", "POST"])
def editPlayer(player_id = 0 ):
	#control access to this page
	if 'email' not in session:
		return redirect(url_for('views.login'))
	form = PlayerForm()
	if form.validate() == False:
		if player_id == 0:
			players = models.Player.query.filter(Player.creator == session['email']).all()
			return render_template('editPlayer.html', players=players, show_form =0, show_players =1, show_player = 0)
		else: 
			player = models.Player.query.filter(and_(Player.id == player_id, Player.creator == session['email'])).all()
			return render_template('editPlayer.html', player=player, form =form, show_form =1, show_players =0, show_player = 1 )
	else:
		models.Player.query.filter(and_(Player.id == player_id, Player.creator == session['email'])).delete()
		player = Player(form.name.data, form.server.data, form.level.data, form.url.data, session['email'])
		db.session.add(player)
		db.session.commit()
		return redirect(url_for('views.contentManager'))


