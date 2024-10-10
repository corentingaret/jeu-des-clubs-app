# routes/player_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from helpers.database import get_db
from helpers.auth import get_current_user
from models import Player
from schemas import PlayerCreate, PlayerUpdate
from typing import List

router = APIRouter()


@router.get("/players", response_model=List[dict])
def get_players(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    players = db.query(Player).all()
    return [
        {
            "id": p.id_player,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "country_born": p.country_born.name if p.country_born else None,
            "country_nationality": (
                p.country_nationality.name if p.country_nationality else None
            ),
            "current_club": p.current_club.name if p.current_club else None,
            "position": p.position.name if p.position else None,
            "foot": p.foot,
            "height_in_cm": p.height_in_cm,
            "retired": p.retired,
        }
        for p in players
    ]


@router.post("/players", response_model=dict)
def add_player(
    player: PlayerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    new_player = Player(**player.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return {
        "message": "Player added successfully.",
        "player": {
            "id": new_player.id_player,
            "first_name": new_player.first_name,
            "last_name": new_player.last_name,
        },
    }


@router.get("/players/{id_player}", response_model=dict)
def get_player(
    id_player: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    player = db.query(Player).filter(Player.id_player == id_player).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return {
        "id": player.id_player,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "country_born": player.country_born.name if player.country_born else None,
        "country_nationality": (
            player.country_nationality.name if player.country_nationality else None
        ),
        "current_club": player.current_club.name if player.current_club else None,
        "position": player.position.name if player.position else None,
        "sub_position": player.sub_position,
        "foot": player.foot,
        "height_in_cm": player.height_in_cm,
        "image_url": player.image_url,
        "retired": player.retired,
    }


@router.put("/players/{id_player}", response_model=dict)
def update_player(
    id_player: int,
    player: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_player = db.query(Player).filter(Player.id_player == id_player).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    for key, value in player.dict(exclude_unset=True).items():
        setattr(db_player, key, value)

    db.commit()
    db.refresh(db_player)

    return {
        "message": "Player updated successfully.",
        "player": {
            "id": db_player.id_player,
            "first_name": db_player.first_name,
            "last_name": db_player.last_name,
            "country_born": (
                db_player.country_born.name if db_player.country_born else None
            ),
            "country_nationality": (
                db_player.country_nationality.name
                if db_player.country_nationality
                else None
            ),
            "current_club": (
                db_player.current_club.name if db_player.current_club else None
            ),
            "position": db_player.position.name if db_player.position else None,
            "sub_position": db_player.sub_position,
            "foot": db_player.foot,
            "height_in_cm": db_player.height_in_cm,
            "image_url": db_player.image_url,
            "retired": db_player.retired,
        },
    }


@router.delete("/players/{id_player}", response_model=dict)
def delete_player(
    id_player: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    player = db.query(Player).filter(Player.id_player == id_player).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return {"message": "Player deleted successfully"}
