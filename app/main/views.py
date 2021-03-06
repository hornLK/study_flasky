from datetime import datetime
from flask import (render_template,session,
                   redirect,url_for,flash,request,
                   current_app
                  )
from . import main
from .. import db
from .forms import NameForm,EditProfileForm,EditProfileAdminForm, PostForm
from ..models import User,Permission, Post
from flask_login import login_required,current_user
from ..decorators import admin_required,permission_required

@main.route('/admin/')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator/')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

@main.route('/',methods=['GET','POST'])
def index():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['BOLOG_POSTS_PAGE'],
        error_out=False)
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
       form.validate_on_submit():
        post = Post(body=form.body.data,
                   author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))
    posts = pagination.items
    return render_template('index.html',
                           form=form,
                           posts=posts,
                          pagination=pagination)

@main.route('/user/<username>/')
def user(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user)

@main.route('/edit-profile/',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been update')
        return redirect(url_for('main.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)


@main.route("/edit-profile/<int:id>/",methods=["GET","POST"])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me =form.about_me.data
        db.session.add(user)
        flash("The profile has been updated")
        return redirect(url_for("main.user",
                               username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    return render_template('edit_profile.html',
                          form=form,user=user)

#@mail.route('/post/<int:id>')
#def post(id):
#    post = Post.query.get_or_404(id)
#    return render_template('post.html',posts=[post])
