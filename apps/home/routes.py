# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps import db
from datetime import datetime
from apps.api_connector.AddressDetailRetriever import AddressDetailRetriever
from unique_names_generator import get_random_name

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(40))
    nickname = db.Column(db.String(40))
    balance = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        # to string function in python
        return f'<Address id: {self.id} + {self.address}>'
    
    
@blueprint.route('/index')
@login_required
def index():
    addresses = Address.query \
        .filter(Address.userid == current_user.id) \
        .order_by(Address.date_created).all()
    return render_template('home/tracking.html', addresses=addresses)
    # return render_template('home/tracking.html', segment='tracking', wallets = [])
    # return render_template('home/index.html', segment='index')

@blueprint.route('/tracking', methods=['POST', 'GET'])
@login_required
def tracking():
    if request.method == 'POST':
        address = request.form['address']
        nickname = request.form['nickname']
        if not nickname: nickname = get_random_name()
        addressDetail = AddressDetailRetriever.retrieve_address_details(address)
        if addressDetail == None:
            return 'There was an issue adding your addresse'
        new_address = Address(address=address, 
                              balance=addressDetail.final_balance, 
                              nickname=nickname,
                              userid=current_user.id)
        try:
            db.session.add(new_address)
            db.session.commit()
            return redirect('/tracking')
        except:
            return 'There was an issue adding your address'
    else:
        print(current_user.id)
        addresses = Address.query \
            .filter(Address.userid == current_user.id) \
            .order_by(Address.date_created).all()
        return render_template('home/tracking.html', addresses=addresses)

@blueprint.route('/transactions/<string:addr>', methods=['POST', 'GET'])
@login_required
def transactions(addr):
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST' and request.args.get('page') == None:
        page = int(request.form['pageToGo'])
    per_page = 50
    addressDetail = AddressDetailRetriever.retrieve_address_details(addr, offset=(page-1)*per_page, limit=per_page)
    if addressDetail == None:
        return 'There was an issue displaying your address'
    presentableTransactions = addressDetail.toPresentableTransactions()
    # print("transactionsssssss")
    # print(len(presentableTransactions.transactions))
    ''' blockchain.com API would time out for transactions with high offset
    https://blockchain.info/rawaddr//12xQ9k5ousS8MqNsMBqHKtjAtCuKezm2Ju?offset=14950&limit=50
    {"error":"server-timeout","message":"Request is taking too long"}
    seems like time increases with offset.
    they might be running some for loops
    '''
    
    return render_template('home/transactions.html', transactions=presentableTransactions, 
                           page = page,
                           total_pages = presentableTransactions.totalTransactions // per_page + 1)


@blueprint.route('/delete/<int:id>')
@login_required
def delete(id):
    address_to_delete = Address.query.get_or_404(id)
    try:
        db.session.delete(address_to_delete)
        db.session.commit()
        return redirect('/tracking')
    except:
        return 'There was a problem deleting that address ${id}'

@blueprint.route('/synchronize/<int:id>')
@login_required
def synchronize(id):
    address_to_synchronize = Address.query.get_or_404(id)
    addressDetail = AddressDetailRetriever.retrieve_address_details(address_to_synchronize.address)
    address_to_synchronize.balance = addressDetail.final_balance
    try:
        db.session.commit()
        return redirect('/tracking')
    except:
        return 'There was a problem synchronizing that wallet ${id}'


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
