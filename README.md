# Luizalabs Challenge

This applications was developed for an challenge from the Magalu/Luizalabs. Here, the objective was to create an API to manager the customers and their favorite products.

So,  it works like a simple CRUD, you can insert new costumers only providing email and name, remember the email is unique, but to delete, update and show an costumer you need pass his/her customer_id. All the customer have one list of favorite products, it can be empty or can have some products that can't repeat, with that API you can insert, remove and see a customer's favorite items.

### How can I run it?

You can run it using two approaches! 

The easiest and simple is with docker-compose, you only need to have that installed.

In the directory of the project simple run:

```shell
docker-compose up
```

and access http://0.0.0.0:8000/ and you will enter in the documentation of the project.

The second approach is with Python 3.7.6 and MongoDB, you will need this two to continue. 

Be sure that your MongoDB is running, and export this variables:

```shell
export API_USER=admin
export API_PASS=admin
export MONGO_HOST=localhost
export MONGO_PORT=27017
```

(remember, this is the default configurations)

After that you need to install the package running

```
python setup.py install
```

And finally you can run using this command: 

```shell
gunicorn -w 4 -b 0.0.0.0:8000 luizalabs_project:app
```

and access using the same link that you http://0.0.0.0:8000/

That's it! Much more easy with docker-compose, right?

### Don't forget the login and password!

To use the API you need the authorization, without that, you will do nothing.

This API use a basicAuth and if you followed all the steps from this tutorial the credentials are the default:

username: **admin**

password: **admin**

In the Swagger (the documentation site) look for the button "Authorize" in the top left corner, put that credentials and you will be testing the API.

### Want to test the project?

Yeah! You can use the unity test to do so.

first, install pytest with:

```shell
pip install pytest
```

and so run:

```
pytest
```

if everything went weel, you are ready to use the application!

### Are the project complete?

So, in the real world it's need to put some improvements like some metrics to see it's performance. I like tools like Prometheus & Grafana and expose in the application a endpoint "/metrics" with some helpful informations of the API. Another solutions is to create your own application to monitor the performance, I really recommend Dash if you are a Python Lover!

### Contacts

Please, if you find some bugs or issues feel free to contact me in one of that channels:

- email: gabrielmvnogueira@gmail.com

- linkedin: https://www.linkedin.com/in/gabrielmvnogueira/

  

### Thank you! :)