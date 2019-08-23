# RESTful API Monitor

This is the component of the market monitor that periodically takes
 data from restful APIs exposed by exchanges. All tasks run asynchronously
 on a single thread.

## Flow

Execution order is as follows:

~~~
1. Create an aiohttp session
2. Call HTTP GET on the relevant url
3. Parse the response
4. Update cache time for rest activity (health monitor checks this)
5. Write valid market values to cache and db (debounced with rxpy)
~~~
## Adding Exchanges

### Restful API Poller
To add an exchange API to poll you must do the following:
~~~
1. Add the exchange name to the config file
2. Add the API url to the config file
3. In the clients.py file add a new class for the new exchange API
    I. Follow the format of the existing classes. The new class must
       implement the map_response method
~~~
