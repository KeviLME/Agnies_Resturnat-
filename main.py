from wesbite import create_app
import stripe
from flask import Flask, render_template, request, url_for, redirect, session

import json


app = create_app()

app.config["STRIPE_PUBLIC_KEY"] = 'pk_test_51NnXW1JT2HBC5ySEagq9GCHh3V6V8YJPAyw7RhpxYNsoC2jhevASWQ3MzMGDD21J9crxaZbQs1AtP21KdFtn5r1R00tnT2BuoQ'
app.config["STRIPE_SECRET_KEY"] = 'sk_test_51NnXW1JT2HBC5ySE0rMExL7wYFwRz0a7Ttt20h9s8XZogV8jtvZSCwhRaJzxxUoEhD5FgDpUwYHw9TThDqdtkagw00fQZY8cx5'


stripe.api_key = app.config['STRIPE_SECRET_KEY']



if __name__ == "__main__":
    app.run(debug=True) 