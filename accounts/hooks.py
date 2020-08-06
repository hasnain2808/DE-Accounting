# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "accounts"
app_title = "Accounts"
app_publisher = "Moha"
app_description = "Double Entry Accounting System"
app_icon = "octicon octicon-book"
app_color = "grey"
app_email = "hasnain@iwebnotes.com"
app_license = "GNU General Public License"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/accounts/css/accounts.css"
# app_include_js = "/assets/accounts/js/accounts.js"

# include js, css files in header of web template
# web_include_css = "/assets/accounts/css/accounts.css"
# web_include_js = "/assets/accounts/js/accounts.js"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "accounts.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "accounts.install.before_install"
# after_install = "accounts.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "accounts.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"accounts.tasks.all"
# 	],
# 	"daily": [
# 		"accounts.tasks.daily"
# 	],
# 	"hourly": [
# 		"accounts.tasks.hourly"
# 	],
# 	"weekly": [
# 		"accounts.tasks.weekly"
# 	]
# 	"monthly": [
# 		"accounts.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "accounts.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "accounts.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "accounts.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

