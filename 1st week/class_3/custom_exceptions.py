class ToomanyattempsError(Exception):
    pass
raise ToomanyattempsError("Too many login attempts")