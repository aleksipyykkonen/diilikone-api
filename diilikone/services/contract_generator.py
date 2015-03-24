from flask_weasyprint import HTML
from flask import render_template

from diilikone.models import Provision


def make_contract(deal):

    #salesperson name
    salesperson = deal.salesperson

    #amount of magazines
    amount_of_magazines = deal.size

    #provision
    provision = Provision.query.filter_by(quantity=deal.size).first()

    #create full name
    full_name = '%s %s' % (salesperson.first_name, salesperson.last_name)

    html = render_template('contract.html', name=full_name, size = amount_of_magazines)
    pdf = HTML(string=html).write_pdf()
    return pdf

