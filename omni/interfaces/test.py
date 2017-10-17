from omni.interfaces.registration import register

def test():

    register(entry_point='omni.interfaces.markets.gemini:get_symbols')