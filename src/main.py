from libs import edp_client as edp


def main_wokrflow():
    edp.login()
    edp.get_consumption()

