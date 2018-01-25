from .etherscan_core import service
from omni.core import interface

@interface
def get_chart(input):
    return service.invoke("GET", endpoint='chart/' + str(input.chart))

