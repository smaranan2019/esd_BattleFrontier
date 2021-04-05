# esd_BattleFrontier

ESD_BATTLEFRONTIER/BF_backend_ms/docker-compose.yml is used for creating and starting the containers. The message broker RabbitMQ will also be started with Compose. Therefore, make sure that you don't have another RabbitMQ container running by checking docker ps -a and stop and remove any RabbitMQ container.

To run the application, here's what you need to do :>

1) Start WAMP and go to phpMyAdmin. Import all the sql files in /sql folder. These includes:
    - AccountDB.sql
    - CardDB.sql
    - OrderDB.sql
    - PaymentDB.sql
    - ShippingDB.sql

2) Open /BF_backend_ms and see the docker-compose.yml file. Run
    docker-compose build
3) Make sure that WAMP/MAMP is running
4) Go to localhost phpmyadmin and create an sql user called is213
5) Run
    docker-compose up -d
5) Run
    docker image ls 
    to make sure that all the images are created
5) Copy the file BF_frontend to C:\wamp64\www\ and open it in a browser by accessing http://localhost/BF_frontend/templates/login.html 
6) Use cases:
    1) As Seller:
        a) Sign up
            Go to http://localhost/BF_frontend/templates/signup.html and key in:
                Username: Ash Ketchum
                Telehandle: (Your telehandle)
                Paypal Email: gotta_ketchum_all@personal.example.com
                Password: Anything can
            Once succeeded, proceed to login
        b) Add cards as Seller
        c) Receive notification for new shipping and Approve/ Reject Shipping
        d) See all new, in transit and complete Shipping
    2) As Buyer:
        a) Sign up
            Go to http://localhost/BF_frontend/templates/signup.html and key in:
                Username: Ash Ketchum
                Telehandle: (Your telehandle)
                Paypal Email: gotta_ketchum_all@personal.example.com
                Password: Anything can
            Once succeeded, click _____ and log in
        b) View all available cards
        c) Select cards and make payment
        d) Receive notification for shipped order and Confirm received order
        e) See all Completed Shipping and Refunded order
    3) As Business:
        a) Release payment to Seller for completed order
        b) Refund payment to Buyer with failed orders 

