
# speedtestLogger
SpeedtestLogger is a self-explanatory name. It is a Python script that uses:
- [sivel](https://github.com/sivel)'s **[speedtest-cli](https://github.com/sivel/speedtest-cli)** for internet speed testing;
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy) to store data in the database;
- sqlite3 as database engine.

## TODOs:
- A small front-end system to consult and filter the results;
- Incremental tweaks such as:
	- Console parameter parsing to let the script be more or less verbose;
	- SpeedTesting on demand (API calls).
	
## But @mmeruje, why did you do this?
Well... in my hometown, Fibre connection is still not available to public and the ADSL connection there was always (and it still is) dropping from ~12Mbps to ~4Mbps. When I called to the ISP Tech Support, they told me that what is happening is a precaution standard procedure when the copper lines have some problem (when they are saturated?).

Now... I am a frequent frequent video-call user to devices within that network connection and when the connection dropps to 4Mbps, the video-call quality is really poor. The fastest solution to bring back the 12Mbps, at the moment, is to restart the router or if that does not work... to call the ISP Tech Support.

Since I am not at my hometown at the moment, I created this script to run from time to time and update a small database. Then, by remotely checking the database, I will be able to know when the router needs to be restarted or when to call again to the ISP support lines.

If there were any other options? Yes, I could simply schedule remote router restart everyday. But I thought this would be something fun to do. 👨‍🚀

##### If you have any suggestion or correction, do not hesitate and contact me. :) 