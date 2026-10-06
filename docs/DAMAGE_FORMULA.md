# Damage Formula

> Status: **working Silkroad-style model for JanganPrototype**.  
> The structure below is our current implementation target, but some original Silkroad internals (especially the exact Balance Rate formula) still require validation from game files / reverse engineering.

## 1. Core component formula

For a single damage component:

```text
DamageComponent =
(
    ((A + B) * (1 + C))
    / (1 + D)
    - E
)
* F
* (1 + G)
* H
* R
```

Where:

| Symbol | Meaning |
|---|---|
| `A` | Basic Attack Power |
| `B` | Skill Attack Power |
| `C` | Attack Power Increasing Rate |
| `D` | Target total accessory Absorption Rate |
| `E` | Target Defense Power for the component being calculated |
| `F` | Balance Rate |
| `G` | Total Damage Increasing Rate |
| `H` | Skill Attack Power Rate / skill multiplier |
| `R` | 3-roll randomization multiplier |

### Attack Power Increase (`C`)

`C` includes attack-power-increasing effects such as equipment, buffs, passives and the relevant mastery attack-increase passive.

The old `mastery_incr` term refers specifically to the **Physical/Magical Attack Increase passive on the main trunk/body of the corresponding mastery/skill tree**.

It is represented as part of:

```text
(1 + C)
```

## 2. Physical and magical damage are calculated separately

Physical and magical damage must stay as separate components.

Conceptually:

```text
PhysicalDamage = PhysicalComponentFormula(...)
MagicalDamage  = MagicalComponentFormula(...)

TotalDamage = PhysicalDamage + MagicalDamage
```

Physical damage uses the target's physical defense.  
Magical / imbue damage uses the target's magical defense.

Imbue damage belongs to the magical component.

## 3. Critical hit rule

A critical hit affects **only the physical damage component**.

```text
PhysicalDamageCrit = PhysicalDamage * 2
MagicalDamageCrit  = MagicalDamage

CriticalTotalDamage =
    (PhysicalDamage * 2)
    + MagicalDamage
```

Therefore, magical damage and imbue damage are **not doubled** by a critical hit.

For a normal hit:

```text
NormalTotalDamage =
    PhysicalDamage
    + MagicalDamage
```

## 4. 3-roll randomization

JanganPrototype uses a Silkroad-style **3-roll / 3-dice** randomization method instead of one uniform damage roll.

Generate three independent multipliers:

```text
r1 = random(0.8, 1.2)
r2 = random(0.8, 1.2)
r3 = random(0.8, 1.2)
```

Then average them:

```text
R = (r1 + r2 + r3) / 3
```

Properties:

- Minimum possible multiplier: `0.8`
- Maximum possible multiplier: `1.2`
- Mean multiplier: `1.0`
- Averaging three rolls makes extreme values less frequent than a single uniform roll.

## 5. Compact notation

For a non-critical component:

```text
BaseComponent =
((A + B) * (1 + C) / (1 + D) - E)
* F
* (1 + G)
* H
* R
```

Final total:

```text
Physical =
((A_phys + B_phys) * (1 + C_phys) / (1 + D_phys) - E_phys)
* F_phys
* (1 + G_phys)
* H_phys
* R_phys

Magical =
((A_mag + B_mag) * (1 + C_mag) / (1 + D_mag) - E_mag)
* F_mag
* (1 + G_mag)
* H_mag
* R_mag

FinalDamage =
(IsCritical ? Physical * 2 : Physical)
+ Magical
```

## 6. Current validation status

Confirmed project decisions:

- Physical and magical damage are separate.
- Critical hit doubles only the physical component.
- Magical / imbue damage is not doubled by critical hits.
- Damage randomization uses the 3-roll averaging method.
- `mastery_incr` means the relevant main-tree Physical/Magical Attack Increase passive.

Still requiring original-game validation:

- Exact original Silkroad Balance Rate formula (`F`).
- Exact ordering / rounding behavior used by the original server.
- Exact original constants and caps, if any, for absorption, damage increase and skill multipliers.
- Whether every damage source uses the same randomization stage/order.

Example previously used during research:

```text
F = 1.07788162
```

This value is illustrative and is **not yet treated as the confirmed original Balance Rate formula**.
