from flask import Flask, request, jsonify, make_response
BASE_URL = '/api/v1.0/'

nbaTeams = [
    {
        "teamId": 0,
        "abbreviation": "ATL",
        "teamName": "Atlanta Hawks",
        "knownAs": "Hawks",
        "location": "Atlanta"
    },
    {
        "teamId": 1,
        "abbreviation": "BOS",
        "teamName": "Boston Celtics",
        "knownAs": "Celtics",
        "location": "Boston"
    },
    {
        "teamId": 2,
        "abbreviation": "BKN",
        "teamName": "Brooklyn Nets",
        "knownAs": "Nets",
        "location": "Brooklyn"
    },
    {
        "teamId": 3,
        "abbreviation": "CHA",
        "teamName": "Charlotte Hornets",
        "knownAs": "Hornets",
        "location": "Charlotte"
    },
    {
        "teamId": 4,
        "abbreviation": "CHI",
        "teamName": "Chicago Bulls",
        "knownAs": "Bulls",
        "location": "Chicago"
    },
    {
        "teamId": 5,
        "abbreviation": "CLE",
        "teamName": "Cleveland Cavaliers",
        "knownAs": "Cavaliers",
        "location": "Cleveland"
    },
    {
        "teamId": 6,
        "abbreviation": "DAL",
        "teamName": "Dallas Mavericks",
        "knownAs": "Mavericks",
        "location": "Dallas"
    },
    {
        "teamId": 7,
        "abbreviation": "DEN",
        "teamName": "Denver Nuggets",
        "knownAs": "Nuggets",
        "location": "Denver"
    },
    {
        "teamId": 8,
        "abbreviation": "DET",
        "teamName": "Detroit Pistons",
        "knownAs": "Pistons",
        "location": "Detroit"
    },
    {
        "teamId": 9,
        "abbreviation": "GSW",
        "teamName": "Golden State Warriors",
        "knownAs": "Warriors",
        "location": "Golden State"
    },
    {
        "teamId": 10,
        "abbreviation": "HOU",
        "teamName": "Houston Rockets",
        "knownAs": "Rockets",
        "location": "Houston"
    },
    {
        "teamId": 11,
        "abbreviation": "IND",
        "teamName": "Indiana Pacers",
        "knownAs": "Pacers",
        "location": "Indiana"
    },
    {
        "teamId": 12,
        "abbreviation": "LAC",
        "teamName": "Los Angeles Clippers",
        "knownAs": "Clippers",
        "location": "Los Angeles"
    },
    {
        "teamId": 13,
        "abbreviation": "LAL",
        "teamName": "Los Angeles Lakers",
        "knownAs": "Lakers",
        "location": "Los Angeles"
    },
    {
        "teamId": 14,
        "abbreviation": "MEM",
        "teamName": "Memphis Grizzlies",
        "knownAs": "Grizzlies",
        "location": "Memphis"
    },
    {
        "teamId": 15,
        "abbreviation": "MIA",
        "teamName": "Miami Heat",
        "knownAs": "Heat",
        "location": "Miami"
    },
    {
        "teamId": 16,
        "abbreviation": "MIL",
        "teamName": "Milwaukee Bucks",
        "knownAs": "Bucks",
        "location": "Milwaukee"
    },
    {
        "teamId": 17,
        "abbreviation": "MIN",
        "teamName": "Minnesota Timberwolves",
        "knownAs": "Timberwolves",
        "location": "Minnesota"
    },
    {
        "teamId": 18,
        "abbreviation": "NOP",
        "teamName": "New Orleans Pelicans",
        "knownAs": "Pelicans",
        "location": "New Orleans"
    },
    {
        "teamId": 19,
        "abbreviation": "NYK",
        "teamName": "New York Knicks",
        "knownAs": "Knicks",
        "location": "New York"
    },
    {
        "teamId": 20,
        "abbreviation": "OKC",
        "teamName": "Oklahoma City Thunder",
        "knownAs": "Thunder",
        "location": "Oklahoma City"
    },
    {
        "teamId": 21,
        "abbreviation": "ORL",
        "teamName": "Orlando Magic",
        "knownAs": "Magic",
        "location": "Orlando"
    },
    {
        "teamId": 22,
        "abbreviation": "PHI",
        "teamName": "Philadelphia 76ers",
        "knownAs": "76ers",
        "location": "Philadelphia"
    },
    {
        "teamId": 23,
        "abbreviation": "PHX",
        "teamName": "Phoenix Suns",
        "knownAs": "Suns",
        "location": "Phoenix"
    },
    {
        "teamId": 24,
        "abbreviation": "POR",
        "teamName": "Portland Trail Blazers",
        "knownAs": "Trail Blazers",
        "location": "Portland"
    },
    {
        "teamId": 25,
        "abbreviation": "SAC",
        "teamName": "Sacramento Kings",
        "knownAs": "Kings",
        "location": "Sacramento"
    },
    {
        "teamId": 26,
        "abbreviation": "SAS",
        "teamName": "San Antonio Spurs",
        "knownAs": "Spurs",
        "location": "San Antonio"
    },
    {
        "teamId": 27,
        "abbreviation": "TOR",
        "teamName": "Toronto Raptors",
        "knownAs": "Raptors",
        "location": "Toronto"
    },
    {
        "teamId": 28,
        "abbreviation": "UTA",
        "teamName": "Utah Jazz",
        "knownAs": "Jazz",
        "location": "Utah"
    },
    {
        "teamId": 29,
        "abbreviation": "WAS",
        "teamName": "Washington Wizards",
        "knownAs": "Wizards",
        "location": "Washington"
    }
]

app = Flask(__name__)

@app.route(BASE_URL + "/teams", methods=["GET"])
def getAllTeams():
    return make_response(jsonify(nbaTeams), 200)

@app.route(BASE_URL + "/teams/<int:id>", methods=["GET"])
def get_team_by_id(id):
    return_team = [team for team in nbaTeams if team["teamId"] == id]

    if return_team:
        return make_response(jsonify(return_team[0]), 200)
    else:
        return make_response("A team with an Id: {}, was not found".format(id), 404)

@app.route(BASE_URL + "/teams", methods=["POST"])
def addTeam():
    nextId = nbaTeams[-1]["teamId"] + 1
    newTeam = {
        "teamId": nextId,
        "abbreviation": request.form["abbreviation"],
        "teamName": request.form["name"],
        "knownAs": request.form["knownAs"],
        "location": request.form["location"]
    }
    if nbaTeams.append(newTeam):
        return make_response(jsonify(newTeam), 201)
    else:
        return  make_response(jsonify)

@app.route(BASE_URL + "/teams/<int:id>", methods=["PUT"])
def editTeam(id):
    for team in nbaTeams:
        if team["teamId"] == id:
            team["abbreviation"] = request.form["abbreviation"]
            team["teamName"] = request.form["name"]
            team["knownAs"] = request.form["knownAs"]
            team["location"] = request.form["location"]
            return make_response(jsonify(team), 200)

    return make_response("Team not found", 404)


@app.route(BASE_URL+"/teams/<int:id>", methods=["DELETE"])
def deleteTeam(id):
    for team in nbaTeams:
        if team["teamId"] == id:
            nbaTeams.remove(team)
            break
    return make_response(jsonify({}), 200)

if __name__ == "__main__":
    app.run(debug=True)
