"""
Recommendation system for crop diseases.
Maps disease names to medicine, fertilizer, and prevention tips.
"""

from typing import Dict, Optional


# Disease to solution mapping
# Format: disease_name -> {medicine, fertilizer, tips}
DISEASE_RECOMMENDATIONS: Dict[str, Dict[str, str]] = {
    # Tomato diseases
    "tomato_early_blight": {
        "medicine": "Mancozeb, Chlorothalonil",
        "fertilizer": "NPK (balanced), Potassium-rich fertilizer",
        "tips": "Avoid overwatering, ensure proper spacing, remove infected leaves, rotate crops annually",
    },
    "tomato_late_blight": {
        "medicine": "Copper-based fungicide, Mancozeb",
        "fertilizer": "NPK with higher Potassium",
        "tips": "Improve air circulation, avoid overhead watering, use resistant varieties",
    },
    "tomato_leaf_mold": {
        "medicine": "Chlorothalonil, Copper oxychloride",
        "fertilizer": "Balanced NPK, Calcium nitrate",
        "tips": "Reduce humidity, increase ventilation in greenhouses, water at soil level",
    },
    "tomato_septoria_leaf_spot": {
        "medicine": "Mancozeb, Chlorothalonil",
        "fertilizer": "NPK, Magnesium sulfate",
        "tips": "Remove infected leaves, avoid wet foliage, practice crop rotation",
    },
    "tomato_spider_mites": {
        "medicine": "Neem oil, Abamectin, Sulfur spray",
        "fertilizer": "Balanced NPK",
        "tips": "Increase humidity, remove weeds, introduce predatory mites",
    },
    "tomato_target_spot": {
        "medicine": "Chlorothalonil, Azoxystrobin",
        "fertilizer": "NPK with Potassium",
        "tips": "Remove plant debris, avoid overhead irrigation, use mulch",
    },
    "tomato_yellow_leaf_curl_virus": {
        "medicine": "No direct cure - control whiteflies with Imidacloprid",
        "fertilizer": "Balanced NPK to support plant health",
        "tips": "Use resistant varieties, control whitefly population, remove infected plants",
    },
    "tomato_mosaic_virus": {
        "medicine": "No cure - focus on prevention",
        "fertilizer": "Balanced NPK for plant vigor",
        "tips": "Use virus-free seeds, sanitize tools, control aphids, remove infected plants",
    },
    "tomato_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK maintenance dose",
        "tips": "Continue good practices: proper watering, monitoring, crop rotation",
    },
    # Potato diseases
    "potato_early_blight": {
        "medicine": "Mancozeb, Chlorothalonil",
        "fertilizer": "NPK, Potassium sulfate",
        "tips": "Avoid overhead irrigation, remove infected foliage, rotate crops",
    },
    "potato_late_blight": {
        "medicine": "Copper fungicide, Metalaxyl-M",
        "fertilizer": "Potassium-rich NPK",
        "tips": "Destroy infected tubers, use certified seed, improve drainage",
    },
    "potato_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK for potatoes",
        "tips": "Monitor regularly, maintain soil health, practice crop rotation",
    },
    # Pepper diseases
    "pepper_bacterial_spot": {
        "medicine": "Copper-based bactericide, Streptomycin",
        "fertilizer": "Balanced NPK, Calcium",
        "tips": "Use disease-free seeds, avoid overhead watering, sanitize equipment",
    },
    "pepper_bell_bacterial_spot": {
        "medicine": "Copper-based bactericide, Streptomycin",
        "fertilizer": "Balanced NPK, Calcium",
        "tips": "Use disease-free seeds, avoid overhead watering, sanitize equipment",
    },
    "pepper_bell_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK",
        "tips": "Continue monitoring and good cultural practices",
    },
    "pepper_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK",
        "tips": "Continue monitoring and good cultural practices",
    },
    # Corn/Maize diseases
    "corn_cercospora_leaf_spot": {
        "medicine": "Azoxystrobin, Propiconazole",
        "fertilizer": "Nitrogen, NPK",
        "tips": "Crop rotation, remove residue, use resistant hybrids",
    },
    "corn_common_rust": {
        "medicine": "Propiconazole, Azoxystrobin",
        "fertilizer": "Balanced NPK",
        "tips": "Plant early, use resistant varieties, ensure good drainage",
    },
    "corn_northern_leaf_blight": {
        "medicine": "Propiconazole, Trifloxystrobin",
        "fertilizer": "NPK with Nitrogen",
        "tips": "Tillage to bury residue, crop rotation, resistant hybrids",
    },
    "corn_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK for corn",
        "tips": "Monitor for pests and diseases, maintain soil fertility",
    },
    # Grape diseases
    "grape_black_rot": {
        "medicine": "Captan, Mancozeb, Myclobutanil",
        "fertilizer": "Balanced NPK",
        "tips": "Remove mummified berries, improve air circulation, fungicide at bloom",
    },
    "grape_esca": {
        "medicine": "No effective cure - preventative only",
        "fertilizer": "Balanced NPK, Boron",
        "tips": "Prune properly, avoid wounding, remove infected vines",
    },
    "grape_leaf_blight": {
        "medicine": "Copper fungicide, Mancozeb",
        "fertilizer": "NPK, Potassium",
        "tips": "Remove infected leaves, improve ventilation, avoid wet foliage",
    },
    "grape_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular grape fertilizer",
        "tips": "Proper pruning, canopy management, regular monitoring",
    },
    # Apple diseases
    "apple_scab": {
        "medicine": "Captan, Sulfur, Myclobutanil",
        "fertilizer": "Balanced NPK",
        "tips": "Remove fallen leaves, prune for air flow, use resistant varieties",
    },
    "apple_cedar_apple_rust": {
        "medicine": "Myclobutanil, Propiconazole",
        "fertilizer": "NPK",
        "tips": "Remove cedar trees nearby, apply fungicide at pink bud stage",
    },
    "apple_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular apple tree fertilizer",
        "tips": "Dormant spray, proper pruning, monitor for pests",
    },
    # Strawberry diseases
    "strawberry_leaf_scorch": {
        "medicine": "Chlorothalonil, Captan",
        "fertilizer": "Balanced NPK",
        "tips": "Remove infected leaves, improve drainage, avoid overhead irrigation",
    },
    "strawberry_healthy": {
        "medicine": "None required",
        "fertilizer": "Strawberry-specific NPK",
        "tips": "Mulch properly, remove runners, monitor regularly",
    },
    # Blueberry diseases
    "blueberry_healthy": {
        "medicine": "None required",
        "fertilizer": "Acidic fertilizer for blueberries",
        "tips": "Maintain soil pH 4.5-5.5, proper pruning, mulch",
    },
    # Cherry diseases
    "cherry_powdery_mildew": {
        "medicine": "Sulfur, Myclobutanil, Potassium bicarbonate",
        "fertilizer": "Balanced NPK",
        "tips": "Improve air circulation, remove infected shoots, avoid excess nitrogen",
    },
    "cherry_healthy": {
        "medicine": "None required",
        "fertilizer": "Regular fruit tree fertilizer",
        "tips": "Proper pruning, monitor for pests, good irrigation",
    },
    # Peach diseases
    "peach_bacterial_spot": {
        "medicine": "Copper bactericide, Streptomycin",
        "fertilizer": "Balanced NPK",
        "tips": "Use resistant varieties, avoid overhead irrigation, prune properly",
    },
    "peach_healthy": {
        "medicine": "None required",
        "fertilizer": "Peach tree fertilizer",
        "tips": "Dormant oil spray, proper pruning, thin fruits",
    },
    # Squash diseases
    "squash_powdery_mildew": {
        "medicine": "Sulfur, Potassium bicarbonate, Neem oil",
        "fertilizer": "Balanced NPK",
        "tips": "Resistant varieties, adequate spacing, avoid overhead watering",
    },
    "squash_healthy": {
        "medicine": "None required",
        "fertilizer": "NPK for cucurbits",
        "tips": "Crop rotation, trellising for air flow, monitor regularly",
    },
    # Soybean diseases
    "soybean_healthy": {
        "medicine": "None required",
        "fertilizer": "Rhizobium inoculation, NPK",
        "tips": "Crop rotation, proper planting depth, weed control",
    },
    # Generic fallback
    "early_blight": {
        "medicine": "Mancozeb, Chlorothalonil",
        "fertilizer": "NPK (balanced), Potassium-rich fertilizer",
        "tips": "Avoid overwatering, ensure proper spacing, remove infected leaves, rotate crops annually",
    },
    "late_blight": {
        "medicine": "Copper-based fungicide, Mancozeb",
        "fertilizer": "NPK with higher Potassium",
        "tips": "Improve air circulation, avoid overhead watering, use resistant varieties",
    },
    "healthy": {
        "medicine": "None required",
        "fertilizer": "Regular NPK maintenance dose",
        "tips": "Continue good practices: proper watering, monitoring, crop rotation",
    },
    # CGC Hackathon / generic leaf classes
    "powdery": {
        "medicine": "Sulfur, Potassium bicarbonate, Neem oil",
        "fertilizer": "Balanced NPK, avoid excess nitrogen",
        "tips": "Improve air circulation, reduce humidity, resistant varieties, avoid overhead watering",
    },
    "rust": {
        "medicine": "Copper fungicide, Propiconazole, Chlorothalonil",
        "fertilizer": "Potassium-rich NPK",
        "tips": "Remove infected leaves, ensure good drainage, use resistant varieties",
    },
}


