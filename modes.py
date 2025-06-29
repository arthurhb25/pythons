import enum

class GameMode(enum.Enum):
    CLASSIC_1P = 0
    CLASSIC_2P = 1
    TIME_ATTACK_1P = 2
    TIME_ATTACK_2P = 3

def get_mode_settings(mode):
    if mode == GameMode.CLASSIC_1P:
        return {"time_attack": False, "players": 1}
    if mode == GameMode.CLASSIC_2P:
        return {"time_attack": False, "players": 2}
    if mode == GameMode.TIME_ATTACK_1P:
        return {"time_attack": True, "players": 1}
    if mode == GameMode.TIME_ATTACK_2P:
        return {"time_attack": True, "players": 2}
    return {"time_attack": False, "players": 2}
