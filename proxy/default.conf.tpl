server {
    /**
     * This line of code specifies the port on which the server should listen for incoming connections.
     * The value of ${LISTEN_PORT} will be dynamically replaced with the actual port number during runtime.
     */
    listen ${LISTEN_PORT};

    /**
     * This configuration block specifies the location for serving static files.
     * 
     * The `location /static` directive is used to define the URL path where the static files will be served from.
     * The `alias /vol/static` directive is used to specify the directory path where the static files are located on the server.
     * 
     * For example, if a request is made to "/static/css/style.css", the server will look for the file at "/vol/static/css/style.css".
     */
    location /static {
        alias /vol/static;
    }

    /**
     * This configuration block defines the location "/" in the NGINX server.
     * It specifies that requests to this location should be passed to the uWSGI server
     * running at the specified ${APP_HOST} and ${APP_PORT}.
     * The "include" directive includes the "/etc/nginx/uwsgi_params" file,
     * which contains the necessary parameters for the uWSGI server.
     * The "client_max_body_size" directive sets the maximum size of the client request body to 10MB.
     */
    location / {
        uwsgi_pass           ${APP_HOST}:${APP_PORT};
        include              /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}