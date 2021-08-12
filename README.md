# Fast_Blocksci
Fast API app to query mtg stuff





### Adminer
We use [`Adminer`](https://www.adminer.org) as our database admin server. 
It's useful for debugging issues during production and development.
Just run `docker-compose` to start the server in the background.

```
docker-compose up -d --build
```

> The "--build" command forces the "adminer/Dockerfile" to rebuild.

Now you can go to [http://localhost:8080](http://localhost:8080) and enter the following settings:

System: `SQLite 3`  
Username: `` (leave empty)
Password: `<PASSWORD>` (Grab the `Adminer Password` from 1password)  
Database: `/db/app.db` (we mount the "db" folder to `/app`)
