from flask_mail import Message

from diilikone.extensions import mail
from diilikone.models import Deal, Provision
from diilikone.services import contract_generator
from diilikone.templates import deal_confirmation

#todo deal as parameter
def send_confirmation_email(deal):
    msg = Message(sender=("Äpy", "diili@apy.fi"))

    email = deal.salesperson.email
    msg.add_recipient(email)

    title = 'Tervetuloa Äpy-myyjäksi!'
    msg.subject = title

    #get provision
    provision = Provision.query.filter_by(quantity=deal.size).first()
    price = provision.price_per_magazine

    ##create proper body for text
    message_body = deal_confirmation.get_message(deal, price)
    msg.body = message_body

    mail.send(msg)
    pass

def send_contract(deal):
    pdf = contract_generator.make_contract(deal)
    msg = Message()

    #TODO set real address, oiva tms
    salesperson = deal.salesperson
    email = salesperson.email

    msg.add_recipient(email)
    msg.attach('%s_sopimus.pdf' % email, 'application/pdf', pdf)

    title = 'Sopimus %s' % email

    body = 'liitteenä soppari, saatesanoja tuskin tarvii'

    msg.subject = title
    msg.body = body

    mail.send(msg)
