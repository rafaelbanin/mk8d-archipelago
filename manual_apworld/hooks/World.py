from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item
from ..Items import ManualItem
from ..Locations import ManualLocation
from ..Data import game_table, item_table, location_table, region_table
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat, remove_specific_item
import logging
import random

def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> list[str] | str | bool:
    return False

def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    Randomize the track unlock order without fixed logic between specific tracks.
    - 4 random tracks start available (no requirement).
    - Each remaining track requires a random number of total unlocks (1-92).
    - Track Unlock items are placed randomly by removing fixed place_item entries.
    """
    # Identify track locations by index so location IDs stay in the original order
    track_indices = [i for i, loc in enumerate(location_table) if not loc.get('victory')]
    goal_index = next((i for i, loc in enumerate(location_table) if loc.get('victory')), None)

    if len(track_indices) != 96:
        logging.warning(f"Expected 96 track locations, found {len(track_indices)}. Skipping randomization.")
        return

    # Remove fixed item placements so Archipelago fills Track Unlock items randomly
    for i in track_indices:
        location_table[i].pop('place_item', None)
        location_table[i].pop('requires', None)

    # Pick 4 random starting tracks
    shuffled = track_indices[:]
    random.shuffle(shuffled)
    starting_tracks = shuffled[:4]

    # The other 92 tracks get randomized @Unlocks requirements (1 to 92)
    remaining_tracks = shuffled[4:]
    requirements = list(range(1, 93))
    random.shuffle(requirements)

    for i in starting_tracks:
        location_table[i]['requires'] = []

    for i, req in zip(remaining_tracks, requirements):
        location_table[i]['requires'] = f"|@Unlocks:{req}|"

    # Goal is reachable once the player has collected 77 unlocks
    if goal_index is not None:
        location_table[goal_index]['requires'] = "|@Unlocks:77|"

    logging.info(f"Random starting tracks: {[location_table[i]['name'] for i in starting_tracks]}")

def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    locationNamesToRemove: list[str] = []
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    itemNamesToRemove: list[str] = []
    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        remove_specific_item(item_pool, item)
    return item_pool

def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    pass

def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    pass

def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    """Send track requirements and starting tracks to the frontend so it can display availability correctly."""
    requirements = {}
    starting_tracks = []
    for loc in location_table:
        name = loc['name']
        if loc.get('victory'):
            continue
        req = loc.get('requires', '')
        if not req or req == []:
            requirements[name] = 0
            starting_tracks.append(name)
        elif isinstance(req, str) and req.startswith('|@Unlocks:') and req.endswith('|'):
            try:
                requirements[name] = int(req[10:-1])
            except ValueError:
                requirements[name] = 0
        else:
            requirements[name] = 0
            starting_tracks.append(name)
    slot_data['track_requirements'] = requirements
    slot_data['starting_tracks'] = starting_tracks
    return slot_data

def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    return slot_data
