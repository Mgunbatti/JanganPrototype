#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ItemTypes.h"
#include "DegreeProgression.generated.h"

// ============================================================================
// DEGREE EQUIPMENT GROUP
//
// Required levels are not identical for every equipment piece inside a degree.
// This grouping mirrors the original 1D-5D progression table.
//
// Weapon / Shield / Gloves share the same level progression.
// Armor pieces then progress in order: Shoulder, Foot, Head, Legs, Chest.
// ============================================================================
UENUM(BlueprintType)
enum class EDegreeEquipmentGroup : uint8
{
    WeaponShieldGloves UMETA(DisplayName = "Weapon / Shield / Gloves"),
    Shoulder           UMETA(DisplayName = "Shoulder"),
    Foot               UMETA(DisplayName = "Foot"),
    Head               UMETA(DisplayName = "Head"),
    Legs               UMETA(DisplayName = "Legs"),
    Chest              UMETA(DisplayName = "Chest")
};


// ============================================================================
// DEGREE PROGRESSION LIBRARY
//
// Current project scope: Degree 1 through Degree 5 only.
//
// This class is intentionally stateless. It provides one canonical source for
// item required levels and the progression rules used by DataTables, item
// validation, shops and future drop generation.
// ============================================================================
UCLASS()
class JANGANPROTOTYPE_API UDegreeProgressionLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:

    // Returns true only for degrees currently supported by JanganPrototype.
    UFUNCTION(BlueprintPure, Category = "Items|Progression")
    static bool IsSupportedDegree(int32 Degree);

    // Returns the required character level for the exact degree, equipment
    // group and stage. Returns INDEX_NONE (-1) for unsupported input.
    UFUNCTION(BlueprintPure, Category = "Items|Progression")
    static int32 GetRequiredLevel(
        int32 Degree,
        EDegreeEquipmentGroup EquipmentGroup,
        EDegreeStage DegreeStage);

    // Convenience anchor for the first weapon/shield/glove level of a degree.
    // D1=1, D2=8, D3=16, D4=24, D5=32.
    //
    // Note: armor pieces have their own slot-specific Main levels, so use
    // GetRequiredLevel() for actual item requirements.
    UFUNCTION(BlueprintPure, Category = "Items|Progression")
    static int32 GetDegreeBaseLevel(int32 Degree);

    // Normal items may use Main / Mid / High.
    // SOx items are restricted to the Main stage of their equipment group.
    UFUNCTION(BlueprintPure, Category = "Items|Progression")
    static bool IsSealStageValid(EDegreeStage DegreeStage, ESealTier SealTier);

    // NPC shop progression rule:
    // only Normal + Main-stage equipment is directly shop-eligible.
    UFUNCTION(BlueprintPure, Category = "Items|Progression")
    static bool IsNPCShopEligible(EDegreeStage DegreeStage, ESealTier SealTier);
};
