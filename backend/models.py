from extensions import db


# Dimension Tables
class Country(db.Model):
    __tablename__ = "country"
    id_country = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flag_emoji = db.Column(db.String(10))

    def __repr__(self):
        return f"<Country {self.name}>"


class City(db.Model):
    __tablename__ = "city"
    id_city = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_country = db.Column(
        db.Integer, db.ForeignKey("country.id_country"), nullable=False
    )
    country = db.relationship("Country", backref="cities")

    def __repr__(self):
        return f"<City {self.name}>"


class Club(db.Model):
    __tablename__ = "club"
    id_club = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_country = db.Column(
        db.Integer, db.ForeignKey("country.id_country"), nullable=False
    )
    id_city = db.Column(db.Integer, db.ForeignKey("city.id_city"))
    logo_image_url = db.Column(db.String(200))
    nickname = db.Column(db.String(100))
    foundation_date = db.Column(db.Date)
    stadium_name = db.Column(db.String(100))

    country = db.relationship("Country", backref="clubs")
    city = db.relationship("City", backref="clubs")

    def __repr__(self):
        return f"<Club {self.name}>"


class Position(db.Model):
    __tablename__ = "position"
    id_position = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))

    def __repr__(self):
        return f"<Position {self.name}>"


class Player(db.Model):
    __tablename__ = "player"
    id_player = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    id_country_born = db.Column(db.Integer, db.ForeignKey("country.id_country"))
    id_country_nationality = db.Column(db.Integer, db.ForeignKey("country.id_country"))
    birth_date = db.Column(db.Date, nullable=False)
    id_current_club = db.Column(db.Integer, db.ForeignKey("club.id_club"))
    id_position = db.Column(db.Integer, db.ForeignKey("position.id_position"))
    sub_position = db.Column(db.String(100))
    foot = db.Column(db.String(10))
    height_in_cm = db.Column(db.Integer)
    image_url = db.Column(db.String(200))
    retired = db.Column(db.Boolean, default=False)

    country_born = db.relationship(
        "Country", foreign_keys=[id_country_born], backref="born_players"
    )
    country_nationality = db.relationship(
        "Country", foreign_keys=[id_country_nationality], backref="national_players"
    )
    current_club = db.relationship("Club", backref="players")
    position = db.relationship("Position", backref="players")

    def __repr__(self):
        return f"<Player {self.first_name} {self.last_name}>"


class Competition(db.Model):
    __tablename__ = "competition"
    id_competition = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_country = db.Column(
        db.Integer, db.ForeignKey("country.id_country"), nullable=False
    )
    competition_type = db.Column(db.String(50))

    country = db.relationship("Country", backref="competitions")

    def __repr__(self):
        return f"<Competition {self.name}>"


# Fact Tables
class Match(db.Model):
    __tablename__ = "match"
    id_match = db.Column(db.Integer, primary_key=True)
    id_competition = db.Column(
        db.Integer, db.ForeignKey("competition.id_competition"), nullable=False
    )
    match_date = db.Column(db.Date, nullable=False)
    season = db.Column(db.String(20), nullable=False)
    id_home_club = db.Column(db.Integer, db.ForeignKey("club.id_club"), nullable=False)
    id_away_club = db.Column(db.Integer, db.ForeignKey("club.id_club"), nullable=False)
    home_club_goals = db.Column(db.Integer, nullable=False)
    away_club_goals = db.Column(db.Integer, nullable=False)
    result_aggregate = db.Column(db.String(10))
    article_url = db.Column(db.String(200))

    competition = db.relationship("Competition", backref="matches")
    home_club = db.relationship(
        "Club", foreign_keys=[id_home_club], backref="home_matches"
    )
    away_club = db.relationship(
        "Club", foreign_keys=[id_away_club], backref="away_matches"
    )

    def __repr__(self):
        return f"<Match {self.home_club} vs {self.away_club} on {self.match_date}>"


class Appearance(db.Model):
    __tablename__ = "appearance"
    id_appearance = db.Column(db.Integer, primary_key=True)
    id_match = db.Column(db.Integer, db.ForeignKey("match.id_match"), nullable=False)
    id_player = db.Column(db.Integer, db.ForeignKey("player.id_player"), nullable=False)
    goals = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    minutes_played = db.Column(db.Integer, nullable=False)
    fg_starter = db.Column(db.Boolean, default=False)
    fg_yellow_card = db.Column(db.Boolean, default=False)
    fg_red_card = db.Column(db.Boolean, default=False)

    match = db.relationship("Match", backref="appearances")
    player = db.relationship("Player", backref="appearances")

    def __repr__(self):
        return f"<Appearance {self.player} in {self.match}>"


class Transfer(db.Model):
    __tablename__ = "transfer"
    id_transfer = db.Column(db.Integer, primary_key=True)
    id_player = db.Column(db.Integer, db.ForeignKey("player.id_player"), nullable=False)
    id_from_club = db.Column(db.Integer, db.ForeignKey("club.id_club"))
    id_to_club = db.Column(db.Integer, db.ForeignKey("club.id_club"))
    transfer_date = db.Column(db.Date, nullable=False)
    transfer_fee = db.Column(db.Numeric(15, 2))
    market_value_in_eur = db.Column(db.Numeric(15, 2))
    transfer_type = db.Column(db.String(50))

    player = db.relationship("Player", backref="transfers")
    from_club = db.relationship(
        "Club", foreign_keys=[id_from_club], backref="transfers_from"
    )
    to_club = db.relationship("Club", foreign_keys=[id_to_club], backref="transfers_to")

    def __repr__(self):
        return f"<Transfer {self.player} from {self.from_club} to {self.to_club} on {self.transfer_date}>"


class PlayerCareer(db.Model):
    __tablename__ = "player_career"
    id_player_career = db.Column(db.Integer, primary_key=True)
    id_player = db.Column(db.Integer, db.ForeignKey("player.id_player"), nullable=False)
    id_club = db.Column(db.Integer, db.ForeignKey("club.id_club"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    player = db.relationship("Player", backref="career_records")
    club = db.relationship("Club", backref="career_players")

    def __repr__(self):
        return f"<PlayerCareer {self.player} at {self.club} from {self.start_date} to {self.end_date}>"
