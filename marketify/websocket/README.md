# Websocket API Monitor

This is the component of the market monitor that establishes a websocket
 connection with several data exchanges. All tasks run asynchronously
 on a single thread.

## Flow

Execution order is as follows:

~~~
1. Establish a websocket connection with the exchange
2. Send an initial priming message (request message)
3. Await incoming messages and parse them as they arrive
4. Update cache time for socket activity (health monitor checks this)
5. Write valid market values to cache and db (debounced with rxpy)
~~~
## Adding Exchanges

### Websokcet API Poller
To add an exchange API to poll you must do the following:
~~~
1. Add the exchange name to the config file
2. Add the socket url, currency type, and primer message to the config file
3. In the clients.py file add a new class for the new exchange API
    I. Follow the format of the existing classes. The new class must
       implement the map_response method
~~~
