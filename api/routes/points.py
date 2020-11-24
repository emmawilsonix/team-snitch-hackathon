from flask import Blueprint, request

points_routes = Blueprint('points_routes', __name__)
@points_routes.route('/points', methods=['GET', 'POST'])
def points_list():
    if request.method == 'GET':
        if request.query_string:
            if (
                request.args.get('userID') is None and 
                request.args.get('sourceUserID') is None and
                request.args.get('orderby') is None
            ):
                return "Bad request param", 400
            else if request.args.get('userID') and request.args.get('sourceUserID'):
                # return the points list with userID and sourceUserID
                pass
            else if request.args.get('userID'):
                # return the points list with userID 
                pass
            else if request.args.get('sourceUserID'):
                # return the points list with sourceUserID 
                pass
            else:
                # do orderby select
                pass
        
        else:
            # select entire points list
            pass
    elif request.method == 'POST':
        userID = request.form.get('userID')
        sourceUserID = request.form.get('sourceUserID')
        points = request.form.get('points')

        if userID is None or sourceUserID is None or points is None:
            return "Bad request, incorrect POST information", 400

        # create the points
        pass

    else:
        return "Bad request method", 405


    return "points"