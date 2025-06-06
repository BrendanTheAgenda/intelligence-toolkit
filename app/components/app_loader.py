# Copyright (c) 2024 Microsoft Corporation. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project.
#
import os

import components.app_mode as am
import components.app_user as au
import streamlit as st
from components.app_auth import check_password, load_passwords
from javascript.styles import add_styles
from streamlit.source_util import (
    _on_pages_changed,
    get_pages,
)


def load_multipage_app(sv=None):
    if os.getenv("AUTH_ENABLED") == "TRUE":
        load_passwords()
        check_password()
    if os.getenv("HIDE_SETTINGS") == "TRUE":
        current_pages = get_pages("Home.py")

        for key, value in current_pages.items():
            if value["page_name"] == "Settings":
                del current_pages[key]
                break
        _on_pages_changed.send()

    # Load user if logged in
    user = au.AppUser()
    user.view_get_info()

    app_mode = am.AppMode()
    app_mode.config()

    add_styles()

    if sv:
        reset_workflow_button = st.sidebar.button(
            ":warning: Reset workflow",
            use_container_width=True,
            help="Clear all data on this workflow and start over. CAUTION: This action can't be undone.",
        )
        if reset_workflow_button:
            sv.reset_workflow()
            st.rerun()
