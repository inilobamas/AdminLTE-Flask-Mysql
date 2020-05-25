from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main
from .forms import SearchForm

logger = get_logger(__name__)
cfg = get_config()

# General List Query
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # Delete Operation
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('Successfully Deleted', 'success')
        except:
            flash('Failed to Delete', 'danger')

    # Query List
    query = DynamicModel.select()
    total_count = query.count()

    # Processing Pagination
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# General Single Model Query & Add & Modify
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # Inquire
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # Modify
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('Successfully Modified', 'success')
            else:
                utils.flash_errors(form)
    else:
        # Add
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('Save Successfully', 'success')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


# Root Dir
@main.route('/', methods=['GET'])
@login_required
def root():
    return redirect(url_for('main.index'))


# Home
@main.route('/index', methods=['GET'])
@login_required
def index():
    form = SearchForm()
    return render_template('index.html', current_user=current_user, form=form)


# Notification Query Method
@main.route('/notifylist', methods=['GET', 'POST'])
@login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')


# Notification Method Configuration
@main.route('/notifyedit', methods=['GET', 'POST'])
@login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')
