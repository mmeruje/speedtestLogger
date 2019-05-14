# speedtestLogger
SpeedtestLogger is a self-explanatory name. It is a Python script that uses:
- [sivel](https://github.com/sivel)'s **[speedtest-cli](https://github.com/sivel/speedtest-cli)** for internet speed testing;
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) to store data in the database;
- sqlite3 as database engine.
- waitress, as WSGI
- falcon, for creating the API

## Installing and running:
1. ```git clone https://github.com/mmeruje/speedtestLogger.git ```
2. ```pip install waitress speedtest-cli sqlalchemy falcon```
3. ```cd speedtestLogger```

### If you want to run the script by yourself
4. ```./python main.py```

### If you want to have a API to access with http requests
4. ```cd BE```
5. ```waitress-serve --port=4000 main:api```

And your endpoint will be something like:

```http://localhost:4000/speedtest```

Available HTTP requests:
* GET   -> will return the last speedtest result
* POST  -> will tell the server to do a speedtest (does not affect the hour of the next speedtest)
* PATCH -> will activate / de-activate the hourly speedtest check

## TODOs:
- A small front-end system to consult and filter the results;
- Incremental tweaks such as:
	- Console parameter parsing to let the script be more or less verbose;
	- Configuration file (speedtest on boot, check interval, ...)
	- ~~SpeedTesting on demand (API calls).~~ [DONE]

## But @mmeruje, why did you do this?
Well... in my hometown, Fibre connection is still not available to public and the ADSL connection there was always (and it still is) dropping from ~12Mbps to ~4Mbps. When I called to the ISP Tech Support, they told me that what is happening is a precaution standard procedure when the copper lines have some problem (when they are saturated?).

Now... I am a frequent frequent video-call user to devices within that network connection and when the connection drops to 4Mbps, the video-call quality is really poor. The fastest solution to bring back the 12Mbps, at the moment, is to restart the router or if that does not work... to call the ISP Tech Support.

Since I am not at my hometown at the moment, I created this script to run from time to time and update a small database. Then, by remotely checking the database, I will be able to know when the router needs to be restarted or when to call again to the ISP support lines.

If there were any other options? Yes, I could simply schedule remote router restart everyday. But I thought this would be something fun to do. 👨‍🚀

##### If you have any suggestion or correction, do not hesitate and contact me. :)
