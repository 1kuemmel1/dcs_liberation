from __future__ import annotations

import logging
import pickle
import shutil
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from game.profiling import logged_duration

if TYPE_CHECKING:
    from game import Game

_dcs_saved_game_folder: Optional[str] = None


def setup(user_folder: str) -> None:
    global _dcs_saved_game_folder
    _dcs_saved_game_folder = user_folder
    if not save_dir().exists():
        save_dir().mkdir(parents=True)


def base_path() -> str:
    global _dcs_saved_game_folder
    assert _dcs_saved_game_folder
    return _dcs_saved_game_folder


def save_dir() -> Path:
    return Path(base_path()) / "Liberation" / "Saves"


def _temporary_save_file() -> str:
    return str(save_dir() / "tmpsave.liberation")


def _autosave_path() -> str:
    return str(save_dir() / "autosave.liberation")


def mission_path_for(name: str) -> Path:
    return Path(base_path()) / "Missions" / name


def load_game(path: str) -> Optional[Game]:
    with open(path, "rb") as f:
        try:
            save = pickle.load(f)
            save.savepath = path
            return save
        except Exception:
            logging.exception("Invalid Save game")
            return None


def save_game(game: Game) -> bool:
    with logged_duration("Saving game"):
        try:
            with open(_temporary_save_file(), "wb") as f:
                pickle.dump(game, f)
            shutil.copy(_temporary_save_file(), game.savepath)
            return True
        except Exception:
            logging.exception("Could not save game")
            return False


def autosave(game: Game) -> bool:
    """
    Autosave to the autosave location
    :param game: Game to save
    :return: True if saved succesfully
    """
    try:
        with open(_autosave_path(), "wb") as f:
            pickle.dump(game, f)
        return True
    except Exception:
        logging.exception("Could not save game")
        return False
