# Mario Kart 8 Deluxe — Archipelago Manual

Manual Archipelago setup for **Mario Kart 8 Deluxe** with all **96 tracks** (base game + Booster Course Pass).

## Concept

- Start with **4 random initial tracks** available.
- Each completed track gives a random `Track Unlock` item.
- Tracks require a random number of total unlocks to become available (e.g., "Requires 5 unlocks"), so there is **no fixed logic between specific tracks**.
- **Goal:** complete 80% of the tracks (77/96) to unlock victory.
- Everything is manual: play the track in MK8D, come back to the frontend and click **Complete**; Archipelago sends the reward immediately.
- On goal completion, the frontend marks all remaining tracks as completed, releasing every leftover item to its respective game. `release_mode` and `collect_mode` are also set to `auto-enabled` in the YAML for automatic collection.

## Structure

```
mk8d-archipelago/
├── manual_apworld/          # Files to build the .apworld
│   ├── data/
│   │   ├── game.json
│   │   ├── items.json
│   │   ├── locations.json
│   │   └── regions.json
│   └── MarioKart8Deluxe.yaml
├── frontend/
│   └── index.html           # Web frontend (open in browser)
└── README.md
```

## How to use

### 1. Ready-to-use APWorld

The file `manual_mariokart8deluxe.apworld` is already generated at the project root. Just copy it to your Archipelago worlds folder.

**Important note:** Manual registers the game internally as `Manual_Mario Kart 8 Deluxe_ManualMK8D`. The YAML and frontend already use this name.

- **Windows:** `%LOCALAPPDATA%\Archipelago\lib\worlds\`
- **Linux:** `~/.local/share/Archipelago/lib/worlds/`

If you want to rebuild it, use the **ManualBuilder**: https://manualforarchipelago.github.io/ManualBuilder/ (upload the JSONs from `manual_apworld/data/` and click **Export to APWorld**).

### 2. Generate the seed

1. Place the YAML `manual_apworld/MarioKart8Deluxe.yaml` into your Archipelago `Players/` folder.
2. Edit the `name: MK8DPlayer` field to whatever you want.
3. Generate the seed (`ArchipelagoGenerate.exe` or `python Generate.py`).
4. Start the server (`ArchipelagoServer.exe` / `python MultiServer.py`).

### 3. Use the frontend

1. Open `frontend/index.html` in a browser (you can use a simple local server).
2. Fill in:
   - **Host / IP**: where the Archipelago server is running (e.g. `archipelago.gg` or `localhost`)
   - **Port**: server port (e.g. `38281`)
   - **Slot Name**: the same `name` you set in the YAML
   - **Password**: if the server has a password
3. Click **Connect**.
4. The **4 random initial tracks** appear as **Available**.
5. Play any available track in MK8D, return to the frontend and click **Complete**.
6. A random `Track Unlock` item is sent immediately, and any track whose unlock requirement is now met becomes available.
7. Once **77 tracks** are completed, click **Completar Goal** to finish the game and release all remaining items.

## Images

The frontend uses official track icons from the **Super Mario Wiki**. If any image fails to load, check your internet connection or replace the URLs in `TRACK_IMAGES` inside `index.html`.

## Notes

- This project **does not connect to Mario Kart 8 Deluxe** nor modify the game.
- Progress is tracked manually through the frontend.
- You can play solo or in a multiworld with other games.

## Credits

- Track images: [Super Mario Wiki](https://www.mariowiki.com/)
- Manual system: [ManualForArchipelago](https://github.com/ManualForArchipelago/Manual)
- Archipelago: [ArchipelagoMW](https://archipelago.gg/)
