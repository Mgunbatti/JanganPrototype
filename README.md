# JanganPrototype

**Unreal Engine 5.8 C++ MMORPG systems prototype**

JanganPrototype is an in-development MMORPG engineering project focused on persistent-world systems, server-authoritative gameplay, data-driven itemization, economy design, combat architecture, and scalable backend foundations.

The project takes inspiration from the pacing and equipment philosophy of classic Silk Road-era MMORPGs while being developed as an independent implementation with original code, systems, and project structure.

> **Status:** Early systems prototype. Core item definitions and the first Chinese weapon/shield data model are implemented. Networking, persistence, combat, inventory, economy, and live-server infrastructure are planned/in progress.

## Current milestone

- Development environment and UE5 C++ project setup
- Shared item enums and structs
- Data-driven `FItemDefinition`
- Degree / stage / seal data model
- Chinese weapon types: Blade, Sword, Glavie, Spear, Bow
- Shield and off-hand rules
- Bow ammunition requirement model
- 1st Degree Chinese equipment dataset validated in UE5 DataTable
- Git-based source control workflow

The 1st Degree DataTable currently contains **18 equipment definitions**: 15 weapons and 3 shields. Binary UE content is intentionally excluded from this public repository.

## Technical direction

- **Engine:** Unreal Engine 5.8.x
- **Gameplay:** C++
- **Data:** Unreal DataTables / reflected USTRUCTs
- **World tooling:** Unreal Python scripts
- **Networking goal:** server-authoritative multiplayer
- **Persistence goal:** PostgreSQL-backed character, inventory, economy, and progression data
- **Deployment goal:** cost-conscious Linux dedicated server architecture
- **Version control:** Git + GitHub

## Item-system foundation

The current item model separates static definitions from future player-owned runtime instances.

```text
FItemDefinition
├── Identity
├── Degree / DegreeStage
├── SealTier
├── EquipmentSlot
├── WeaponType
├── OffHandRule
├── WeaponStats
├── ShieldStats
└── Economy metadata

Future:
FItemInstance
├── Unique instance ID
├── Definition reference
├── Enhancement level (+)
├── Current durability
├── Alchemy modifiers
└── Magic options
```

This separation is intended to support persistent inventory, alchemy, secure trading, rollback-safe database transactions, and anti-duplication validation later in development.

## Chinese weapon model

| Type | Slot behavior | Design direction |
|---|---|---|
| Blade | Main Hand + Shield allowed | Physical-leaning one-hand weapon |
| Sword | Main Hand + Shield allowed | Magical-leaning one-hand weapon |
| Glavie | Main Hand, off-hand blocked | Physical-leaning two-hand weapon |
| Spear | Main Hand, off-hand blocked | Magical-leaning two-hand weapon |
| Bow | Main Hand + Arrow required | Ranged hybrid weapon |
| Shield | Off Hand | Defensive equipment |

## Repository structure

```text
Config/                         Unreal project configuration
Scripts/                        Unreal Python world/prototyping tools
Source/JanganPrototype/        C++ game module
Source/JanganPrototype/Items/  Item-system data types
docs/                           Architecture and roadmap
```

Large generated folders, UE binaries, local caches, source assets, and public-game content are intentionally excluded through `.gitignore`.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md).

## Build notes

The repository represents engineering source and documentation rather than a complete redistributable game package. Unreal `Content/`, generated binaries, caches, previews, and source art are intentionally excluded.

For local development, use the matching Unreal Engine version and regenerate project files as needed from `JanganPrototype.uproject`.

## Project ownership

This is a **proprietary portfolio / development repository**, not an open-source project.

No license is granted to reuse, redistribute, commercialize, or create derivative works from this repository except for rights that may be required by GitHub's Terms of Service. See [LICENSE](LICENSE) for details.

Third-party trademarks belong to their respective owners. This project is not affiliated with or endorsed by Joymax or any other third-party game publisher, and no original Silkroad Online game assets are intended to be distributed in this repository.

---

**Current focus:** Degree & Equipment Progression → Seal / SOx → Item Instance → Inventory
