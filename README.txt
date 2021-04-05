# esd_BattleFrontier

ESD_BATTLEFRONTIER/BF_backend_ms/docker-compose.yml is used for creating and starting the containers. The message broker RabbitMQ will also be started with Compose. Therefore, make sure that you don't have another RabbitMQ container running by checking docker ps -a and stop and remove any RabbitMQ container.

To run the application, here's what you need to do :>

1) Build rabbitmq-mgmt image. We are using the same image as Lab 6, but if you don't have a rabbitmq-mgmt image when running docker images, open CMD window and run:
    docker run -d --hostname esd-rabbit --name rabbitmq-mgmt -p 5672:5672 -p 15672:15672 rabbitmq:3-management
