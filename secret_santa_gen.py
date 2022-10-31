#!/usr/bin/env python3

import sys, json, logging
import numpy as np
import numpy.random as nrandom
from getpass import getpass

def send_mail(dest_name, to_gift, sender_address, sender_pw, inputs):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText


    mail_content = """Hi there!
    Get a gift for %s. Budget is %s.

Regards,
Your Friendly Neighborhood Secret Santa generator""" % (to_gift, str(inputs['budget']))

    # sets the email address the email will be sent to
    receiver_address = inputs['partecipants'][dest_name]

    # sets up the MIME
    message = MIMEMultipart()
    message['From'] = sender_address # your email address
    message['To'] = receiver_address # Secret Santa's email address
    message['Subject'] = 'Secret Santa' # subject of the

    # sets the body of the mail
    message.attach(MIMEText(mail_content, 'plain'))

    # creates the SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.connect("smtp.gmail.com", 587)
    session.ehlo()
    session.starttls()
    session.login(sender_address, sender_pw)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

if __name__ == "__main__":
    """Generate Secret Santa giver-receiver pairs from a list.

    Send the results via mail (provided in the input file).
    You need to have a gmail account with 2-Step verification that you can access from third-party app (see App passwords).

    Debug flag ON: show you the extraction process.
    Reveal flag ON: show the results.
    TODO: exclusion lists.
    """

    debug = False
    reveal = False # show the combinations
    #-------- SET UP LOGGER -------------
    c_log = logging.getLogger()
    c_log.setLevel(logging.INFO)
    if debug: c_log.setLevel(logging.DEBUG)
    log_format = logging.Formatter('[%(levelname)5s - %(funcName)10s] %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    c_log.addHandler(ch)

    #-------- READ INPUTS -------------
    in_fname = sys.argv[1]
    with open(in_fname) as inj:
        inputs = json.load(inj)

    if 'budget' not in inputs.keys(): inputs['budget'] = 'none'
    #-------- EXTRACT RELEVANT -------------
    # get parteciants from key of name: mail dictionary
    partecipants = np.array(list(inputs['partecipants'].keys())) # I know, cumbersome conversion
    N_range = np.arange(len(partecipants), dtype=int) # map partecipants to integers

    c_log.info("%15s" % "partecipants:\n"+"\n".join(["%20s (%30s)" % (p, inputs['partecipants'][p])
                                                     for p in partecipants]))

    #-------- EXTRACTION -------------
    check_shuffle = [True]
    i = 0
    # shuffle until there are no self-loop
    # !! This might become very slow if the size of the group is too large !!
    while len(check_shuffle):
        c_log.debug("%15s" % "partecipants:"+"".join(["%20i " % p for p in N_range]))
        Nshuffle = N_range.copy()
        nrandom.shuffle(Nshuffle)
        c_log.debug("%15s" % "shuffle:"+"".join(["%20i " % p for p in Nshuffle]))
        check_shuffle = np.where(Nshuffle == N_range)[0]
        c_log.debug(check_shuffle)
        i += 1
    c_log.info('Consistent solution after %i tries' % i)

    # Print results
    if reveal:
        print('These are the results:')
        for receiver, giver in zip(partecipants[N_range], partecipants[Nshuffle]):
            print("%15s (%30s) gifts %-15s (%-20s)" % (giver, inputs['partecipants'][giver],
                                                  receiver, inputs['partecipants'][receiver],))

    # Log into sender email
    sender_address = input('Email from:')
    if '@' not in sender_address: raise ValueError('not a valid email address (%s)' % sender_address)
    c_log.info('Mail domain %s' % sender_address.split('@')[1])
    sender_pw = getpass('Email pw:')
    #print(sender_pw)

    for receiver, giver in zip(partecipants[N_range], partecipants[Nshuffle]):
        c_log.info("Email from %s to %s (%s)" % (sender_address, giver, inputs['partecipants'][giver]))
        send_mail(giver, receiver, sender_address, sender_pw, inputs)
