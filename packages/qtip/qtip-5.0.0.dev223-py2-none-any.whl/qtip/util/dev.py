##############################################################################
# Copyright (c) 2017 ZTE Corporation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from qtip.base.error import ToBeDoneError


def create_to_be_done(method, module='qtip'):
    def tbd():
        raise ToBeDoneError(method, module)
    return tbd
