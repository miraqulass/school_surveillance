from flask import Flask, Blueprint, render_template

security_bp = Blueprint("security", __name__, template_folder="templates")


@security_bp.route("/")
def index():
    return render_template(
        "security-recorded-motion.html", active_page="security_recorded_motion"
    )


@security_bp.route("/security_recorded_motion")
def security_recorded_motion():
    return render_template(
        "security-recorded-motion.html", active_page="security_recorded_motion"
    )


@security_bp.route("/security_live_feed")
def security_live_feed():
    return render_template("security-live-feed.html", active_page="security_live_feed")


@security_bp.route("/security_students_list")
def security_students_list():
    return render_template(
        "security-student-list.html", active_page="security_students_list"
    )


if __name__ == "__main__":
    app.run(debug=True)
