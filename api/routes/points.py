from flask import Blueprint, request

points_routes = Blueprint('points_routes', __name__)
@points_routes.route('/points', methods=['GET', 'POST'])
def points_list():
    if request.method == 'GET':
        if request.query_string:
            if (
                request.args.get('teamID') is None and 
                request.args.get('orderby') is None
            ):
                return "Bad request param breh", 400
            if request.args.get('teamID'):
                # do team ID select
                pass
            if request.args.get('orderby'):
                # do orderby select
                pass
        else:
            # select entire points list
            pass
    elif request.method == 'POST':
        # create the points
        pass

    else:
        return "Bad request method", 405


    return "points "