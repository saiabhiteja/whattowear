const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/** Use for image/photo URLs from the API; supports both full URLs and local paths (e.g. /uploads/...). */
export function imageUrl(url: string): string {
  if (!url) return "";
  return url.startsWith("http") ? url : `${BASE_URL.replace(/\/$/, "")}${url.startsWith("/") ? url : `/${url}`}`;
}

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, options);
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Something went wrong" }));
    throw new Error(error.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}

// Types
export interface UserProfile {
  id: string;
  photo_url: string;
  skin_tone: "FAIR" | "MEDIUM" | "DARK";
  skin_undertone: "WARM" | "COOL" | "NEUTRAL";
  created_at: string;
  updated_at: string;
}

export interface UploadPhotoResponse {
  message: string;
  photo_url: string;
  skin_tone: string;
  skin_undertone: string;
}

export interface ClothingItem {
  id: string;
  image_url: string;
  dominant_color: string;
  secondary_color: string;
  clothing_type: string;
  occasion: string;
  season: string;
  created_at: string;
}

export interface Suggestion {
  clothing: ClothingItem;
  score: number;
  reasons: string[];
}

export interface RecommendationResponse {
  suggestions: Suggestion[];
  event: string;
  weather: string;
  time_of_day: string;
}

export const CLOTHING_TYPES = ["SHIRT", "TSHIRT", "JEANS", "TROUSERS", "KURTA", "JACKET", "SHORTS", "DRESS", "BLAZER", "HOODIE"] as const;
export const OCCASIONS = ["CASUAL", "OFFICE", "PARTY", "WEDDING", "TRADITIONAL"] as const;
export const SEASONS = ["SUMMER", "WINTER", "ALL"] as const;
export const EVENTS = ["OFFICE", "CASUAL", "PARTY", "WEDDING"] as const;
export const WEATHER_OPTIONS = ["HOT", "COLD", "RAINY"] as const;
export const TIME_OPTIONS = ["DAY", "NIGHT"] as const;

// API functions
export async function healthCheck() {
  return request<{ status: string; app: string }>("/");
}

export async function uploadPhoto(photo: File): Promise<UploadPhotoResponse> {
  const formData = new FormData();
  formData.append("photo", photo);
  return request<UploadPhotoResponse>("/user/upload-photo", {
    method: "POST",
    body: formData,
  });
}

export async function getUserProfile(): Promise<UserProfile> {
  return request<UserProfile>("/user/profile");
}

export async function uploadClothing(
  image: File,
  clothingType: string,
  occasion: string,
  season: string
): Promise<ClothingItem> {
  const formData = new FormData();
  formData.append("image", image);
  formData.append("clothing_type", clothingType);
  formData.append("occasion", occasion);
  formData.append("season", season);
  return request<ClothingItem>("/clothing/upload", {
    method: "POST",
    body: formData,
  });
}

export async function getAllClothing(): Promise<ClothingItem[]> {
  return request<ClothingItem[]>("/clothing/all");
}

export async function getRecommendations(
  event: string,
  weather: string,
  timeOfDay: string
): Promise<RecommendationResponse> {
  return request<RecommendationResponse>("/recommendation/suggest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ event, weather, time_of_day: timeOfDay }),
  });
}
