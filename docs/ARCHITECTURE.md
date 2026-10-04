# Architecture

## Purpose

This document describes the target architecture for JanganPrototype and distinguishes **implemented foundations** from **planned systems**.

The guiding principles are:

- server authority for state-changing gameplay
- data-driven content
- persistent player-owned item instances
- low-cost early deployment
- clear separation between static game data and mutable player state
- exploit-resistant economy and inventory transactions

## 1. Static game-data layer — implemented foundation

Unreal reflected types define reusable item metadata.

```text
FItemDefinition
├── ItemID
├── DisplayName
├── ItemCategory
├── Degree
├── DegreeStage
├── RequiredLevel
├── SealTier
├── EquipmentSlot
├── WeaponType
├── OffHandRule
├── AmmunitionType
├── MaxStackSize
├── WeaponStats
├── ShieldStats
└── Economy metadata
```

Current supporting types include:

- `EItemCategory`
- `EWeaponType`
- `EDegreeStage`
- `ESealTier`
- `EEquipmentSlot`
- `EOffHandRule`
- `EAmmunitionType`
- `FStatRange`
- `FWeaponStats`
- `FShieldStats`

Static definitions are suitable for DataTables and should not contain player-specific mutable state.

## 2. Runtime item-instance layer — planned

Player-owned equipment will be represented separately from static definitions.

```text
FItemInstance
├── InstanceID
├── ItemDefinitionID
├── EnhancementLevel
├── CurrentDurability
├── AlchemyModifiers
├── MagicOptions
├── Ownership metadata
└── Persistence metadata
```

This prevents a global definition from being modified when one player's item changes.

## 3. Inventory and equipment — planned

Target responsibilities:

- server-authoritative slot mutations
- stack handling
- equipment compatibility validation
- main-hand / off-hand rules
- shield compatibility
- bow ammunition validation and consumption
- unique item-instance tracking
- anti-duplication safeguards

## 4. Character-stat layer — planned

The character system will own base and derived values such as:

- STR / INT
- HP / MP
- physical and magical attack
- physical and magical defense
- hit / accuracy
- parry / avoidance
- mastery-dependent combat values

Equipment contributes to derived stats through validated item definitions and instances.

## 5. Combat layer — planned

Combat direction:

- click / tab-target gameplay
- server-authoritative hit and damage resolution
- physical and magical damage paths
- skills, cooldowns, buffs and debuffs
- PvE and PvP coefficients separated where needed
- ammunition and resource consumption validated server-side

Clients should request actions; the server decides authoritative results.

## 6. World simulation — planned

World gameplay systems will include:

- monster definitions
- spawn groups
- aggro / threat
- leash behavior
- respawn
- NPC shops
- loot tables
- safe zones
- teleport / gateway logic

To control infrastructure cost, inactive AI and distant world actors should minimize ticking and unnecessary replication.

## 7. Economy — planned

Economy design is treated as a first-class system rather than an afterthought.

Planned areas:

- controlled gold sources
- deliberate gold sinks
- NPC buy / sell
- repair
- alchemy costs
- trade goods
- player trading
- stalls / player shops
- audit logs for high-value transactions

Every economy mutation should be validated by the authoritative server.

## 8. Persistence and backend — planned

Target persistence stack:

```text
UE Dedicated Server
        ↓
Backend / persistence boundary
        ↓
PostgreSQL
```

Persistent records are expected to include:

- account / character
- inventory
- equipment instances
- currencies
- progression
- skills / masteries
- quests
- guild / social state where applicable

Transactions should be used for operations that move or consume valuable state.

## 9. Security model — planned

The architecture assumes the client is untrusted.

Validation targets include:

- inventory mutations
- item-instance ownership
- enhancement operations
- combat requests
- movement bounds
- trade transactions
- currency changes
- loot claims

Important actions should also generate auditable server logs.

## 10. Deployment direction — planned

Early-stage infrastructure should remain cost-conscious.

The preferred starting direction is a small number of Linux-hosted services rather than premature microservice fragmentation. Systems can be separated as load and operational needs become measurable.

## Current architecture checkpoint

**Implemented now:**

- C++ project foundation
- reflected item enums / structs
- DataTable-compatible `FItemDefinition`
- weapon, shield, degree, seal, equipment-slot and off-hand rules
- 1st Degree Chinese equipment data validated locally

**Next:**

Degree progression → Seal / SOx → Item Instance → Inventory.
