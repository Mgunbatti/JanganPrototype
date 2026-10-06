#include "Items/DegreeProgression.h"

namespace
{
    constexpr int32 UnsupportedLevel = INDEX_NONE;

    int32 GetStageIndex(const EDegreeStage DegreeStage)
    {
        switch (DegreeStage)
        {
        case EDegreeStage::Main: return 0;
        case EDegreeStage::Mid:  return 1;
        case EDegreeStage::High: return 2;
        default:                  return INDEX_NONE;
        }
    }

    int32 GetGroupOffset(const EDegreeEquipmentGroup EquipmentGroup)
    {
        switch (EquipmentGroup)
        {
        case EDegreeEquipmentGroup::WeaponShieldGloves: return 0;
        case EDegreeEquipmentGroup::Shoulder:           return 1;
        case EDegreeEquipmentGroup::Foot:               return 2;
        case EDegreeEquipmentGroup::Head:               return 3;
        case EDegreeEquipmentGroup::Legs:               return 4;
        case EDegreeEquipmentGroup::Chest:              return 5;
        default:                                        return INDEX_NONE;
        }
    }
}

bool UDegreeProgressionLibrary::IsSupportedDegree(const int32 Degree)
{
    return Degree >= 1 && Degree <= 5;
}

int32 UDegreeProgressionLibrary::GetDegreeBaseLevel(const int32 Degree)
{
    switch (Degree)
    {
    case 1: return 1;
    case 2: return 8;
    case 3: return 16;
    case 4: return 24;
    case 5: return 32;
    default: return UnsupportedLevel;
    }
}

int32 UDegreeProgressionLibrary::GetRequiredLevel(
    const int32 Degree,
    const EDegreeEquipmentGroup EquipmentGroup,
    const EDegreeStage DegreeStage)
{
    if (!IsSupportedDegree(Degree))
    {
        return UnsupportedLevel;
    }

    const int32 StageIndex = GetStageIndex(DegreeStage);
    const int32 GroupOffset = GetGroupOffset(EquipmentGroup);

    if (StageIndex == INDEX_NONE || GroupOffset == INDEX_NONE)
    {
        return UnsupportedLevel;
    }

    // D1 differs slightly from later degrees, so keep it explicit.
    if (Degree == 1)
    {
        static constexpr int32 D1Levels[6][3] =
        {
            { 1, 3, 5 },   // Weapon / Shield / Gloves
            { 1, 4, 6 },   // Shoulder
            { 1, 5, 7 },   // Foot
            { 1, 6, 8 },   // Head
            { 1, 7, 9 },   // Legs
            { 1, 8, 10 }   // Chest
        };

        return D1Levels[GroupOffset][StageIndex];
    }

    static constexpr int32 LevelsD2ToD5[4][6][3] =
    {
        {
            { 8, 10, 13 }, { 9, 11, 14 }, { 10, 12, 15 },
            { 11, 13, 16 }, { 12, 14, 17 }, { 13, 15, 18 }
        },
        {
            { 16, 18, 21 }, { 17, 19, 22 }, { 18, 20, 23 },
            { 19, 21, 24 }, { 20, 22, 25 }, { 21, 23, 26 }
        },
        {
            { 24, 26, 29 }, { 25, 27, 30 }, { 26, 28, 31 },
            { 27, 29, 32 }, { 28, 30, 33 }, { 29, 31, 34 }
        },
        {
            { 32, 35, 38 }, { 33, 36, 39 }, { 34, 37, 40 },
            { 35, 38, 41 }, { 36, 39, 42 }, { 37, 40, 43 }
        }
    };

    return LevelsD2ToD5[Degree - 2][GroupOffset][StageIndex];
}

bool UDegreeProgressionLibrary::IsSealStageValid(
    const EDegreeStage DegreeStage,
    const ESealTier SealTier)
{
    if (SealTier == ESealTier::Normal)
    {
        return true;
    }

    return DegreeStage == EDegreeStage::Main;
}

bool UDegreeProgressionLibrary::IsNPCShopEligible(
    const EDegreeStage DegreeStage,
    const ESealTier SealTier)
{
    return SealTier == ESealTier::Normal
        && DegreeStage == EDegreeStage::Main;
}
