

1. To spin up all containers, after opening up docker's GUI app, run in terminal

```{bash}
    cd ./dockersetup
    docker compose up --build
```

2. To go into a docker container either run the following in terminal, or go to the docker gui, click on the running container, and click on the terminal icon to open it up. 

```{bash}
    docker exec -it container_name bash
```

3. To list currently running docker containers, 

```{bash}
    docker ps -a
```

Remove the -a flag to see all containers. 

4. You can remove the docker containers with `docker compose down` or delete a specific container using the container id by running `docker rm container_id`.



5. Mysql
mysql -uroot -pdb