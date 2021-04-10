x`1# esd_BattleFrontier

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
4) Go to localhost phpmyadmin and create an sql user called is213 to allow remote access to the database
    a) Open phpMyAdmin and click User accounts
    b) Click Add user account and specify the following:
        User name: (Use text field:) is213
        Host name: (Any host) %
        Password: Change to No Password
    c) Select Data
    d) Click Go
5) Run
    docker-compose up -d
5) Run
    docker image ls 
    to make sure that all the images are created
5) Copy the folder BF_frontend to C:\wamp64\www\ and open it in a browser by accessing http://localhost/BF_frontend/templates/login.html 
6) Use cases: 
    Please follow the following order to test the service. Some pages might need to be reloaded to display properly.
    1) As Buyer:
        a) Sign up
            Go to http://localhost/BF_frontend/templates/signup.html and key in:
                Username: Ash Ketchum
                Telehandle: (Your telehandle)
                    ! Do also add our bot @battle_frontier_bot before proceeding to enter Paypal Email
                Paypal Email: gotta_ketchum_all@personal.example.com
                Password: test_usecase
            Click JOIN THE CLUB!
            Once succeeded, click THIS WAY TRAINER!!! and log in:
                Username: Ash Ketchum
                Password: test_usecase
        b) View all available cards
        c) Select any card
        d) Make payment: Click on paypal button and log in with the following details:
            Email: gotta_ketchum_all@personal.example.com
            Password: BC3se?!g
        d) Supposedly, you would be able to receive a notification on Telegram (which will be done in step ____). 
            For now, click on S.S.Ann on the navbar and Confirm received order. You will be able to see the completed order at the end of the page.
        e) See all Completed Shipping in S.S.Ann and Refunded order in Trainer's Coins (Cover in step ____)

    2) As Seller:
        a) Log in:
            Go to http://localhost/BF_frontend/templates/signup.html and key in:
                Username: Professor Oak
                Password: oakidokie
        b) Add cards as Seller:
            Name of Pokemon: Aron
            Type of Pokemon: Normal
            Link of Pokemon image: https://assets.pokemon.com/assets/cms2/img/cards/web/SM10/SM10_EN_124.png
            Pokemon Description: This is a good Pokemon.
            Price of Card: 45.65
            Paypal Client ID: AYQc_qAbEPG6CkSMMeg5UKH3jMacRzyZgFkas5omdcccW7A4cBe8mjxcj8iIkRogp3jqJamMhw0mS-78
        Once succeeded, you will be redirected to http://localhost/BF_frontend/templates/Uploaded.html
        If you sign in as a Buyer, you will be able to see your added card at the end :)
        c) (Optional) Receive notification for new shipping (We won't cover this part since it will be sent to our group's telegram handle), but you can try 
        by creating a new account with your own telegram handle and upload a card as a Seller and buy it as a Buyer.
        d) Approve/ Reject Shipping
        On the navbar, go to Pokemon Center. You should see 2 order under To Ship.
        Click Didn't Ship for the first order and Shipped for the second order (which should be the order you just made as a Buyer in step 1c). 
        d) See all new, in transit and complete Shipping
        Go to Pokemon Center to view any change in the shipping order.

    3) As Business:
        a) Release payment to Seller for completed order
        Go to http://localhost/BF_frontend/templates/BF_UI.html. Under Successful Transaction, click Pay Seller!
        You will be redirected to http://localhost/BF_frontend/templates/BF_release.html. Click on the Paypal button and key in the following:
            Email: battle_my_frontier@business.example.com
            Password: SW5;#i$R
        Proceed to pay the seller and once succeeded, you will be redirected back to http://localhost/BF_frontend/templates/BF_UI.html.
        From the Seller point of view, you can see the completed order under Completed Wooohooo! in Pokemon Center.
        b) Refund payment to Buyer with failed orders 
        In http://localhost/BF_frontend/templates/BF_UI.html, under Refund seller has rejected, select Refund now. You should be logged into the Paypal main page for Battle Frontier.
        Search for the correct transaction from Ash and refund. Once refunded, go back to http://localhost/BF_frontend/templates/BF_UI.html and confirm the refund by clicking Refund Completed.
        From the Buyer point of view, you can see the refunded payment under Refunded Payment in Trainer's Coins.

