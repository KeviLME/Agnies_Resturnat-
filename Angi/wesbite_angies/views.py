from flask import Blueprint,render_template,request,url_for, current_app, redirect, flash
import json
from collections import defaultdict
import stripe





views = Blueprint("views", __name__)





@views.route("/")
def home():
    return render_template("home.html")


items = [] #this is a list of dictionaries
Total = 0





@views.route("/Menu",methods=["GET","POST"])
def Menu():
    if request.method == "POST":#need to capture the form here and pritn the datat 
        Pizza_Info = json.loads(request.form.get("Pizza_Info"))
        global items

        global Total


        item = {"size":Pizza_Info["size"],"type":Pizza_Info["type"],"Cash":Pizza_Info["Cash"], "price_id":Pizza_Info["price_id"]} 

        for existing_item in items:
            if existing_item["size"] == item["size"] and existing_item["type"] == item["type"]:
                existing_item["quantity"] += 1
                Total+= existing_item["Cash"]
                break
        else:
            item["quantity"] = 1  # Initialize quantity for new items
            items.append(item)
            Total += item["Cash"]

        print(items)

        #print(f"Selected pizza size: {item['size']}  Selected pizza type: {item['type']} Pizza worth: {item['Cash']}")

        return render_template("Menu.html")


        
    return render_template("Menu.html")



@views.route("/Order",methods=["GET","POST"])
def Order():

    stripe_public_key = current_app.config["STRIPE_PUBLIC_KEY"]
    stripe_secret_key = current_app.config["STRIPE_SECRET_KEY"]

    stripe.api_key = stripe_secret_key

    global items
    global Total
    
    try:
        line_items = [
            {
                'price': item["price_id"],  # Replace with the actual price ID
                'quantity': item["quantity"],
            }
            for item in items
        ]
    except (KeyError, TypeError) as e:
        # Handle the exception (e.g., log the error)
        print(f"Error constructing line_items: {str(e)}")
        line_items = []
    
    if not line_items:
        flash('Your cart is empty. Please add items to your cart before proceeding.', 'error')
        return redirect(url_for("views.Menu"))


    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=url_for('views.Thank_You', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('views.Order', _external=True),
    )

    

     



    return render_template("order.html", items=items, Total=Total, checkout_session_id=session["id"], check_out_public_key=stripe_public_key)







        






@views.route("/Thank_You",methods=["GET","POST"])
def Thank_You():
    return render_template("ThankYou.html")
     






