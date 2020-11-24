from flask import Blueprint, request

teams_routes = Blueprint('teams_routes', __name__)
@teams_routes.route('/teams', methods=['GET', 'POST'])
def teams_list():
    if request.method == 'GET':
        if request.query_string:
            if request.args.get('orderby') is None:
                return "Bad request param breh", 400
            if request.args.get('orderby'):
                # do orderby select
                pass
        else:
            # select entire teams list
            pass
    elif request.method == 'POST':
        # create the team 
        pass

    else:
        return "Bad request method", 405


    return "teams"