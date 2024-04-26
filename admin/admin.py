from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/")
def index():
    return render_template("recorded-motion.html", active_page="recorded_motion")


@admin_bp.route("/recorded_motion")
def recorded_motion():
    return render_template("recorded-motion.html", active_page="recorded_motion")


@admin_bp.route("/live_feed")
def live_feed():
    return render_template("live-feed.html", active_page="live_feed")


@admin_bp.route("/students_list")
def students_list():
    return render_template("student-list.html", active_page="students_list")


@admin_bp.route("/user_list")
def user_list():
    return render_template("user-list.html", active_page="user_list")