def get_recommendation(disease_name: str) -> Dict[str, str]:
    """
    Get recommendation for a given disease name.
    Performs fuzzy matching to handle variations in disease naming.

    Args:
        disease_name: Name of the detected disease (e.g., "Tomato_Early_Blight")

    Returns:
        Dictionary with medicine, fertilizer, and tips keys
    """
    # Normalize: lowercase, replace spaces/underscores (PlantVillage uses ___)
    normalized = (
        disease_name.lower()
        .strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("___", "_")
        .replace("__", "_")
    )

    # Direct match
    if normalized in DISEASE_RECOMMENDATIONS:
        return DISEASE_RECOMMENDATIONS[normalized].copy()

    # Try partial match (e.g., "early_blight" in "tomato_early_blight")
    for key, value in DISEASE_RECOMMENDATIONS.items():
        if normalized in key or key in normalized:
            return value.copy()

    # Try matching key parts
    parts = normalized.split("_")
    for key in DISEASE_RECOMMENDATIONS:
        if all(part in key for part in parts if len(part) > 2):
            return DISEASE_RECOMMENDATIONS[key].copy()

    # Fallback to generic healthy or early_blight
    return DISEASE_RECOMMENDATIONS.get(
        "healthy",
        {
            "medicine": "Consult local agricultural expert",
            "fertilizer": "Balanced NPK recommended",
            "tips": "Isolate affected plant, take sample to extension office for diagnosis",
        },
    ).copy()


def format_recommendation(disease_name: str) -> str:
    """
    Format recommendation as human-readable string.

    Args:
        disease_name: Name of the disease

    Returns:
        Formatted string with all recommendations
    """
    rec = get_recommendation(disease_name)
    return (
        f"Medicine: {rec['medicine']}\n"
        f"Fertilizer: {rec['fertilizer']}\n"
        f"Tips: {rec['tips']}"
    )
