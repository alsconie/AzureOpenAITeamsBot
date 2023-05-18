#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 8000
    APP_ID = os.environ.get("MicrosoftAppId", "{ENTER APP ID}")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "{ENTER APP PASSWORD}")
