#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ItemTypes.h"
#include "SealSystem.generated.h"

// ============================================================================
// SEAL / SOX SYSTEM
//
// Current project scope: classic Degree 1-5 itemization.
// Supported tiers:
//   Normal
//   Seal of Star
//   Seal of Moon
//   Seal of Sun
//
// Important:
// SOx is a rarity/tier classification, not a synthetic +value.
// Actual attack/defense values belong to the item's static definition data.
// ============================================================================
UCLASS()
class JANGANPROTOTYPE_API USealSystemLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:

    // True for Star / Moon / Sun.
    UFUNCTION(BlueprintPure, Category = "Items|Seal")
    static bool IsSealItem(ESealTier SealTier);

    // Normal=0, Star=1, Moon=2, Sun=3.
    UFUNCTION(BlueprintPure, Category = "Items|Seal")
    static int32 GetSealRank(ESealTier SealTier);

    // In the classic 1-5D model, SOx items use the Main stage of the degree.
    UFUNCTION(BlueprintPure, Category = "Items|Seal")
    static bool IsStageValidForSeal(EDegreeStage DegreeStage, ESealTier SealTier);

    // Convenience validation for static item definitions.
    // This does not validate numerical stats; those remain data-driven.
    UFUNCTION(BlueprintPure, Category = "Items|Seal")
    static bool IsSealDefinitionValid(const FItemDefinition& ItemDefinition);

    // Classic 1-5D SOx is drop-only in our project model.
    UFUNCTION(BlueprintPure, Category = "Items|Seal")
    static bool IsNPCPurchasable(ESealTier SealTier);
};
