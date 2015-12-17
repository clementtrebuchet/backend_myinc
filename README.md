##bottle Authentication and Authorisation
    As you certainly know default bottle framework doesn't enable authentication or authorisation,
    except basic authentication which is not really sexy therefor this not works with MongoDB 
    For this reason we use cork-bottle plugin which allow us to implement simple authentication and authorisation on top of MongoDB
    The process is :
    Registration account is pending (users.pending_registrations)
    Send an email with a link for account verification
    Link is clicked account is verified users.users
    
###Activate your bottle application within your google account:
    In order for the bottle-cork auth plugin to use gmail as your SMTP provider/server for sending mail for account registration
    just activate the fact that application with poor authentication are able to act as you
      - smtp_url = "starttls://gmail_username:gmail_password@smtp.gmail.com:587"
    
    More information:
    Gmail Account > Settings > Accounts > Other Google Account settings > Security > Connected applications and sites > Review permissions
<pre>
Activate for your application be able to work:
<a href="https://www.google.com/settings/security/lesssecureapps">lesssecureapps</a>
</pre>
###MongoDB users collections
<pre>
use users
switched to db users
> db.roles.find()
{ "_id" : ObjectId("5669dc65f99ba42f7e1593c1"), "role" : "administrator", "val" : 100 }
{ "_id" : ObjectId("5669dc65f99ba42f7e1593c2"), "role" : "user", "val" : 50 }
> db.users.find()
{ "_id" : ObjectId("5669dd063ea2476e1c2356f8"), "creation_date" : "2015-12-10 20:11:17.513216", "desc" : null, "email_addr" : "clement.trebuchet@gmail.com", "hash" : "cFq0bxqxdktiawPpJyTkRWacWa/ajwhAHMOoqj4B1TXdVJdq32hu6JCA7BYb4iy/pUz/wnePR+aTuBQ2+nZKp+w=", "last_login" : "2015-12-10 20:13:58.430395", "login" : "messagebot", "role" : "user" }
> db.pending_registrations.find()
{ "_id" : ObjectId("5669f0013ea2476e1c2356f9"), "creation_date" : "2015-12-10 21:34:57.627674", "desc" : null, "email_addr" : "clement.trebuchet@gmail.com", "hash" : "cBJJ8+8Ipa/4eKyGvnimvuc8n2Y7DIVUQdpXKLos+gSHSWP7OqnxnQ6V8wDJ0xK6Fl5zE/F1F3FjfcObO9qVJkQ=", "pending_registration" : "11726d9173414e7998d1660d3c75a8c0", "role" : "user", "username" : "test" }

</pre>
###Original Confirmation mail

    Note the "pending_registration" : "11726d9173414e7998d1660d3c75a8c0" value in db.pending_registrations is the id of the link of the mail
    once clicked user become active and can successfully login

<pre>                                                                                                                                                                                                                                                         
Return-Path: <clement.trebuchet@gmail.com>
Received: from clemopower.teamat4cs ([2a01:e34:ef0e:68e0:3a59:f9ff:fec7:fc78])
        by smtp.gmail.com with ESMTPSA id jm4sm14112599wjb.7.2015.12.10.13.34.58
        for <clement.trebuchet@gmail.com>
        (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);
        Thu, 10 Dec 2015 13:34:58 -0800 (PST)
Message-ID: <5669f002.4473c20a.24eaf.ffffd299@mx.google.com>
Date: Thu, 10 Dec 2015 13:34:58 -0800 (PST)
Content-Type: multipart/alternative; boundary="===============0835155550=="
MIME-Version: 1.0
Subject: Signup confirmation
From: clement.trebuchet@gmail.com
To: clement.trebuchet@gmail.com

--===============0835155550==
Content-Type: text/html; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit


Hi test! Click <a href="http://localhost:10080/validate_registration/11726d9173414e7998d1660d3c75a8c0">HERE</a> to finish your registration</p>
or go to http://localhost:10080/validate_registration/11726d9173414e7998d1660d3c75a8c0</p>

--===============0835155550==--
</pre>
    # backend_myinc
