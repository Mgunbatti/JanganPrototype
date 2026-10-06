#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "ItemTypes.generated.h"


// ============================================================================
// ITEM CATEGORY
// ============================================================================

UENUM(BlueprintType)
enum class EItemCategory : uint8
{
    None        UMETA(DisplayName = "None"),
    Weapon      UMETA(DisplayName = "Weapon"),
    Shield      UMETA(DisplayName = "Shield"),
    Ammunition  UMETA(DisplayName = "Ammunition"),
    Armor       UMETA(DisplayName = "Armor"),
    Accessory   UMETA(DisplayName = "Accessory"),
    Consumable  UMETA(DisplayName = "Consumable"),
    Material    UMETA(DisplayName = "Material")
};


// ============================================================================
// CHINESE WEAPON TYPE
// ============================================================================

UENUM(BlueprintType)
enum class EWeaponType : uint8
{
    None    UMETA(DisplayName = "None"),
    Blade   UMETA(DisplayName = "Blade"),
    Sword   UMETA(DisplayName = "Sword"),
    Glavie  UMETA(DisplayName = "Glavie"),
    Spear   UMETA(DisplayName = "Spear"),
    Bow     UMETA(DisplayName = "Bow")
};


// ============================================================================
// DEGREE STAGE
//
// Every normal degree contains three item levels.
//
// Main = First / lowest level of the degree.
//        NPC shops sell this level.
//        SOx items always use this level.
//
// Mid  = Second item level.
//
// High = Third item level.
// ============================================================================

UENUM(BlueprintType)
enum class EDegreeStage : uint8
{
    Main    UMETA(DisplayName = "Main"),
    Mid     UMETA(DisplayName = "Mid"),
    High    UMETA(DisplayName = "High")
};


// ============================================================================
// SEAL TIER
// ============================================================================

UENUM(BlueprintType)
enum class ESealTier : uint8
{
    Normal      UMETA(DisplayName = "Normal"),
    SealOfStar  UMETA(DisplayName = "Seal of Star"),
    SealOfMoon  UMETA(DisplayName = "Seal of Moon"),
    SealOfSun   UMETA(DisplayName = "Seal of Sun")
};


// ============================================================================
// EQUIPMENT SLOT
// ============================================================================

UENUM(BlueprintType)
enum class EEquipmentSlot : uint8
{
    None        UMETA(DisplayName = "None"),
    MainHand    UMETA(DisplayName = "Main Hand"),
    OffHand     UMETA(DisplayName = "Off Hand")
};


// ============================================================================
// OFFHAND RULE
//
// Blade / Sword -> Shield can be equipped.
// Bow           -> Arrow must be equipped.
// Glavie/Spear  -> Offhand cannot be used.
// ============================================================================

UENUM(BlueprintType)
enum class EOffHandRule : uint8
{
    None            UMETA(DisplayName = "None"),
    ShieldAllowed   UMETA(DisplayName = "Shield Allowed"),
    ArrowRequired   UMETA(DisplayName = "Arrow Required"),
    Blocked         UMETA(DisplayName = "Blocked")
};


// ============================================================================
// AMMUNITION TYPE
// ============================================================================

UENUM(BlueprintType)
enum class EAmmunitionType : uint8
{
    None    UMETA(DisplayName = "None"),
    Arrow   UMETA(DisplayName = "Arrow")
};


// ============================================================================
// GENERIC MIN / MAX STAT RANGE
// ============================================================================

USTRUCT(BlueprintType)
struct FStatRange
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float Min = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly)
    float Max = 0.0f;
};


// ============================================================================
// WEAPON STATS
// ============================================================================

USTRUCT(BlueprintType)
struct FWeaponStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Attack")
    FStatRange MeleeAttackPower;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Attack")
    FStatRange MagicalAttackPower;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Specialization")
    FStatRange MeleeSpecialization;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Specialization")
    FStatRange MagicalSpecialization;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
    int32 Durability = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Weapon")
    int32 Accuracy = 0;
};


// ============================================================================
// SHIELD STATS
// ============================================================================

USTRUCT(BlueprintType)
struct FShieldStats
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Defense")
    float MeleeDefensivePower = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Defense")
    float MagicalDefensivePower = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Specialization")
    float MeleeSpecialization = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Specialization")
    float MagicalSpecialization = 0.0f;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Shield")
    int32 Durability = 0;
};


// ============================================================================
// MASTER ITEM DEFINITION
//
// IMPORTANT:
//
// This contains STATIC item data.
//
// Example:
// Copper Sword
// Degree 1
// Level 1
// Melee Attack 15-16
//
// Player-specific information such as:
//
// +7
// Current Durability
// Blues
// Alchemy modifications
//
// WILL NOT be stored here.
//
// Those will belong to FItemInstance later.
// ============================================================================

USTRUCT(BlueprintType)
struct FItemDefinition : public FTableRowBase
{
    GENERATED_BODY()


    // ------------------------------------------------------------------------
    // IDENTITY
    // ------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Identity")
    FName ItemID = NAME_None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Identity")
    FText DisplayName;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Identity")
    EItemCategory ItemCategory = EItemCategory::None;


    // ------------------------------------------------------------------------
    // PROGRESSION
    // ------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Progression")
    int32 Degree = 1;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Progression")
    EDegreeStage DegreeStage = EDegreeStage::Main;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Progression")
    int32 RequiredLevel = 1;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Progression")
    ESealTier SealTier = ESealTier::Normal;


    // ------------------------------------------------------------------------
    // EQUIPMENT
    // ------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Equipment")
    EEquipmentSlot EquipmentSlot = EEquipmentSlot::None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Equipment")
    EWeaponType WeaponType = EWeaponType::None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Equipment")
    EOffHandRule OffHandRule = EOffHandRule::None;


    // ------------------------------------------------------------------------
    // AMMUNITION
    // ------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Ammunition")
    EAmmunitionType AmmunitionType = EAmmunitionType::None;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Ammunition")
    int32 MaxStackSize = 1;


    // ------------------------------------------------------------------------
    // ITEM STATS
    // ------------------------------------------------------------------------

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats")
    FWeaponStats WeaponStats;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Stats")
    FShieldStats ShieldStats;


    // ------------------------------------------------------------------------
    // ECONOMY
    // ------------------------------------------------------------------------

    // Can this item be purchased directly from an NPC shop?
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Economy")
    bool bSoldByNPC = false;

    // Can the player sell this item to an NPC?
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Economy")
    bool bCanSellToNPC = true;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Economy")
    int64 BuyPrice = 0;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Economy")
    int64 SellPrice = 0;
};