# Development Roadmap

This roadmap tracks the engineering order for JanganPrototype. It is intentionally staged so later MMORPG systems build on stable data, authority, and persistence foundations.

## Phase 1 — Project foundation

- [x] Development environment & C++ project setup
- [x] Project folder structure & naming conventions
- [x] Git / GitHub source-control workflow
- [x] Core enums, structs & shared item data types
- [x] Item Definition System
- [x] Chinese 1st Degree equipment dataset
- [ ] Degree & Equipment Progression System
- [ ] Seal / SOx Tier System
- [ ] Item Instance System

## Phase 2 — Inventory & equipment

- [ ] Inventory System
- [ ] Equipment Slot System
- [ ] Main-hand / off-hand validation
- [ ] Shield compatibility rules
- [ ] Arrow / Ammunition System
- [ ] Server-authoritative item mutations
- [ ] Unique item-instance IDs
- [ ] Duplication safeguards

## Phase 3 — Character progression

- [ ] Character base attributes
- [ ] STR / INT system
- [ ] Derived character stats
- [ ] Weapon & equipment stat calculation
- [ ] Character level & EXP
- [ ] Skill EXP / SP
- [ ] Mastery system
- [ ] Skill definitions and requirements

## Phase 4 — Combat

- [ ] Target selection / tab-target
- [ ] Basic attacks
- [ ] Skill casting
- [ ] Cooldowns
- [ ] Physical damage
- [ ] Magical damage
- [ ] Critical / hit / accuracy / parry
- [ ] Buff / debuff framework
- [ ] PvE damage rules
- [ ] PvP damage rules
- [ ] Server-side combat validation

## Phase 5 — Item enhancement

- [ ] Durability
- [ ] Alchemy enhancement (+)
- [ ] Alchemy stones
- [ ] Magic options / blue attributes
- [ ] Failure / protection rules
- [ ] Weapon enhancement glow / VFX

## Phase 6 — PvE world systems

- [ ] Monster definitions
- [ ] Monster stats & combat
- [ ] AI
- [ ] Aggro / threat
- [ ] Spawn groups
- [ ] Respawn / leash
- [ ] Server-side mob optimization
- [ ] Loot tables
- [ ] Equipment drops
- [ ] SOx drops
- [ ] Gold / EXP / SP rewards

## Phase 7 — NPC & economy

- [ ] NPC base system
- [ ] NPC shops
- [ ] Buy / sell
- [ ] Repair
- [ ] Gold economy core
- [ ] Gold source / sink balancing
- [ ] Item pricing
- [ ] Player-to-player trading
- [ ] Stall / player shop
- [ ] Trade goods
- [ ] Trader / Hunter / Thief job system

## Phase 8 — Quests & social systems

- [ ] Quest definitions
- [ ] Quest progress
- [ ] Quest rewards
- [ ] Party system
- [ ] Party EXP / loot distribution
- [ ] Friends
- [ ] Guilds
- [ ] Guild permissions / progression
- [ ] Chat

## Phase 9 — PvP & world rules

- [ ] PvP flagging
- [ ] Duel system
- [ ] Colosseum PvP
- [ ] Death / resurrection
- [ ] Town / safe zones
- [ ] World-zone rules
- [ ] Teleport / gateway system
- [ ] Jangan gameplay integration

## Phase 10 — Networking & persistence

- [ ] Replication architecture
- [ ] Server authority / RPC validation
- [ ] Player sessions
- [ ] Account / authentication backend
- [ ] Character creation / selection
- [ ] Persistent character data
- [ ] Persistent inventory / equipment
- [ ] PostgreSQL architecture
- [ ] Backend API boundary
- [ ] Database transactions
- [ ] Save / load
- [ ] Rollback-safe high-value operations

## Phase 11 — Security & operations

- [ ] Movement validation
- [ ] Combat validation
- [ ] Economy validation
- [ ] Anti-cheat foundations
- [ ] Logging / audit
- [ ] GM / admin tools
- [ ] Server metrics / monitoring
- [ ] Crash recovery / data safety

## Phase 12 — Deployment & live operations

- [ ] Dedicated server build
- [ ] Linux deployment
- [ ] Server performance optimization
- [ ] Database performance optimization
- [ ] Network bandwidth optimization
- [ ] Load / stress testing
- [ ] Automated gameplay tests
- [ ] Security / exploit testing
- [ ] Internal testing
- [ ] Alpha infrastructure
- [ ] Beta infrastructure
- [ ] Live-server architecture
- [ ] Patch / version management
- [ ] Live operations tools
- [ ] Level-cap expansion pipeline
- [ ] New Degree / region integration
- [ ] Production launch & scaling

---

## Current focus

**Degree & Equipment Progression System**

Immediate sequence:

```text
Degree Progression
      ↓
Seal / SOx
      ↓
Item Instance
      ↓
Inventory
      ↓
Equipment
```
