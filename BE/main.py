import falcon
from APIHandlers import SpeedTestDataAPIHandler


api = falcon.API()
api.add_route('/speedtest', SpeedTestDataAPIHandler())

