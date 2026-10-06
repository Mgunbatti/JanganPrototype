#include "Items/SealSystem.h"

bool USealSystemLibrary::IsSealItem(const ESealTier SealTier)
{
    return SealTier == ESealTier::SealOfStar
        || SealTier == ESealTier::SealOfMoon
        || SealTier == ESealTier::SealOfSun;
}

int32 USealSystemLibrary::GetSealRank(const ESealTier SealTier)
{
    switch (SealTier)
    {
    case ESealTier::Normal:     return 0;
    case ESealTier::SealOfStar: return 1;
    case ESealTier::SealOfMoon: return 2;
    case ESealTier::SealOfSun:  return 3;
    default:                    return INDEX_NONE;
    }
}

bool USealSystemLibrary::IsStageValidForSeal(
    const EDegreeStage DegreeStage,
    const ESealTier SealTier)
{
    if (SealTier == ESealTier::Normal)
    {
        return true;
    }

    return DegreeStage == EDegreeStage::Main;
}

bool USealSystemLibrary::IsSealDefinitionValid(
    const FItemDefinition& ItemDefinition)
{
    if (!IsStageValidForSeal(ItemDefinition.DegreeStage, ItemDefinition.SealTier))
    {
        return false;
    }

    if (IsSealItem(ItemDefinition.SealTier) && ItemDefinition.bSoldByNPC)
    {
        return false;
    }

    return true;
}

bool USealSystemLibrary::IsNPCPurchasable(const ESealTier SealTier)
{
    return SealTier == ESealTier::Normal;
}
